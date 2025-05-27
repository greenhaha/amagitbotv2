"""
LLM基础抽象类
定义统一的LLM接口，支持不同的LLM提供商
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    """聊天消息模型"""
    role: str  # system, user, assistant
    content: str


class ChatResponse(BaseModel):
    """聊天响应模型"""
    content: str
    thinking_process: Optional[List[str]] = None  # 思维链步骤
    usage: Optional[Dict[str, Any]] = None
    model: Optional[str] = None


class BaseLLM(ABC):
    """LLM基础抽象类"""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
    
    @abstractmethod
    async def chat_completion(
        self,
        messages: List[ChatMessage],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        enable_thinking: bool = False
    ) -> ChatResponse:
        """
        聊天完成接口
        
        Args:
            messages: 聊天消息列表
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
            enable_thinking: 是否启用思维链
            
        Returns:
            ChatResponse: 聊天响应
        """
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """获取可用的模型列表"""
        pass 