"""
记忆数据模型
定义MongoDB中存储的数据结构
"""
from datetime import datetime
from typing import List, Dict, Any, Optional, Annotated
from pydantic import BaseModel, Field, BeforeValidator
from bson import ObjectId
from core.config import settings


def validate_object_id(v):
    """验证ObjectId"""
    if isinstance(v, ObjectId):
        return v
    if isinstance(v, str) and ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[ObjectId, BeforeValidator(validate_object_id)]


class ConversationMessage(BaseModel):
    """对话消息模型"""
    role: str  # user, assistant, system
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    emotion: Optional[str] = None
    emotion_confidence: Optional[float] = None


class PersonaState(BaseModel):
    """人格状态模型"""
    personality_type: str  # gentle, rational, humorous, outgoing, etc.
    traits: Dict[str, float]  # 人格特征权重
    mood: str  # current mood
    energy_level: float = 1.0  # 0.0 - 1.0
    last_updated: datetime = Field(default_factory=datetime.now)


class ConversationSession(BaseModel):
    """对话会话模型"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    session_id: str
    messages: List[ConversationMessage] = []
    persona_state: PersonaState
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class MemorySummary(BaseModel):
    """记忆摘要模型"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    session_id: str
    summary_text: str
    key_topics: List[str] = []
    emotional_tone: str
    importance_score: float = 0.0  # 0.0 - 1.0
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserProfile(BaseModel):
    """用户档案模型"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    name: Optional[str] = None
    preferences: Dict[str, Any] = {}
    personality_insights: Dict[str, float] = {}  # 从对话中学习到的用户性格特征
    interaction_history: Dict[str, Any] = {}  # 交互历史统计
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


def get_default_speaking_style():
    """获取默认说话风格配置"""
    return {
        "use_cat_speech": settings.default_use_cat_speech,
        "formality_level": settings.default_formality_level,
        "enthusiasm_level": settings.default_enthusiasm_level,
        "cuteness_level": settings.default_cuteness_level,
    }

def get_default_appearance():
    """获取默认外观配置"""
    return {
        "species": settings.default_bot_species,
        "hair_color": settings.default_bot_hair_color,
        "eye_color": settings.default_bot_eye_color,
        "outfit": settings.default_bot_outfit,
        "special_features": settings.default_bot_special_features
    }

def get_default_preferences():
    """获取默认偏好配置"""
    return {
        "favorite_activities": ["聊天", "帮助主人", "学习新知识"],
        "favorite_topics": ["日常生活", "科技", "文学", "美食"],
        "dislikes": ["被忽视", "无法帮助到别人"]
    }

class BotProfile(BaseModel):
    """机器人档案模型"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str  # 所属用户ID
    bot_name: str = Field(default_factory=lambda: settings.default_bot_name)  # 机器人名字
    bot_description: str = Field(default_factory=lambda: settings.default_bot_description)  # 机器人描述
    personality_type: str = Field(default_factory=lambda: settings.default_bot_personality)  # 基础人格类型
    custom_traits: Dict[str, float] = Field(default_factory=dict)  # 自定义人格特征
    speaking_style: Dict[str, Any] = Field(default_factory=get_default_speaking_style)  # 说话风格
    appearance: Dict[str, str] = Field(default_factory=get_default_appearance)  # 外观设定
    background_story: str = Field(default_factory=lambda: settings.default_bot_background)  # 背景故事
    preferences: Dict[str, Any] = Field(default_factory=get_default_preferences)  # 机器人偏好
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str} 