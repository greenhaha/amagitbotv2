#!/usr/bin/env python3
"""
重置机器人配置脚本
确保使用最新的环境变量设置
"""
import asyncio
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

BASE_URL = "http://localhost:8000"

async def reset_bot_config():
    """重置机器人配置"""
    print("🔄 开始重置机器人配置...")
    
    # 1. 检查服务器状态
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ 服务器未运行，请先启动服务器")
            return
        print("✅ 服务器运行正常")
    except Exception as e:
        print(f"❌ 无法连接到服务器: {e}")
        return
    
    # 2. 获取当前配置
    print("\n📋 当前配置:")
    try:
        response = requests.get(f"{BASE_URL}/config")
        if response.status_code == 200:
            config = response.json()
            bot_config = config.get('bot_config', {})
            print(f"   机器人名字: {bot_config.get('default_bot_name', 'N/A')}")
            print(f"   人格类型: {bot_config.get('default_bot_personality', 'N/A')}")
            print(f"   种族: {bot_config.get('default_bot_race', 'N/A')}")
        else:
            print(f"❌ 获取配置失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取配置错误: {e}")
    
    # 3. 获取LLM提供商信息
    print("\n🤖 LLM提供商配置:")
    try:
        response = requests.get(f"{BASE_URL}/llm-providers")
        if response.status_code == 200:
            providers = response.json()
            print(f"   默认提供商: {providers.get('default', 'N/A')}")
            print(f"   可用提供商: {providers.get('providers', [])}")
        else:
            print(f"❌ 获取提供商信息失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取提供商信息错误: {e}")
    
    # 4. 测试聊天功能（使用mock提供商）
    print("\n💬 测试聊天功能:")
    test_user = "config_test_user"
    
    try:
        # 使用mock提供商测试
        payload = {
            "message": "你好，请介绍一下自己",
            "user_id": test_user,
            "llm_provider": "mock"
        }
        
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ 聊天功能正常")
            print(f"   机器人回复: {result['response'][:100]}...")
            
            metadata = result.get('metadata', {})
            print(f"   实际机器人名字: {metadata.get('bot_name', 'N/A')}")
            print(f"   实际人格类型: {metadata.get('bot_personality', 'N/A')}")
            
            # 检查是否是露娜配置
            if "露娜" in metadata.get('bot_name', ''):
                print("✅ 露娜配置已生效")
            else:
                print("⚠️  露娜配置未生效，可能需要重新创建用户档案")
                
        else:
            error_detail = ""
            try:
                error_data = response.json()
                error_detail = error_data.get('detail', response.text)
            except:
                error_detail = response.text
            print(f"❌ 聊天测试失败: {response.status_code}")
            print(f"   错误详情: {error_detail}")
            
    except Exception as e:
        print(f"❌ 聊天测试错误: {e}")
    
    # 5. 测试SiliconFlow提供商
    print("\n🔧 测试SiliconFlow提供商:")
    try:
        payload = {
            "message": "简单测试",
            "user_id": test_user,
            "llm_provider": "siliconflow"
        }
        
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ SiliconFlow提供商正常")
            print(f"   回复: {result['response'][:100]}...")
        else:
            error_detail = ""
            try:
                error_data = response.json()
                error_detail = error_data.get('detail', response.text)
            except:
                error_detail = response.text
            print(f"❌ SiliconFlow测试失败: {response.status_code}")
            print(f"   错误详情: {error_detail}")
            print("💡 建议使用mock提供商进行测试")
            
    except Exception as e:
        print(f"❌ SiliconFlow测试错误: {e}")
        print("💡 建议使用mock提供商进行测试")
    
    # 6. 提供建议
    print("\n💡 配置建议:")
    print("   1. 如果要使用露娜角色，确保环境变量正确设置")
    print("   2. 如果API有问题，可以使用mock提供商进行测试")
    print("   3. 重启服务器可以确保环境变量正确加载")
    print("   4. 使用新的用户ID可以避免旧配置缓存问题")

if __name__ == "__main__":
    asyncio.run(reset_bot_config()) 