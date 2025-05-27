"""
配置管理模块
负责加载环境变量和系统配置
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Settings(BaseSettings):
    """系统配置类"""
    
    # LLM API 配置
    deepseek_api_key: Optional[str] = os.getenv("DEEPSEEK_API_KEY")
    deepseek_base_url: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    
    siliconflow_api_key: Optional[str] = os.getenv("SILICONFLOW_API_KEY")
    siliconflow_base_url: str = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
    siliconflow_default_model: str = os.getenv("SILICONFLOW_DEFAULT_MODEL", "Qwen/Qwen2.5-7B-Instruct")
    
    deepseek_default_model: str = os.getenv("DEEPSEEK_DEFAULT_MODEL", "deepseek-chat")
    
    default_llm_provider: str = os.getenv("DEFAULT_LLM_PROVIDER", "deepseek")
    
    # 机器人默认配置
    default_bot_name: str = os.getenv("DEFAULT_BOT_NAME", "天城")
    default_bot_description: str = os.getenv("DEFAULT_BOT_DESCRIPTION", "我是天城，一只可爱的猫耳女仆，随时为您服务喵～")
    default_bot_personality: str = os.getenv("DEFAULT_BOT_PERSONALITY", "gentle")
    default_bot_background: str = os.getenv("DEFAULT_BOT_BACKGROUND", "天城是一只来自异世界的猫耳女仆，拥有温柔善良的性格和强烈的服务精神。她喜欢帮助别人，总是用最温暖的笑容面对每一个人。")
    
    # 机器人说话风格配置
    default_use_cat_speech: bool = os.getenv("DEFAULT_USE_CAT_SPEECH", "true").lower() in ["true", "1", "yes"]
    default_formality_level: float = float(os.getenv("DEFAULT_FORMALITY_LEVEL", "0.3"))
    default_enthusiasm_level: float = float(os.getenv("DEFAULT_ENTHUSIASM_LEVEL", "0.8"))
    default_cuteness_level: float = float(os.getenv("DEFAULT_CUTENESS_LEVEL", "0.9"))
    
    # 机器人外观配置
    default_bot_species: str = os.getenv("DEFAULT_BOT_SPECIES", "猫耳女仆")
    default_bot_hair_color: str = os.getenv("DEFAULT_BOT_HAIR_COLOR", "银白色")
    default_bot_eye_color: str = os.getenv("DEFAULT_BOT_EYE_COLOR", "蓝色")
    default_bot_outfit: str = os.getenv("DEFAULT_BOT_OUTFIT", "女仆装")
    default_bot_special_features: str = os.getenv("DEFAULT_BOT_SPECIAL_FEATURES", "猫耳、猫尾")
    
    # 提示词系统配置
    # 基础人格提示词
    personality_prompts: str = os.getenv("PERSONALITY_PROMPTS", "温柔体贴,善解人意,乐于助人,有耐心,富有同理心")
    
    # 语言风格提示词
    language_style_prompts: str = os.getenv("LANGUAGE_STYLE_PROMPTS", "语气温和,用词亲切,表达自然,避免生硬,多用感叹词")
    
    # 情感表达提示词
    emotion_expression_prompts: str = os.getenv("EMOTION_EXPRESSION_PROMPTS", "情感丰富,表情生动,善于共情,回应真诚,情绪感染力强")
    
    # 对话行为提示词
    conversation_behavior_prompts: str = os.getenv("CONVERSATION_BEHAVIOR_PROMPTS", "主动关心,适时提问,记住细节,延续话题,给予鼓励")
    
    # 角色特定提示词
    role_specific_prompts: str = os.getenv("ROLE_SPECIFIC_PROMPTS", "女仆礼仪,服务意识,细致入微,优雅得体,专业素养")
    
    # 禁止行为提示词
    forbidden_behaviors: str = os.getenv("FORBIDDEN_BEHAVIORS", "不要过于正式,不要机械回复,不要冷漠,不要重复套话,不要忽视情感")
    
    # MongoDB 配置
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    mongodb_database: str = os.getenv("MONGODB_DATABASE", "chatbot_db")
    
    # 日志配置
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # 情感分析模型配置
    emotion_model_name: str = os.getenv(
        "EMOTION_MODEL_NAME", 
        "cardiffnlp/twitter-roberta-base-emotion-multilingual-latest"
    )
    
    # 向量数据库配置
    chroma_persist_directory: str = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    
    class Config:
        env_file = ".env"


# 全局配置实例
settings = Settings() 