"""
DeepSeek LLM实现
"""
import json
import httpx
from typing import List, Dict, Any
from core.logger import logger
from .base import BaseLLM, ChatMessage, ChatResponse


class DeepSeekLLM(BaseLLM):
    """DeepSeek LLM实现类"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com/v1"):
        super().__init__(api_key, base_url)
        self.default_model = "deepseek-chat"
    
    async def chat_completion(
        self,
        messages: List[ChatMessage],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        enable_thinking: bool = False
    ) -> ChatResponse:
        """DeepSeek聊天完成实现"""
        
        if not model:
            model = self.default_model
            
        # 如果启用思维链，添加系统提示
        if enable_thinking:
            thinking_prompt = """
请在回答问题时，先展示你的思考过程。格式如下：
<thinking>
1. 分析问题...
2. 考虑可能的解决方案...
3. 选择最佳方案...
</thinking>

然后给出你的最终回答。
"""
            # 在消息开头添加思维链提示
            enhanced_messages = [
                ChatMessage(role="system", content=thinking_prompt)
            ] + messages
        else:
            enhanced_messages = messages
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [{"role": msg.role, "content": msg.content} for msg in enhanced_messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60.0
                )
                response.raise_for_status()
                
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # 解析思维过程
                thinking_process = None
                if enable_thinking and "<thinking>" in content:
                    thinking_start = content.find("<thinking>") + len("<thinking>")
                    thinking_end = content.find("</thinking>")
                    if thinking_end > thinking_start:
                        thinking_text = content[thinking_start:thinking_end].strip()
                        thinking_process = [step.strip() for step in thinking_text.split('\n') if step.strip()]
                        # 移除思维过程，只保留最终回答
                        content = content[thinking_end + len("</thinking>"):].strip()
                
                logger.info(f"DeepSeek API调用成功，模型: {model}")
                
                return ChatResponse(
                    content=content,
                    thinking_process=thinking_process,
                    usage=result.get("usage"),
                    model=model
                )
                
        except httpx.HTTPError as e:
            logger.error(f"DeepSeek API调用失败: {e}")
            raise Exception(f"DeepSeek API调用失败: {e}")
        except Exception as e:
            logger.error(f"DeepSeek处理异常: {e}")
            raise Exception(f"DeepSeek处理异常: {e}")
    
    def get_available_models(self) -> List[str]:
        """获取DeepSeek可用模型列表"""
        return ["deepseek-chat", "deepseek-coder"] 