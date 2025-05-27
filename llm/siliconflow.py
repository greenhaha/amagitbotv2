"""
SiliconFlow LLM实现
"""
import json
import httpx
from typing import List, Dict, Any
from core.logger import logger
from .base import BaseLLM, ChatMessage, ChatResponse


class SiliconFlowLLM(BaseLLM):
    """SiliconFlow LLM实现类"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.siliconflow.cn/v1", default_model: str = "Qwen/Qwen2.5-7B-Instruct"):
        super().__init__(api_key, base_url)
        self.default_model = default_model
        
        # SiliconFlow支持的模型列表
        self.available_models = {
            # Qwen系列
            "Qwen/Qwen2.5-7B-Instruct": {
                "name": "通义千问2.5-7B",
                "description": "阿里巴巴通义千问2.5-7B指令模型，平衡性能与效率",
                "max_tokens": 8192,
                "context_length": 32768
            },
            "Qwen/Qwen2.5-14B-Instruct": {
                "name": "通义千问2.5-14B", 
                "description": "阿里巴巴通义千问2.5-14B指令模型，更强的推理能力",
                "max_tokens": 8192,
                "context_length": 32768
            },
            "Qwen/Qwen2.5-32B-Instruct": {
                "name": "通义千问2.5-32B",
                "description": "阿里巴巴通义千问2.5-32B指令模型，顶级性能",
                "max_tokens": 8192,
                "context_length": 32768
            },
            "Qwen/Qwen2.5-72B-Instruct": {
                "name": "通义千问2.5-72B",
                "description": "阿里巴巴通义千问2.5-72B指令模型，最强性能",
                "max_tokens": 8192,
                "context_length": 32768
            },
            "Qwen/Qwen3-235B-A22B": {
                "name": "通义千问3-235B",
                "description": "阿里巴巴通义千问3-235B MoE模型，支持思维链推理，顶级性能",
                "max_tokens": 8192,
                "context_length": 32768
            },
            # Meta Llama系列
            "meta-llama/Meta-Llama-3.1-8B-Instruct": {
                "name": "Llama 3.1-8B",
                "description": "Meta Llama 3.1-8B指令模型，开源领先",
                "max_tokens": 4096,
                "context_length": 128000
            },
            "meta-llama/Meta-Llama-3.1-70B-Instruct": {
                "name": "Llama 3.1-70B",
                "description": "Meta Llama 3.1-70B指令模型，强大性能",
                "max_tokens": 4096,
                "context_length": 128000
            },
            "meta-llama/Meta-Llama-3.1-405B-Instruct": {
                "name": "Llama 3.1-405B",
                "description": "Meta Llama 3.1-405B指令模型，顶级开源模型",
                "max_tokens": 4096,
                "context_length": 128000
            },
            # DeepSeek系列
            "deepseek-ai/DeepSeek-V2.5": {
                "name": "DeepSeek V2.5",
                "description": "DeepSeek V2.5模型，强大的推理能力",
                "max_tokens": 4096,
                "context_length": 32768
            },
            "deepseek-ai/deepseek-llm-67b-chat": {
                "name": "DeepSeek 67B Chat",
                "description": "DeepSeek 67B对话模型",
                "max_tokens": 4096,
                "context_length": 4096
            },
            # 其他模型
            "01-ai/Yi-1.5-34B-Chat": {
                "name": "Yi 1.5-34B Chat",
                "description": "零一万物Yi 1.5-34B对话模型",
                "max_tokens": 4096,
                "context_length": 4096
            },
            "THUDM/glm-4-9b-chat": {
                "name": "GLM-4-9B Chat",
                "description": "智谱GLM-4-9B对话模型",
                "max_tokens": 8192,
                "context_length": 128000
            },
            "internlm/internlm2_5-7b-chat": {
                "name": "InternLM2.5-7B Chat",
                "description": "上海AI实验室InternLM2.5-7B对话模型",
                "max_tokens": 4096,
                "context_length": 32768
            }
        }
    
    async def chat_completion(
        self,
        messages: List[ChatMessage],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = None,
        enable_thinking: bool = False
    ) -> ChatResponse:
        """SiliconFlow聊天完成实现"""
        
        if not model:
            model = self.default_model
            
        # 验证模型是否支持
        if model not in self.available_models:
            logger.warning(f"模型 {model} 不在支持列表中，使用默认模型 {self.default_model}")
            model = self.default_model
            
        # 根据模型设置合适的max_tokens
        if max_tokens is None:
            model_info = self.available_models.get(model, {})
            max_tokens = min(model_info.get("max_tokens", 2000), 2000)  # 限制在2000以内
            
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
                
                logger.info(f"SiliconFlow API调用成功，模型: {model}")
                
                return ChatResponse(
                    content=content,
                    thinking_process=thinking_process,
                    usage=result.get("usage"),
                    model=model
                )
                
        except httpx.HTTPError as e:
            logger.error(f"SiliconFlow API调用失败: {e}")
            raise Exception(f"SiliconFlow API调用失败: {e}")
        except Exception as e:
            logger.error(f"SiliconFlow处理异常: {e}")
            raise Exception(f"SiliconFlow处理异常: {e}")
    
    def get_available_models(self) -> List[str]:
        """获取SiliconFlow可用模型列表"""
        return list(self.available_models.keys())
    
    def get_model_info(self, model: str = None) -> Dict[str, Any]:
        """获取模型详细信息"""
        if not model:
            model = self.default_model
        return self.available_models.get(model, {})
    
    def get_all_models_info(self) -> Dict[str, Dict[str, Any]]:
        """获取所有模型的详细信息"""
        return self.available_models 