"""
聊天机器人演示脚本
展示完整的用户提问响应流程
"""
import asyncio
import json
from datetime import datetime
from core.chatbot import ChatbotCore, ChatRequest
from core.logger import logger


async def demo_chat_flow():
    """演示完整的聊天流程"""
    print("🤖 智能聊天机器人系统演示")
    print("=" * 50)
    
    # 初始化聊天机器人核心
    try:
        chatbot = ChatbotCore()
        print("✅ 聊天机器人系统初始化成功")
    except Exception as e:
        print(f"❌ 系统初始化失败: {e}")
        return
    
    # 演示对话场景
    demo_conversations = [
        {
            "message": "你好！我今天心情很好，想和你聊聊天",
            "user_id": "demo_user",
            "personality_type": "outgoing",
            "description": "积极情绪 + 外向人格"
        },
        {
            "message": "我最近工作压力很大，感觉有些焦虑",
            "user_id": "demo_user",
            "personality_type": "empathetic",
            "description": "负面情绪 + 共情人格"
        },
        {
            "message": "能帮我分析一下这个技术问题吗？",
            "user_id": "demo_user",
            "personality_type": "analytical",
            "description": "中性情绪 + 分析人格"
        }
    ]
    
    session_id = None
    
    for i, conv in enumerate(demo_conversations, 1):
        print(f"\n🎭 场景 {i}: {conv['description']}")
        print("-" * 30)
        
        # 创建聊天请求
        request = ChatRequest(
            message=conv["message"],
            user_id=conv["user_id"],
            session_id=session_id,
            personality_type=conv["personality_type"],
            enable_thinking=True
        )
        
        print(f"👤 用户: {request.message}")
        
        try:
            # 处理聊天请求
            response = await chatbot.process_chat(request)
            session_id = response.session_id  # 保持会话连续性
            
            # 展示响应结果
            print(f"🤖 机器人: {response.response}")
            
            # 展示思维过程
            if response.thinking_process:
                print("\n🧠 思维过程:")
                for step in response.thinking_process:
                    print(f"   • {step}")
            
            # 展示情感分析
            emotion = response.emotion_analysis
            print(f"\n😊 情感分析: {emotion['emotion']} (置信度: {emotion['confidence']:.2f}) {emotion['emoji']}")
            
            # 展示人格状态
            persona = response.persona_state
            print(f"🎭 人格状态: {persona['personality_type']} | 情绪: {persona['mood']} | 能量: {persona['energy_level']:.1f}")
            
            # 展示主要特征
            if persona['main_traits']:
                traits = ", ".join([f"{k}: {v:.1f}" for k, v in persona['main_traits'].items()])
                print(f"✨ 主要特征: {traits}")
            
            # 展示相关记忆
            if response.relevant_memories:
                print(f"💭 相关记忆: 找到 {len(response.relevant_memories)} 条相关记忆")
            
            print(f"📚 知识库: {response.knowledge_base_action}")
            
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            logger.error(f"演示聊天失败: {e}")
    
    # 展示会话摘要
    if session_id:
        print(f"\n📊 会话摘要")
        print("-" * 30)
        try:
            summary = await chatbot.get_session_summary("demo_user", session_id)
            print(f"会话ID: {summary['session_id']}")
            print(f"消息数量: {summary['message_count']}")
            print(f"当前人格: {summary['current_persona']['personality_type']}")
            print(f"当前情绪: {summary['current_persona']['mood']}")
            if summary.get('session_summary'):
                print(f"会话总结: {summary['session_summary']}")
        except Exception as e:
            print(f"获取会话摘要失败: {e}")
    
    # 清理资源
    chatbot.close()
    print("\n✅ 演示完成，系统已关闭")


async def demo_personality_switching():
    """演示人格切换功能"""
    print("\n🎭 人格切换演示")
    print("=" * 50)
    
    try:
        chatbot = ChatbotCore()
        
        # 获取可用人格类型
        personalities = chatbot.get_available_personalities()
        print(f"可用人格类型: {', '.join(personalities)}")
        
        # 演示同一消息在不同人格下的响应
        test_message = "我需要一些建议来解决这个问题"
        user_id = "personality_demo_user"
        
        for personality in personalities[:3]:  # 演示前3种人格
            print(f"\n🎭 {personality.upper()} 人格:")
            print("-" * 20)
            
            request = ChatRequest(
                message=test_message,
                user_id=user_id,
                personality_type=personality,
                enable_thinking=False
            )
            
            try:
                response = await chatbot.process_chat(request)
                print(f"回应: {response.response}")
                print(f"情绪: {response.persona_state['mood']}")
            except Exception as e:
                print(f"处理失败: {e}")
        
        chatbot.close()
        
    except Exception as e:
        print(f"人格切换演示失败: {e}")


def print_system_info():
    """打印系统信息"""
    print("🔧 系统信息")
    print("=" * 50)
    
    from core.config import settings
    
    print(f"默认LLM提供商: {settings.default_llm_provider}")
    print(f"MongoDB URL: {settings.mongodb_url}")
    print(f"MongoDB 数据库: {settings.mongodb_database}")
    print(f"日志级别: {settings.log_level}")
    print(f"ChromaDB 目录: {settings.chroma_persist_directory}")
    
    # 检查API密钥配置
    if settings.deepseek_api_key:
        print("✅ DeepSeek API Key 已配置")
    else:
        print("❌ DeepSeek API Key 未配置")
    
    if settings.siliconflow_api_key:
        print("✅ SiliconFlow API Key 已配置")
    else:
        print("❌ SiliconFlow API Key 未配置")


async def main():
    """主函数"""
    print("🚀 智能聊天机器人系统演示启动")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 打印系统信息
    print_system_info()
    
    # 运行主要演示
    await demo_chat_flow()
    
    # 运行人格切换演示
    await demo_personality_switching()
    
    print("\n🎉 所有演示完成！")
    print("\n💡 提示:")
    print("1. 启动 FastAPI 服务: python main.py")
    print("2. 访问 API 文档: http://localhost:8000/docs")
    print("3. 运行测试: pytest tests/")


if __name__ == "__main__":
    asyncio.run(main()) 