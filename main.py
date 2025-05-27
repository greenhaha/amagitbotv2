"""
FastAPI 主应用
提供聊天机器人的Web API接口
"""
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Dict, Any

from core.chatbot import ChatbotCore, ChatRequest, ChatbotResponse
from core.logger import logger
from core.config import settings


# 全局聊天机器人实例
chatbot_core = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    global chatbot_core
    
    # 启动时初始化
    logger.info("正在启动聊天机器人系统...")
    try:
        chatbot_core = ChatbotCore()
        logger.info("聊天机器人系统启动成功")
        yield
    except Exception as e:
        logger.error(f"聊天机器人系统启动失败: {e}")
        raise
    finally:
        # 关闭时清理资源
        if chatbot_core:
            chatbot_core.close()
        logger.info("聊天机器人系统已关闭")


# 创建FastAPI应用
app = FastAPI(
    title="智能聊天机器人系统",
    description="支持情感分析、动态人格、记忆存储和知识学习的多功能聊天机器人",
    version="1.0.0",
    lifespan=lifespan
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "智能聊天机器人系统",
        "version": "1.0.0",
        "status": "running",
        "features": [
            "智能对话系统（LLM接入）",
            "实时思维系统（Chain of Thought）",
            "情感表达系统",
            "持久记忆系统（MongoDB）",
            "动态人格系统",
            "知识库学习系统（RAG）"
        ]
    }


@app.post("/chat", response_model=ChatbotResponse)
async def chat(request: ChatRequest) -> ChatbotResponse:
    """
    聊天接口
    
    处理用户消息并返回智能回复，包含：
    - LLM回复
    - 思维链步骤
    - 情感分析结果
    - 人格状态
    - 相关记忆
    - 知识库存储状态
    """
    try:
        if not chatbot_core:
            raise HTTPException(status_code=500, detail="聊天机器人系统未初始化")
        
        logger.info(f"收到聊天请求 - 用户: {request.user_id}, 消息: {request.message[:50]}...")
        
        # 处理聊天请求
        response = await chatbot_core.process_chat(request)
        
        logger.info(f"聊天请求处理完成 - 会话: {response.session_id}")
        return response
        
    except Exception as e:
        logger.error(f"聊天请求处理失败: {e}")
        raise HTTPException(status_code=500, detail=f"聊天处理失败: {str(e)}")


@app.get("/session/{user_id}/{session_id}/summary")
async def get_session_summary(user_id: str, session_id: str) -> Dict[str, Any]:
    """
    获取会话摘要
    
    返回会话的详细信息，包括：
    - 会话基本信息
    - 消息统计
    - 当前人格状态
    - 知识库统计
    """
    try:
        if not chatbot_core:
            raise HTTPException(status_code=500, detail="聊天机器人系统未初始化")
        
        summary = await chatbot_core.get_session_summary(user_id, session_id)
        
        if "error" in summary:
            raise HTTPException(status_code=404, detail=summary["error"])
        
        return summary
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取会话摘要失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取会话摘要失败: {str(e)}")


@app.post("/session/{user_id}/{session_id}/reset-persona")
async def reset_persona(
    user_id: str, 
    session_id: str, 
    personality_type: str = "gentle"
) -> Dict[str, Any]:
    """
    重置人格状态
    
    将指定会话的人格状态重置为指定类型
    """
    try:
        if not chatbot_core:
            raise HTTPException(status_code=500, detail="聊天机器人系统未初始化")
        
        success = await chatbot_core.reset_persona(user_id, session_id, personality_type)
        
        if success:
            return {
                "message": f"人格状态已重置为: {personality_type}",
                "user_id": user_id,
                "session_id": session_id,
                "new_personality": personality_type
            }
        else:
            raise HTTPException(status_code=400, detail="重置人格状态失败")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"重置人格状态失败: {e}")
        raise HTTPException(status_code=500, detail=f"重置人格状态失败: {str(e)}")


