"""
记忆管理器
负责管理对话记忆、会话状态和用户档案
"""
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from core.config import settings
from core.logger import logger
from .models import (
    ConversationSession, 
    ConversationMessage, 
    PersonaState, 
    MemorySummary, 
    UserProfile,
    BotProfile
)


class MemoryManager:
    """记忆管理器"""
    
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.mongodb_url)
        self.db = self.client[settings.mongodb_database]
        
        # 集合引用
        self.conversations = self.db.conversations
        self.summaries = self.db.summaries
        self.user_profiles = self.db.user_profiles
        self.bot_profiles = self.db.bot_profiles
        
        # 创建索引
        self._create_indexes()
        
        logger.info("记忆管理器初始化完成")
    
    def _create_indexes(self):
        """创建数据库索引"""
        try:
            # 对话会话索引
            self.conversations.create_index([("user_id", 1), ("session_id", 1)])
            self.conversations.create_index([("user_id", 1), ("created_at", -1)])
            self.conversations.create_index([("is_active", 1)])
            
            # 记忆摘要索引
            self.summaries.create_index([("user_id", 1), ("created_at", -1)])
            self.summaries.create_index([("importance_score", -1)])
            
            # 用户档案索引
            self.user_profiles.create_index([("user_id", 1)], unique=True)
            
            # 机器人档案索引
            self.bot_profiles.create_index([("user_id", 1)], unique=True)
            
            logger.info("数据库索引创建完成")
        except Exception as e:
            logger.error(f"创建数据库索引失败: {e}")
    
    async def create_session(self, user_id: str, initial_persona: PersonaState) -> str:
        """
        创建新的对话会话
        
        Args:
            user_id: 用户ID
            initial_persona: 初始人格状态
            
        Returns:
            str: 会话ID
        """
        session_id = str(uuid.uuid4())
        
        session = ConversationSession(
            user_id=user_id,
            session_id=session_id,
            persona_state=initial_persona
        )
        
        try:
            result = await self.conversations.insert_one(session.dict(by_alias=True))
            logger.info(f"创建新会话: {session_id}, 用户: {user_id}")
            return session_id
        except Exception as e:
            logger.error(f"创建会话失败: {e}")
            raise
    
    async def add_message(
        self, 
        user_id: str, 
        session_id: str, 
        message: ConversationMessage
    ) -> bool:
        """
        添加消息到会话
        
        Args:
            user_id: 用户ID
            session_id: 会话ID
            message: 消息对象
            
        Returns:
            bool: 是否成功
        """
        try:
            result = await self.conversations.update_one(
                {"user_id": user_id, "session_id": session_id},
                {
                    "$push": {"messages": message.dict()},
                    "$set": {"updated_at": datetime.now()}
                }
            )
            
            if result.modified_count > 0:
                logger.info(f"添加消息到会话 {session_id}")
                return True
            else:
                logger.warning(f"会话 {session_id} 不存在")
                return False
                
        except Exception as e:
            logger.error(f"添加消息失败: {e}")
            return False
    
    async def get_session(self, user_id: str, session_id: str) -> Optional[ConversationSession]:
        """
        获取会话信息
        
        Args:
            user_id: 用户ID
            session_id: 会话ID
            
        Returns:
            Optional[ConversationSession]: 会话对象
        """
        try:
            session_data = await self.conversations.find_one({
                "user_id": user_id,
                "session_id": session_id
            })
            
            if session_data:
                return ConversationSession(**session_data)
            return None
            
        except Exception as e:
            logger.error(f"获取会话失败: {e}")
            return None
    
    async def get_recent_messages(
        self, 
        user_id: str, 
        session_id: str, 
        limit: int = 10
    ) -> List[ConversationMessage]:
        """
        获取最近的消息
        
        Args:
            user_id: 用户ID
            session_id: 会话ID
            limit: 消息数量限制
            
        Returns:
            List[ConversationMessage]: 消息列表
        """
        try:
            session = await self.get_session(user_id, session_id)
            if session and session.messages:
                # 返回最近的消息
                recent_messages = session.messages[-limit:] if len(session.messages) > limit else session.messages
                return recent_messages
            return []
            
        except Exception as e:
            logger.error(f"获取最近消息失败: {e}")
            return []
    
    async def update_persona_state(
        self, 
        user_id: str, 
        session_id: str, 
        persona_state: PersonaState
    ) -> bool:
        """
        更新人格状态
        
        Args:
            user_id: 用户ID
            session_id: 会话ID
            persona_state: 新的人格状态
            
        Returns:
            bool: 是否成功
        """
        try:
            result = await self.conversations.update_one(
                {"user_id": user_id, "session_id": session_id},
                {
                    "$set": {
                        "persona_state": persona_state.dict(),
                        "updated_at": datetime.now()
                    }
                }
            )
            
            if result.modified_count > 0:
                logger.info(f"更新人格状态: {persona_state.personality_type}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"更新人格状态失败: {e}")
            return False
    
    async def create_memory_summary(
        self, 
        user_id: str, 
        session_id: str, 
        summary_text: str,
        key_topics: List[str] = None,
        emotional_tone: str = "neutral",
        importance_score: float = 0.5
    ) -> bool:
        """
        创建记忆摘要
        
        Args:
            user_id: 用户ID
            session_id: 会话ID
            summary_text: 摘要文本
            key_topics: 关键话题
            emotional_tone: 情感基调
            importance_score: 重要性评分
            
        Returns:
            bool: 是否成功
        """
        try:
            summary = MemorySummary(
                user_id=user_id,
                session_id=session_id,
                summary_text=summary_text,
                key_topics=key_topics or [],
                emotional_tone=emotional_tone,
                importance_score=importance_score
            )
            
            result = await self.summaries.insert_one(summary.dict(by_alias=True))
            logger.info(f"创建记忆摘要: {summary_text[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"创建记忆摘要失败: {e}")
            return False
    
    async def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """
        获取用户档案
        
        Args:
            user_id: 用户ID
            
        Returns:
            Optional[UserProfile]: 用户档案
        """
        try:
            profile_data = await self.user_profiles.find_one({"user_id": user_id})
            if profile_data:
                return UserProfile(**profile_data)
            return None
            
        except Exception as e:
            logger.error(f"获取用户档案失败: {e}")
            return None
    
    async def update_user_profile(self, user_profile: UserProfile) -> bool:
        """
        更新用户档案
        
        Args:
            user_profile: 用户档案对象
            
        Returns:
            bool: 是否成功
        """
        try:
            user_profile.updated_at = datetime.now()
            
            result = await self.user_profiles.update_one(
                {"user_id": user_profile.user_id},
                {"$set": user_profile.dict(by_alias=True, exclude={"id"})},
                upsert=True
            )
            
            logger.info(f"更新用户档案: {user_profile.user_id}")
            return True
            
        except Exception as e:
            logger.error(f"更新用户档案失败: {e}")
            return False
    
    async def get_conversation_context(
        self, 
        user_id: str, 
        session_id: str, 
        context_length: int = 5
    ) -> List[Dict[str, Any]]:
        """
        获取对话上下文
        
        Args:
            user_id: 用户ID
            session_id: 会话ID
            context_length: 上下文长度
            
        Returns:
            List[Dict[str, Any]]: 上下文消息列表
        """
        try:
            recent_messages = await self.get_recent_messages(user_id, session_id, context_length)
            
            context = []
            for msg in recent_messages:
                context.append({
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp,
                    "emotion": msg.emotion
                })
            
            return context
            
        except Exception as e:
            logger.error(f"获取对话上下文失败: {e}")
            return []
    
    async def get_bot_profile(self, user_id: str) -> Optional[BotProfile]:
        """
        获取机器人档案
        
        Args:
            user_id: 用户ID
            
        Returns:
            Optional[BotProfile]: 机器人档案
        """
        try:
            profile_data = await self.bot_profiles.find_one({"user_id": user_id})
            if profile_data:
                return BotProfile(**profile_data)
            
            # 如果没有找到，创建默认的天城档案
            default_profile = BotProfile(user_id=user_id)
            await self.update_bot_profile(default_profile)
            return default_profile
            
        except Exception as e:
            logger.error(f"获取机器人档案失败: {e}")
            return None
    
    async def update_bot_profile(self, bot_profile: BotProfile) -> bool:
        """
        更新机器人档案
        
        Args:
            bot_profile: 机器人档案对象
            
        Returns:
            bool: 是否成功
        """
        try:
            bot_profile.updated_at = datetime.now()
            
            result = await self.bot_profiles.update_one(
                {"user_id": bot_profile.user_id},
                {"$set": bot_profile.dict(by_alias=True, exclude={"id"})},
                upsert=True
            )
            
            logger.info(f"更新机器人档案: {bot_profile.bot_name} (用户: {bot_profile.user_id})")
            return True
            
        except Exception as e:
            logger.error(f"更新机器人档案失败: {e}")
            return False
    
    async def create_default_bot_profile(self, user_id: str) -> BotProfile:
        """
        创建默认的机器人档案
        
        Args:
            user_id: 用户ID
            
        Returns:
            BotProfile: 默认机器人档案
        """
        try:
            default_profile = BotProfile(user_id=user_id)
            await self.update_bot_profile(default_profile)
            logger.info(f"为用户 {user_id} 创建默认机器人档案: 天城")
            return default_profile
            
        except Exception as e:
            logger.error(f"创建默认机器人档案失败: {e}")
            raise
    
    async def update_bot_name(self, user_id: str, new_name: str) -> bool:
        """
        更新机器人名字
        
        Args:
            user_id: 用户ID
            new_name: 新名字
            
        Returns:
            bool: 是否成功
        """
        try:
            result = await self.bot_profiles.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "bot_name": new_name,
                        "updated_at": datetime.now()
                    }
                }
            )
            
            if result.modified_count > 0:
                logger.info(f"更新机器人名字为: {new_name} (用户: {user_id})")
                return True
            return False
            
        except Exception as e:
            logger.error(f"更新机器人名字失败: {e}")
            return False
    
    async def update_bot_personality(
        self, 
        user_id: str, 
        personality_type: str, 
        custom_traits: Dict[str, float] = None
    ) -> bool:
        """
        更新机器人人格
        
        Args:
            user_id: 用户ID
            personality_type: 人格类型
            custom_traits: 自定义特征
            
        Returns:
            bool: 是否成功
        """
        try:
            update_data = {
                "personality_type": personality_type,
                "updated_at": datetime.now()
            }
            
            if custom_traits:
                update_data["custom_traits"] = custom_traits
            
            result = await self.bot_profiles.update_one(
                {"user_id": user_id},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                logger.info(f"更新机器人人格为: {personality_type} (用户: {user_id})")
                return True
            return False
            
        except Exception as e:
            logger.error(f"更新机器人人格失败: {e}")
            return False
    
    async def update_bot_speaking_style(
        self, 
        user_id: str, 
        speaking_style: Dict[str, Any]
    ) -> bool:
        """
        更新机器人说话风格
        
        Args:
            user_id: 用户ID
            speaking_style: 说话风格配置
            
        Returns:
            bool: 是否成功
        """
        try:
            result = await self.bot_profiles.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "speaking_style": speaking_style,
                        "updated_at": datetime.now()
                    }
                }
            )
            
            if result.modified_count > 0:
                logger.info(f"更新机器人说话风格 (用户: {user_id})")
                return True
            return False
            
        except Exception as e:
            logger.error(f"更新机器人说话风格失败: {e}")
            return False

    def close(self):
        """关闭数据库连接"""
        if self.client:
            self.client.close()
            logger.info("MongoDB连接已关闭") 