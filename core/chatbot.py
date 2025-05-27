"""
聊天机器人核心控制器
整合所有模块功能，提供统一的聊天接口
"""
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel

from core.logger import logger
from llm.factory import LLMFactory
from llm.base import ChatMessage, ChatResponse
from emotion.analyzer import EmotionAnalyzer, EmotionResult
from memory.manager import MemoryManager
from memory.models import ConversationMessage, PersonaState
from persona.manager import PersonaManager, PersonalityType
from rag.knowledge_base import KnowledgeBase


class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str
    user_id: str
    session_id: Optional[str] = None
    llm_provider: Optional[str] = None
    model: Optional[str] = None  # 指定使用的模型
    enable_thinking: bool = True
    personality_type: Optional[str] = None


class ChatbotResponse(BaseModel):
    """聊天机器人响应模型"""
    response: str
    session_id: str
    thinking_process: Optional[List[str]] = None
    emotion_analysis: Dict[str, Any]
    persona_state: Dict[str, Any]
    relevant_memories: List[Dict[str, Any]] = []
    knowledge_base_action: str = "stored"
    metadata: Dict[str, Any] = {}


class ChatbotCore:
    """聊天机器人核心控制器"""
    
    def __init__(self):
        # 初始化各个模块
        self.emotion_analyzer = EmotionAnalyzer()
        self.memory_manager = MemoryManager()
        self.persona_manager = PersonaManager()
        self.knowledge_base = KnowledgeBase()
        
        logger.info("聊天机器人核心控制器初始化完成")
    
    async def process_chat(self, request: ChatRequest) -> ChatbotResponse:
        """
        处理聊天请求
        
        Args:
            request: 聊天请求
            
        Returns:
            ChatbotResponse: 聊天响应
        """
        try:
            # 1. 情感分析
            emotion_result = self.emotion_analyzer.analyze_emotion(request.message)
            logger.info(f"情感分析完成: {emotion_result.emotion.value}")
            
            # 2. 获取或创建会话
            session_id = request.session_id or str(uuid.uuid4())
            session = await self.memory_manager.get_session(request.user_id, session_id)
            
            if not session:
                # 创建新会话
                personality_type = PersonalityType.GENTLE
                if request.personality_type:
                    try:
                        personality_type = PersonalityType(request.personality_type)
                    except ValueError:
                        logger.warning(f"无效的人格类型: {request.personality_type}")
                
                initial_persona = self.persona_manager.create_default_persona(personality_type)
                session_id = await self.memory_manager.create_session(request.user_id, initial_persona)
                session = await self.memory_manager.get_session(request.user_id, session_id)
            
            # 3. 根据情感调整人格状态
            current_persona = session.persona_state
            adjusted_persona = self.persona_manager.adjust_persona_by_emotion(
                current_persona, 
                emotion_result.emotion, 
                emotion_result.confidence
            )
            
            # 更新人格状态
            await self.memory_manager.update_persona_state(
                request.user_id, 
                session_id, 
                adjusted_persona
            )
            
            # 4. 获取相关记忆
            relevant_memories = self.knowledge_base.get_relevant_memories(
                request.message, 
                request.user_id, 
                n_results=3
            )
            
            # 5. 构建对话上下文
            conversation_context = await self.memory_manager.get_conversation_context(
                request.user_id, 
                session_id, 
                context_length=5
            )
            
            # 6. 获取机器人档案
            bot_profile = await self.memory_manager.get_bot_profile(request.user_id)
            if not bot_profile:
                bot_profile = await self.memory_manager.create_default_bot_profile(request.user_id)
            
            # 7. 生成个性化系统提示
            personality_prompt = self.persona_manager.get_bot_personality_prompt(adjusted_persona, bot_profile)
            
            # 构建记忆上下文
            memory_context = ""
            if relevant_memories:
                memory_context = "\n相关记忆:\n" + "\n".join([
                    f"- {memory['content'][:100]}..." 
                    for memory in relevant_memories[:2]
                ])
            
            system_prompt = f"""
{personality_prompt}

当前情绪状态: {adjusted_persona.mood}
能量水平: {adjusted_persona.energy_level:.1f}

用户情感分析: {emotion_result.description} {emotion_result.emoji}

{memory_context}

请根据你的角色设定、人格特征和当前状态，以及用户的情感状态，给出合适的回应。
"""
            
            # 8. 构建消息列表
            messages = [ChatMessage(role="system", content=system_prompt)]
            
            # 添加历史对话上下文
            for ctx in conversation_context[-3:]:  # 最近3轮对话
                messages.append(ChatMessage(
                    role=ctx["role"], 
                    content=ctx["content"]
                ))
            
            # 添加当前用户消息
            messages.append(ChatMessage(role="user", content=request.message))
            
            # 9. 调用LLM生成回复
            llm = LLMFactory.create_llm(request.llm_provider)
            llm_response = await llm.chat_completion(
                messages=messages,
                model=request.model,
                enable_thinking=request.enable_thinking,
                temperature=0.7
            )
            
            # 10. 保存对话到记忆系统
            user_message = ConversationMessage(
                role="user",
                content=request.message,
                emotion=emotion_result.emotion.value,
                emotion_confidence=emotion_result.confidence
            )
            
            assistant_message = ConversationMessage(
                role="assistant",
                content=llm_response.content
            )
            
            await self.memory_manager.add_message(request.user_id, session_id, user_message)
            await self.memory_manager.add_message(request.user_id, session_id, assistant_message)
            
            # 11. 添加到知识库
            emotion_info = {
                "emotion": emotion_result.emotion.value,
                "confidence": emotion_result.confidence
            }
            
            self.knowledge_base.add_conversation_turn(
                user_message=request.message,
                assistant_response=llm_response.content,
                user_id=request.user_id,
                session_id=session_id,
                emotion_info=emotion_info
            )
            
            # 12. 构建响应
            response = ChatbotResponse(
                response=f"{llm_response.content} {emotion_result.emoji}",
                session_id=session_id,
                thinking_process=llm_response.thinking_process,
                emotion_analysis={
                    "emotion": emotion_result.emotion.value,
                    "confidence": emotion_result.confidence,
                    "emoji": emotion_result.emoji,
                    "description": emotion_result.description
                },
                persona_state={
                    "personality_type": adjusted_persona.personality_type,
                    "mood": adjusted_persona.mood,
                    "energy_level": adjusted_persona.energy_level,
                    "main_traits": {
                        trait: value for trait, value in adjusted_persona.traits.items() 
                        if value > 0.6
                    }
                },
                relevant_memories=[
                    {
                        "content": memory["content"][:100] + "...",
                        "similarity": memory["similarity"]
                    }
                    for memory in relevant_memories
                ],
                knowledge_base_action="stored",
                metadata={
                    "llm_model": llm_response.model,
                    "llm_usage": llm_response.usage,
                    "processing_time": datetime.now().isoformat(),
                    "bot_name": bot_profile.bot_name,
                    "bot_personality": bot_profile.personality_type
                }
            )
            
            logger.info(f"聊天处理完成，会话ID: {session_id}")
            return response
            
        except Exception as e:
            logger.error(f"聊天处理失败: {e}")
            raise
    
    async def get_session_summary(self, user_id: str, session_id: str) -> Dict[str, Any]:
        """
        获取会话摘要
        
        Args:
            user_id: 用户ID
            session_id: 会话ID
            
        Returns:
            Dict[str, Any]: 会话摘要
        """
        try:
            session = await self.memory_manager.get_session(user_id, session_id)
            if not session:
                return {"error": "会话不存在"}
            
            # 获取知识库统计
            kb_stats = self.knowledge_base.get_collection_stats()
            
            # 生成会话总结
            session_summary = self.knowledge_base.summarize_session(user_id, session_id)
            
            return {
                "session_id": session_id,
                "user_id": user_id,
                "created_at": session.created_at.isoformat(),
                "updated_at": session.updated_at.isoformat(),
                "message_count": len(session.messages),
                "current_persona": {
                    "personality_type": session.persona_state.personality_type,
                    "mood": session.persona_state.mood,
                    "energy_level": session.persona_state.energy_level
                },
                "session_summary": session_summary,
                "knowledge_base_stats": kb_stats
            }
            
        except Exception as e:
            logger.error(f"获取会话摘要失败: {e}")
            return {"error": str(e)}
    
    async def reset_persona(
        self, 
        user_id: str, 
        session_id: str, 
        personality_type: str = "gentle"
    ) -> bool:
        """
        重置人格状态
        
        Args:
            user_id: 用户ID
            session_id: 会话ID
            personality_type: 新的人格类型
            
        Returns:
            bool: 是否成功
        """
        try:
            personality_enum = PersonalityType(personality_type)
            new_persona = self.persona_manager.create_default_persona(personality_enum)
            
            success = await self.memory_manager.update_persona_state(
                user_id, 
                session_id, 
                new_persona
            )
            
            if success:
                logger.info(f"人格状态已重置为: {personality_type}")
            
            return success
            
        except Exception as e:
            logger.error(f"重置人格状态失败: {e}")
            return False
    
    def get_available_personalities(self) -> List[str]:
        """获取可用的人格类型列表"""
        return [personality.value for personality in PersonalityType]
    
    def get_available_llm_providers(self) -> List[str]:
        """获取可用的LLM提供商列表"""
        return LLMFactory.get_available_providers()
    
    async def get_bot_profile(self, user_id: str) -> Dict[str, Any]:
        """
        获取机器人档案
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict[str, Any]: 机器人档案信息
        """
        try:
            bot_profile = await self.memory_manager.get_bot_profile(user_id)
            if not bot_profile:
                bot_profile = await self.memory_manager.create_default_bot_profile(user_id)
            
            return {
                "bot_name": bot_profile.bot_name,
                "bot_description": bot_profile.bot_description,
                "personality_type": bot_profile.personality_type,
                "speaking_style": bot_profile.speaking_style,
                "appearance": bot_profile.appearance,
                "background_story": bot_profile.background_story,
                "preferences": bot_profile.preferences,
                "created_at": bot_profile.created_at.isoformat(),
                "updated_at": bot_profile.updated_at.isoformat()
            }
            
        except Exception as e:
            logger.error(f"获取机器人档案失败: {e}")
            return {"error": str(e)}
    
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
            success = await self.memory_manager.update_bot_name(user_id, new_name)
            if success:
                logger.info(f"机器人名字已更新为: {new_name}")
            return success
            
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
            success = await self.memory_manager.update_bot_personality(
                user_id, personality_type, custom_traits
            )
            if success:
                logger.info(f"机器人人格已更新为: {personality_type}")
            return success
            
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
            success = await self.memory_manager.update_bot_speaking_style(
                user_id, speaking_style
            )
            if success:
                logger.info(f"机器人说话风格已更新")
            return success
            
        except Exception as e:
            logger.error(f"更新机器人说话风格失败: {e}")
            return False
    
    async def update_bot_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """
        更新机器人完整档案
        
        Args:
            user_id: 用户ID
            profile_data: 档案数据
            
        Returns:
            bool: 是否成功
        """
        try:
            # 获取现有档案
            bot_profile = await self.memory_manager.get_bot_profile(user_id)
            if not bot_profile:
                bot_profile = await self.memory_manager.create_default_bot_profile(user_id)
            
            # 更新字段
            if "bot_name" in profile_data:
                bot_profile.bot_name = profile_data["bot_name"]
            if "bot_description" in profile_data:
                bot_profile.bot_description = profile_data["bot_description"]
            if "personality_type" in profile_data:
                bot_profile.personality_type = profile_data["personality_type"]
            if "speaking_style" in profile_data:
                bot_profile.speaking_style.update(profile_data["speaking_style"])
            if "appearance" in profile_data:
                bot_profile.appearance.update(profile_data["appearance"])
            if "background_story" in profile_data:
                bot_profile.background_story = profile_data["background_story"]
            if "preferences" in profile_data:
                bot_profile.preferences.update(profile_data["preferences"])
            
            # 保存更新
            success = await self.memory_manager.update_bot_profile(bot_profile)
            if success:
                logger.info(f"机器人档案已更新")
            return success
            
        except Exception as e:
            logger.error(f"更新机器人档案失败: {e}")
            return False
    
    def close(self):
        """关闭资源"""
        self.memory_manager.close()
        logger.info("聊天机器人核心控制器已关闭") 