#!/usr/bin/env python3
"""
控制台聊天演示脚本
自动演示控制台聊天的各种功能
"""
import requests
import time
import json

BASE_URL = "http://localhost:8000"

def check_server():
    """检查服务器状态"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def send_chat_message(message, user_id="demo_user", personality="gentle"):
    """发送聊天消息"""
    url = f"{BASE_URL}/chat"
    payload = {
        "message": message,
        "user_id": user_id,
        "personality_type": personality,
        "enable_thinking": True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ 请求失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

def display_chat_result(message, result, personality):
    """显示聊天结果"""
    print(f"\n{'='*60}")
    print(f"🎭 人格类型: {personality}")
    print(f"👤 用户: {message}")
    print("-" * 60)
    
    if result:
        print(f"🤖 机器人: {result['response']}")
        
        # 情感分析
        emotion = result.get('emotion_analysis', {})
        if emotion:
            print(f"😊 情感分析: {emotion.get('emotion', 'unknown')} "
                  f"(置信度: {emotion.get('confidence', 0):.2f}) {emotion.get('emoji', '')}")
        
        # 人格状态
        persona = result.get('persona_state', {})
        if persona:
            print(f"🎭 人格状态: {persona.get('personality_type', 'unknown')} | "
                  f"情绪: {persona.get('mood', 'unknown')} | "
                  f"能量: {persona.get('energy_level', 0):.1f}")
        
        # 思维过程
        thinking = result.get('thinking_process', [])
        if thinking:
            print("🧠 思维过程:")
            for i, step in enumerate(thinking, 1):
                print(f"   {i}. {step}")
        
        # 其他信息
        memories = result.get('relevant_memories', [])
        if memories:
            print(f"💭 相关记忆: {len(memories)} 条")
        
        kb_action = result.get('knowledge_base_action', '')
        if kb_action:
            print(f"📚 知识库: {kb_action}")
    else:
        print("❌ 无法获取回复")

def demo_console_chat():
    """演示控制台聊天功能"""
    print("🚀 控制台聊天机器人演示")
    print("=" * 60)
    
    # 检查服务器
    if not check_server():
        print("❌ 服务器未运行，请先启动: python3 main.py")
        return
    
    print("✅ 服务器连接正常")
    
    # 演示不同人格的对话
    demo_conversations = [
        {
            "personality": "gentle",
            "messages": [
                "你好！我今天心情很好",
                "我有点担心明天的考试"
            ]
        },
        {
            "personality": "humorous", 
            "messages": [
                "讲个笑话给我听",
                "我今天工作很累"
            ]
        },
        {
            "personality": "analytical",
            "messages": [
                "如何提高学习效率？",
                "Python和Java有什么区别？"
            ]
        },
        {
            "personality": "empathetic",
            "messages": [
                "我最近压力很大",
                "感觉有点孤独"
            ]
        }
    ]
    
    print("\n🎬 开始演示不同人格的对话效果...")
    
    for demo in demo_conversations:
        personality = demo["personality"]
        messages = demo["messages"]
        
        print(f"\n🎭 === {personality.upper()} 人格演示 ===")
        
        for message in messages:
            result = send_chat_message(message, "demo_user", personality)
            display_chat_result(message, result, personality)
            time.sleep(2)  # 稍作停顿
    
    print(f"\n{'='*60}")
    print("✅ 演示完成！")
    print("\n💡 要体验完整的控制台聊天功能，请运行:")
    print("   python3 console_chat.py")
    print("\n📖 查看详细使用指南:")
    print("   cat CONSOLE_CHAT_README.md")

if __name__ == "__main__":
    demo_console_chat() 