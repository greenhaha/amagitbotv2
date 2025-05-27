#!/usr/bin/env python3
"""
与露娜·天城聊天的简单控制台脚本
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_header():
    """打印标题"""
    print("=" * 60)
    print("🌙 与露娜·天城的对话 🌙")
    print("=" * 60)
    print("💡 输入 'quit' 或 'exit' 退出")
    print("💡 输入 'help' 查看帮助")
    print("💡 输入 'status' 查看系统状态")
    print("-" * 60)

def check_server():
    """检查服务器状态"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_bot_info():
    """获取机器人信息"""
    try:
        response = requests.get(f"{BASE_URL}/config", timeout=5)
        if response.status_code == 200:
            config = response.json()
            bot_config = config.get('bot_config', {})
            return {
                'name': bot_config.get('default_bot_name', '未知'),
                'personality': bot_config.get('default_bot_personality', '未知'),
                'description': bot_config.get('default_bot_description', '无描述')
            }
    except:
        pass
    return None

def send_message(message, user_id="luna_chat_user", session_id=None):
    """发送消息"""
    payload = {
        "message": message,
        "user_id": user_id,
        "llm_provider": "mock",  # 使用mock提供商确保稳定
        "enable_thinking": True
    }
    
    if session_id:
        payload["session_id"] = session_id
    
    try:
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            error_detail = ""
            try:
                error_data = response.json()
                error_detail = error_data.get('detail', response.text)
            except:
                error_detail = response.text
            return {"error": f"请求失败 ({response.status_code}): {error_detail}"}
    except requests.exceptions.Timeout:
        return {"error": "请求超时，请稍后重试"}
    except Exception as e:
        return {"error": f"网络错误: {e}"}

def display_response(result):
    """显示回复"""
    if "error" in result:
        print(f"❌ {result['error']}")
        return
    
    # 机器人回复
    print(f"🌙 露娜: {result['response']}")
    
    # 情感分析
    emotion = result.get('emotion_analysis', {})
    if emotion:
        print(f"💭 情感: {emotion.get('emotion', 'unknown')} "
              f"({emotion.get('confidence', 0):.2f}) {emotion.get('emoji', '')}")
    
    # 人格状态
    persona = result.get('persona_state', {})
    if persona:
        print(f"🎭 状态: {persona.get('personality_type', 'unknown')} | "
              f"情绪: {persona.get('mood', 'unknown')} | "
              f"能量: {persona.get('energy_level', 0):.1f}")
    
    # 思维过程
    if result.get('thinking_process'):
        print("🧠 思维过程:")
        for i, step in enumerate(result['thinking_process'], 1):
            print(f"   {i}. {step}")
    
    print("-" * 60)

def show_status():
    """显示系统状态"""
    print("\n📊 系统状态:")
    
    # 服务器状态
    if check_server():
        print("✅ 服务器: 运行正常")
    else:
        print("❌ 服务器: 无法连接")
        return
    
    # 机器人信息
    bot_info = get_bot_info()
    if bot_info:
        print(f"🤖 机器人: {bot_info['name']}")
        print(f"🎭 人格: {bot_info['personality']}")
        print(f"📝 描述: {bot_info['description'][:50]}...")
    else:
        print("❌ 无法获取机器人信息")
    
    # LLM提供商
    try:
        response = requests.get(f"{BASE_URL}/llm-providers", timeout=5)
        if response.status_code == 200:
            providers = response.json()
            print(f"🔧 LLM提供商: {providers.get('default', 'unknown')}")
        else:
            print("❌ 无法获取LLM提供商信息")
    except:
        print("❌ 无法获取LLM提供商信息")
    
    print("-" * 60)

def show_help():
    """显示帮助"""
    print("\n📖 帮助信息:")
    print("   quit/exit - 退出程序")
    print("   help - 显示此帮助")
    print("   status - 显示系统状态")
    print("   clear - 清屏")
    print("\n💡 聊天技巧:")
    print("   - 露娜是傲娇性格的猫族女仆")
    print("   - 可以询问她的背景、喜好、能力等")
    print("   - 她会用'喵'结尾，表现出傲娇特质")
    print("   - 试试问她关于银月庄园或魔法的事情")
    print("-" * 60)

def main():
    """主函数"""
    print_header()
    
    # 检查服务器
    if not check_server():
        print("❌ 无法连接到服务器，请确保服务器正在运行")
        print("💡 运行命令: python main.py")
        return
    
    # 显示机器人信息
    bot_info = get_bot_info()
    if bot_info:
        print(f"🤖 已连接到: {bot_info['name']}")
        print(f"🎭 人格类型: {bot_info['personality']}")
        print("-" * 60)
    
    session_id = None
    
    while True:
        try:
            user_input = input("👤 你: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit']:
                print("👋 再见！")
                break
            elif user_input.lower() == 'help':
                show_help()
                continue
            elif user_input.lower() == 'status':
                show_status()
                continue
            elif user_input.lower() == 'clear':
                print("\033[2J\033[H")  # 清屏
                print_header()
                continue
            
            # 发送消息
            print("🤔 思考中...", end="", flush=True)
            result = send_message(user_input, session_id=session_id)
            print("\r" + " " * 20 + "\r", end="")  # 清除状态信息
            
            # 更新会话ID
            if "session_id" in result:
                session_id = result["session_id"]
            
            # 显示回复
            display_response(result)
            
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")

if __name__ == "__main__":
    main() 