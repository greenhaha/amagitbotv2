"""
LLM工厂类
根据配置创建不同的LLM实例
"""
from typing import Optional
from core.config import settings
from core.logger import logger
from .base import BaseLLM
from .deepseek import DeepSeekLLM
from .siliconflow import SiliconFlowLLM
from .mock import MockLLM


class LLMFactory:
    """LLM工厂类"""
    
    @staticmethod
    def create_llm(provider: Optional[str] = None) -> BaseLLM:
        """
        创建LLM实例
        
        Args:
            provider: LLM提供商名称，如果为None则使用默认配置
            
        Returns:
            BaseLLM: LLM实例
        """
        if not provider:
            provider = settings.default_llm_provider
        
        provider = provider.lower()
        
        if provider == "deepseek":
            if not settings.deepseek_api_key:
                raise ValueError("DeepSeek API Key未配置")
            
            logger.info("创建DeepSeek LLM实例")
            return DeepSeekLLM(
                api_key=settings.deepseek_api_key,
                base_url=settings.deepseek_base_url
            )
        
        elif provider == "siliconflow":
            if not settings.siliconflow_api_key:
                raise ValueError("SiliconFlow API Key未配置")
            
            logger.info("创建SiliconFlow LLM实例")
            return SiliconFlowLLM(
                api_key=settings.siliconflow_api_key,
                base_url=settings.siliconflow_base_url,
                default_model=settings.siliconflow_default_model
            )
        
        elif provider == "mock":
            logger.info("创建模拟LLM实例")
            return MockLLM()
        
        else:
            raise ValueError(f"不支持的LLM提供商: {provider}")
    
    @staticmethod
    def get_available_providers() -> list:
        """获取可用的LLM提供商列表"""
        providers = []
        
        if settings.deepseek_api_key:
            providers.append("deepseek")
        
        if settings.siliconflow_api_key:
            providers.append("siliconflow")
        
        # 模拟提供商总是可用
        providers.append("mock")
        
        return providers 