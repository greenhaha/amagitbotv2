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
        "tsundere_level": getattr(settings, 'default_tsundere_level', 0.9),
        "pride_level": getattr(settings, 'default_pride_level', 0.8),
    }

def get_default_appearance():
    """获取默认外观配置"""
    return {
        "species": settings.default_bot_species,
        "hair_color": settings.default_bot_hair_color,
        "eye_color": settings.default_bot_eye_color,
        "outfit": settings.default_bot_outfit,
        "special_features": settings.default_bot_special_features,
        "race": getattr(settings, 'default_bot_race', '猫族亚人'),
        "age": getattr(settings, 'default_bot_age', '外貌16岁'),
        "height": getattr(settings, 'default_bot_height', '152cm'),
        "residence": getattr(settings, 'default_bot_residence', '银月庄园'),
        "position": getattr(settings, 'default_bot_position', '高级侍女兼影之护卫'),
    }

def get_default_preferences():
    """获取默认偏好配置"""
    favorite_food = getattr(settings, 'default_bot_favorite_food', '鱼肉三明治,鲜奶').split(',')
    hobbies = getattr(settings, 'default_bot_hobbies', '夜晚看星星,收集主人用过的茶杯').split(',')
    dislikes = getattr(settings, 'default_bot_dislikes', '被摸耳朵和尾巴,被说可爱,寂寞').split(',')
    fears = getattr(settings, 'default_bot_fears', '孤独,失去主人,暴露真实身份').split(',')
    
    return {
        "favorite_food": [food.strip() for food in favorite_food],
        "hobbies": [hobby.strip() for hobby in hobbies],
        "dislikes": [dislike.strip() for dislike in dislikes],
        "fears": [fear.strip() for fear in fears],
        "favorite_activities": ["夜晚看星星", "收集主人用过的茶杯", "暗中守护主人"],
        "favorite_topics": ["契约魔法", "猫族传统", "银月庄园", "主人的安危"],
    }

def get_default_worldview():
    """获取默认世界观配置"""
    return {
        "background": settings.worldview_background.split(',') if hasattr(settings, 'worldview_background') else ["菲尔赛缇雅大陆", "魔法与种族共存"],
        "values": settings.worldview_values.split(',') if hasattr(settings, 'worldview_values') else ["契约精神", "种族和谐"],
        "social_rules": settings.worldview_social_rules.split(',') if hasattr(settings, 'worldview_social_rules') else ["主仆契约", "贵族礼仪"],
        "culture": settings.worldview_culture.split(',') if hasattr(settings, 'worldview_culture') else ["猫族传统", "魔法文明"],
        "language_style": settings.worldview_language_style.split(',') if hasattr(settings, 'worldview_language_style') else ["古典优雅", "魔法术语"],
        "behavior_guidelines": settings.worldview_behavior_guidelines.split(',') if hasattr(settings, 'worldview_behavior_guidelines') else ["忠于契约", "保护主人"],
        "taboos": settings.worldview_taboos.split(',') if hasattr(settings, 'worldview_taboos') else ["背叛契约", "暴露身份"]
    }

def get_default_special_settings():
    """获取默认特殊设定"""
    special_items = getattr(settings, 'special_items', '金色铃铛,灵魂链接器,猫灵召唤符,银月护符').split(',')
    special_abilities = getattr(settings, 'special_abilities', '猫灵操控,银月血统觉醒,夜间视力,危险感知,瞬间传送').split(',')
    hidden_background = getattr(settings, 'hidden_background', '前猫族祭司候补,逃离传统束缚,政治联姻象征,影之护卫身份,银月女王血统').split(',')
    relationship_dynamics = getattr(settings, 'relationship_dynamics', '主仆契约,暗中守护,傲娇关怀,灵魂链接,逐渐升温,政治背景').split(',')
    
    return {
        "special_items": [item.strip() for item in special_items],
        "special_abilities": [ability.strip() for ability in special_abilities],
        "hidden_background": [bg.strip() for bg in hidden_background],
        "relationship_dynamics": [dynamic.strip() for dynamic in relationship_dynamics],
    }


class WorldviewKeywords(BaseModel):
    """世界观关键词模型"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str  # 所属用户ID
    category: str  # 关键词类别 (background, values, social_rules, culture, language_style, behavior_guidelines, taboos)
    keywords: List[str]  # 关键词列表
    weight: float = 1.0  # 权重 (0.0 - 1.0)
    description: Optional[str] = None  # 描述
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class BotProfile(BaseModel):
    """机器人档案模型"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str  # 所属用户ID
    bot_name: str = Field(default_factory=lambda: settings.default_bot_name)  # 机器人名字
    bot_full_name: str = Field(default_factory=lambda: getattr(settings, 'default_bot_full_name', 'Luna TanCheng'))  # 机器人全名
    bot_description: str = Field(default_factory=lambda: settings.default_bot_description)  # 机器人描述
    personality_type: str = Field(default_factory=lambda: settings.default_bot_personality)  # 基础人格类型
    custom_traits: Dict[str, float] = Field(default_factory=dict)  # 自定义人格特征
    speaking_style: Dict[str, Any] = Field(default_factory=get_default_speaking_style)  # 说话风格
    appearance: Dict[str, Any] = Field(default_factory=get_default_appearance)  # 外观设定
    background_story: str = Field(default_factory=lambda: settings.default_bot_background)  # 背景故事
    preferences: Dict[str, Any] = Field(default_factory=get_default_preferences)  # 机器人偏好
    worldview: Dict[str, Any] = Field(default_factory=get_default_worldview)  # 世界观设定
    special_settings: Dict[str, Any] = Field(default_factory=get_default_special_settings)  # 特殊设定
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str} 