@app.get("/personalities")
async def get_available_personalities() -> Dict[str, Any]:
    """获取可用的人格类型列表"""
    try:
        if not chatbot_core:
            raise HTTPException(status_code=500, detail="聊天机器人系统未初始化")
        
        personalities = chatbot_core.get_available_personalities()
        
        return {
            "personalities": personalities,
            "descriptions": {
                "gentle": "温柔、耐心、富有同理心",
                "rational": "理性、逻辑性强",
                "humorous": "幽默、风趣",
                "outgoing": "外向、热情",
                "caring": "关怀、支持性强",
                "creative": "富有创造力、想象力",
                "analytical": "分析性强、注重细节",
                "empathetic": "高度共情、情感智能",
                "tsundere": "傲娇、表面高冷内心温柔、害羞否认"
            }
        }
        
    except Exception as e:
        logger.error(f"获取人格类型列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取人格类型列表失败: {str(e)}")


@app.get("/llm-providers")
async def get_available_llm_providers() -> Dict[str, Any]:
    """获取可用的LLM提供商列表"""
    try:
        if not chatbot_core:
            raise HTTPException(status_code=500, detail="聊天机器人系统未初始化")
        
        providers = chatbot_core.get_available_llm_providers()
        
        return {
            "providers": providers,
            "default": settings.default_llm_provider,
            "descriptions": {
                "deepseek": "DeepSeek API - 高质量的中文对话模型",
                "siliconflow": "SiliconFlow API - 多模型支持平台",
                "mock": "模拟LLM - 用于演示和测试，无需API密钥"
            }
        }
        
    except Exception as e:
        logger.error(f"获取LLM提供商列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取LLM提供商列表失败: {str(e)}")


@app.get("/models/{provider}")
async def get_available_models(provider: str) -> Dict[str, Any]:
    """获取指定提供商的可用模型列表"""
    try:
        from llm.factory import LLMFactory
        
        # 验证提供商是否可用
        available_providers = LLMFactory.get_available_providers()
        if provider not in available_providers:
            raise HTTPException(status_code=404, detail=f"提供商 {provider} 不可用")
        
        # 创建LLM实例并获取模型信息
        llm = LLMFactory.create_llm(provider)
        models = llm.get_available_models()
        
        # 如果是SiliconFlow，获取详细信息
        if provider == "siliconflow" and hasattr(llm, 'get_all_models_info'):
            models_info = llm.get_all_models_info()
            return {
                "provider": provider,
                "models": models,
                "models_info": models_info,
                "default_model": getattr(llm, 'default_model', models[0] if models else None)
            }
        else:
            return {
                "provider": provider,
                "models": models,
                "default_model": getattr(llm, 'default_model', models[0] if models else None)
            }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取模型列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取模型列表失败: {str(e)}")


@app.get("/models")
async def get_all_available_models() -> Dict[str, Any]:
    """获取所有提供商的可用模型列表"""
    try:
        from llm.factory import LLMFactory
        
        available_providers = LLMFactory.get_available_providers()
        all_models = {}
        
        for provider in available_providers:
            try:
                llm = LLMFactory.create_llm(provider)
                models = llm.get_available_models()
                
                if provider == "siliconflow" and hasattr(llm, 'get_all_models_info'):
                    models_info = llm.get_all_models_info()
                    all_models[provider] = {
                        "models": models,
                        "models_info": models_info,
                        "default_model": getattr(llm, 'default_model', models[0] if models else None)
                    }
                else:
                    all_models[provider] = {
                        "models": models,
                        "default_model": getattr(llm, 'default_model', models[0] if models else None)
                    }
            except Exception as e:
                logger.warning(f"获取 {provider} 模型列表失败: {e}")
                all_models[provider] = {"error": str(e)}
        
        return {
            "providers": available_providers,
            "models": all_models,
            "default_provider": settings.default_llm_provider
        }
        
    except Exception as e:
        logger.error(f"获取所有模型列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取所有模型列表失败: {str(e)}")


@app.get("/bot-profile/{user_id}")
async def get_bot_profile(user_id: str) -> Dict[str, Any]:
    """获取机器人档案"""
    try:
        if not chatbot_core:
            raise HTTPException(status_code=500, detail="聊天机器人系统未初始化")
        
        profile = await chatbot_core.get_bot_profile(user_id)
        
        if "error" in profile:
            raise HTTPException(status_code=404, detail=profile["error"])
        
        return profile
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取机器人档案失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取机器人档案失败: {str(e)}")


@app.put("/bot-profile/{user_id}")
async def update_bot_profile(user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """更新机器人档案"""
    try:
        if not chatbot_core:
            raise HTTPException(status_code=500, detail="聊天机器人系统未初始化")
        
        success = await chatbot_core.update_bot_profile(user_id, profile_data)
        
        if success:
            return {
                "message": "机器人档案更新成功",
                "user_id": user_id,
                "updated_fields": list(profile_data.keys())
            }
        else:
            raise HTTPException(status_code=400, detail="更新机器人档案失败")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新机器人档案失败: {e}")
        raise HTTPException(status_code=500, detail=f"更新机器人档案失败: {str(e)}")


@app.put("/bot-profile/{user_id}/name")
async def update_bot_name(user_id: str, name_data: Dict[str, str]) -> Dict[str, Any]:
    """更新机器人名字"""
    try:
        if not chatbot_core:
            raise HTTPException(status_code=500, detail="聊天机器人系统未初始化")
        
        new_name = name_data.get("bot_name")
        if not new_name:
            raise HTTPException(status_code=400, detail="缺少bot_name字段")
        
        success = await chatbot_core.update_bot_name(user_id, new_name)
        
        if success:
            return {
                "message": f"机器人名字已更新为: {new_name}",
                "user_id": user_id,
                "bot_name": new_name
            }
        else:
            raise HTTPException(status_code=400, detail="更新机器人名字失败")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新机器人名字失败: {e}")
        raise HTTPException(status_code=500, detail=f"更新机器人名字失败: {str(e)}")


@app.put("/bot-profile/{user_id}/personality")
async def update_bot_personality(user_id: str, personality_data: Dict[str, Any]) -> Dict[str, Any]:
    """更新机器人人格"""
    try:
        if not chatbot_core:
            raise HTTPException(status_code=500, detail="聊天机器人系统未初始化")
        
        personality_type = personality_data.get("personality_type")
        if not personality_type:
            raise HTTPException(status_code=400, detail="缺少personality_type字段")
        
        custom_traits = personality_data.get("custom_traits")
        
        success = await chatbot_core.update_bot_personality(
            user_id, personality_type, custom_traits
        )
        
        if success:
            return {
                "message": f"机器人人格已更新为: {personality_type}",
                "user_id": user_id,
                "personality_type": personality_type,
                "custom_traits": custom_traits
            }
        else:
            raise HTTPException(status_code=400, detail="更新机器人人格失败")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新机器人人格失败: {e}")
        raise HTTPException(status_code=500, detail=f"更新机器人人格失败: {str(e)}")


@app.put("/bot-profile/{user_id}/speaking-style")
async def update_bot_speaking_style(user_id: str, style_data: Dict[str, Any]) -> Dict[str, Any]:
    """更新机器人说话风格"""
    try:
        if not chatbot_core:
            raise HTTPException(status_code=500, detail="聊天机器人系统未初始化")
        
        speaking_style = style_data.get("speaking_style")
        if not speaking_style:
            raise HTTPException(status_code=400, detail="缺少speaking_style字段")
        
        success = await chatbot_core.update_bot_speaking_style(user_id, speaking_style)
        
        if success:
            return {
                "message": "机器人说话风格已更新",
                "user_id": user_id,
                "speaking_style": speaking_style
            }
        else:
            raise HTTPException(status_code=400, detail="更新机器人说话风格失败")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新机器人说话风格失败: {e}")
        raise HTTPException(status_code=500, detail=f"更新机器人说话风格失败: {str(e)}")


@app.get("/config")
async def get_environment_config() -> Dict[str, Any]:
    """获取环境配置信息"""
    try:
        return {
            "bot_config": {
                "default_bot_name": settings.default_bot_name,
                "default_bot_full_name": getattr(settings, 'default_bot_full_name', 'Luna TanCheng'),
                "default_bot_description": settings.default_bot_description,
                "default_bot_personality": settings.default_bot_personality,
                "default_bot_background": settings.default_bot_background,
                "default_bot_race": getattr(settings, 'default_bot_race', '猫族亚人'),
                "default_bot_age": getattr(settings, 'default_bot_age', '外貌16岁'),
                "default_bot_height": getattr(settings, 'default_bot_height', '152cm'),
                "default_bot_residence": getattr(settings, 'default_bot_residence', '银月庄园'),
                "default_bot_position": getattr(settings, 'default_bot_position', '高级侍女兼影之护卫'),
                "default_bot_special_ability": getattr(settings, 'default_bot_special_ability', '操控猫灵,银月血统,夜间视力,敏锐感知'),
            },
            "speaking_style_config": {
                "default_use_cat_speech": settings.default_use_cat_speech,
                "default_formality_level": settings.default_formality_level,
                "default_enthusiasm_level": settings.default_enthusiasm_level,
                "default_cuteness_level": settings.default_cuteness_level,
                "default_tsundere_level": getattr(settings, 'default_tsundere_level', 0.9),
                "default_pride_level": getattr(settings, 'default_pride_level', 0.8),
            },
            "appearance_config": {
                "default_bot_species": settings.default_bot_species,
                "default_bot_hair_color": settings.default_bot_hair_color,
                "default_bot_eye_color": settings.default_bot_eye_color,
                "default_bot_outfit": settings.default_bot_outfit,
                "default_bot_special_features": settings.default_bot_special_features
            },
            "preferences_config": {
                "default_bot_favorite_food": getattr(settings, 'default_bot_favorite_food', '鱼肉三明治,鲜奶'),
                "default_bot_hobbies": getattr(settings, 'default_bot_hobbies', '夜晚看星星,收集主人用过的茶杯'),
                "default_bot_dislikes": getattr(settings, 'default_bot_dislikes', '被摸耳朵和尾巴,被说可爱,寂寞'),
                "default_bot_fears": getattr(settings, 'default_bot_fears', '孤独,失去主人,暴露真实身份'),
            },
            "special_config": {
                "special_items": getattr(settings, 'special_items', '金色铃铛,灵魂链接器,猫灵召唤符,银月护符'),
                "special_abilities": getattr(settings, 'special_abilities', '猫灵操控,银月血统觉醒,夜间视力,危险感知,瞬间传送'),
                "hidden_background": getattr(settings, 'hidden_background', '前猫族祭司候补,逃离传统束缚,政治联姻象征,影之护卫身份,银月女王血统'),
                "relationship_dynamics": getattr(settings, 'relationship_dynamics', '主仆契约,暗中守护,傲娇关怀,灵魂链接,逐渐升温,政治背景'),
            },
            "llm_config": {
                "default_llm_provider": settings.default_llm_provider
            },
            "prompt_config": {
                "personality_prompts": settings.personality_prompts,
                "language_style_prompts": settings.language_style_prompts,
                "emotion_expression_prompts": settings.emotion_expression_prompts,
                "conversation_behavior_prompts": settings.conversation_behavior_prompts,
                "role_specific_prompts": settings.role_specific_prompts,
                "forbidden_behaviors": settings.forbidden_behaviors
            }
        }
        
    except Exception as e:
        logger.error(f"获取环境配置失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取环境配置失败: {str(e)}")


@app.get("/worldview/categories")
async def get_worldview_categories() -> Dict[str, Any]:
    """获取世界观类别信息"""
    try:
        from core.worldview_manager import worldview_manager
        
        return {
            "categories": worldview_manager.worldview_categories,
            "weights": worldview_manager.category_weights,
            "descriptions": {
                "background": "定义机器人所处的世界背景和环境设定",
                "values": "机器人坚持的核心价值观和信念",
                "social_rules": "机器人遵循的社会规则和行为准则",
                "culture": "影响机器人的文化背景和思维方式",
                "language_style": "机器人的语言表达风格和特色",
                "behavior_guidelines": "指导机器人行为的具体准则",
                "taboos": "机器人绝对避免的行为和话题"
            }
        }
        
    except Exception as e:
        logger.error(f"获取世界观类别信息失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取世界观类别信息失败: {str(e)}")


@app.get("/worldview/{user_id}")
async def get_worldview_summary(user_id: str) -> Dict[str, Any]:
    """获取用户的世界观摘要"""
    try:
        if not chatbot_core:
            raise HTTPException(status_code=500, detail="聊天机器人系统未初始化")
        
        summary = await chatbot_core.get_worldview_summary(user_id)
        
        if "error" in summary:
            raise HTTPException(status_code=404, detail=summary["error"])
        
        return summary
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取世界观摘要失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取世界观摘要失败: {str(e)}")


@app.put("/worldview/{user_id}/{category}")
async def update_worldview_category(
    user_id: str, 
    category: str, 
    worldview_data: Dict[str, Any]
) -> Dict[str, Any]:
    """更新特定类别的世界观关键词"""
    try:
        if not chatbot_core:
            raise HTTPException(status_code=500, detail="聊天机器人系统未初始化")
        
        keywords = worldview_data.get("keywords", [])
        weight = worldview_data.get("weight", 1.0)
        
        if not keywords:
            raise HTTPException(status_code=400, detail="关键词列表不能为空")
        
        # 验证类别是否有效
        valid_categories = [
            "background", "values", "social_rules", "culture", 
            "language_style", "behavior_guidelines", "taboos"
        ]
        if category not in valid_categories:
            raise HTTPException(
                status_code=400, 
                detail=f"无效的类别。有效类别: {', '.join(valid_categories)}"
            )
        
        success = await chatbot_core.update_worldview_category(
            user_id, category, keywords, weight
        )
        
        if success:
            return {
                "message": f"世界观类别 {category} 更新成功",
                "user_id": user_id,
                "category": category,
                "keywords": keywords,
                "weight": weight
            }
        else:
            raise HTTPException(status_code=400, detail="更新世界观类别失败")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新世界观类别失败: {e}")
        raise HTTPException(status_code=500, detail=f"更新世界观类别失败: {str(e)}")


@app.post("/worldview/{user_id}/reset")
async def reset_worldview(user_id: str) -> Dict[str, Any]:
    """重置用户的世界观设定为默认值"""
    try:
        if not chatbot_core:
            raise HTTPException(status_code=500, detail="聊天机器人系统未初始化")
        
        success = await chatbot_core.reset_worldview(user_id)
        
        if success:
            return {
                "message": "世界观设定已重置为默认值",
                "user_id": user_id
            }
        else:
            raise HTTPException(status_code=400, detail="重置世界观设定失败")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"重置世界观设定失败: {e}")
        raise HTTPException(status_code=500, detail=f"重置世界观设定失败: {str(e)}")


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """健康检查接口"""
    try:
        if not chatbot_core:
            return {"status": "unhealthy", "message": "聊天机器人系统未初始化"}
        
        # 可以添加更多健康检查逻辑
        return {
            "status": "healthy",
            "message": "聊天机器人系统运行正常",
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        return {"status": "unhealthy", "message": f"健康检查失败: {str(e)}"}


if __name__ == "__main__":
    # 运行应用
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.log_level.lower()
    ) 