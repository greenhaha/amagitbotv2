"""
露娜·天城角色设定演示脚本
展示新的角色配置和傲娇人格功能
"""
import asyncio
import json
import requests
from typing import Dict, Any


class LunaCharacterDemo:
    """露娜·天城角色演示器"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_user_id = "luna_demo_user"
    
    def test_api_endpoint(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """测试API端点"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url)
            elif method.upper() == "POST":
                response = requests.post(url, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API请求失败: {e}")
            return {"error": str(e)}
    
    def demo_character_configuration(self):
        """演示角色配置"""
        print("🌟 露娜·天城 角色配置演示")
        print("=" * 50)
        
        # 1. 获取环境配置
        print("\n1. 获取环境配置信息:")
        config = self.test_api_endpoint("GET", "/config")
        
        if "error" not in config:
            bot_config = config.get("bot_config", {})
            print(f"   机器人名字: {bot_config.get('default_bot_name')}")
            print(f"   机器人描述: {bot_config.get('default_bot_description')}")
            print(f"   默认人格: {bot_config.get('default_bot_personality')}")
            print(f"   背景故事: {bot_config.get('default_bot_background')[:50]}...")
            
            appearance_config = config.get("appearance_config", {})
            print(f"   种族: {appearance_config.get('default_bot_species')}")
            print(f"   发色: {appearance_config.get('default_bot_hair_color')}")
            print(f"   眼色: {appearance_config.get('default_bot_eye_color')}")
            print(f"   特殊特征: {appearance_config.get('default_bot_special_features')}")
        
        # 2. 获取机器人档案
        print("\n2. 获取机器人档案:")
        profile = self.test_api_endpoint("GET", f"/bot-profile/{self.test_user_id}")
        
        if "error" not in profile:
            print(f"   机器人名字: {profile.get('bot_name')}")
            print(f"   人格类型: {profile.get('personality_type')}")
            print(f"   说话风格: {profile.get('speaking_style')}")
            print(f"   外观设定: {profile.get('appearance')}")
            print(f"   偏好设定: {profile.get('preferences')}")
    
    def demo_personality_types(self):
        """演示人格类型"""
        print("\n🎭 人格类型演示")
        print("=" * 50)
        
        personalities = self.test_api_endpoint("GET", "/personalities")
        
        if "error" not in personalities:
            print("可用的人格类型:")
            for personality, description in personalities.get("descriptions", {}).items():
                print(f"   {personality}: {description}")
                
            # 检查是否包含傲娇类型
            if "tsundere" in personalities.get("personalities", []):
                print("\n✅ 傲娇人格类型已成功添加!")
            else:
                print("\n❌ 傲娇人格类型未找到")
    
    def demo_worldview_settings(self):
        """演示世界观设定"""
        print("\n🌌 世界观设定演示")
        print("=" * 50)
        
        # 1. 获取世界观类别
        categories = self.test_api_endpoint("GET", "/worldview/categories")
        
        if "error" not in categories:
            print("世界观类别:")
            for category, description in categories.get("descriptions", {}).items():
                print(f"   {category}: {description}")
        
        # 2. 获取用户世界观摘要
        print("\n用户世界观摘要:")
        summary = self.test_api_endpoint("GET", f"/worldview/{self.test_user_id}")
        
        if "error" not in summary:
            print(f"   总类别数: {summary.get('total_categories')}")
            print(f"   总关键词数: {summary.get('total_keywords')}")
            
            # 显示部分类别内容
            categories_data = summary.get("categories", {})
            for category in ["background", "values", "culture"]:
                if category in categories_data:
                    cat_data = categories_data[category]
                    print(f"   {category}: {cat_data.get('keywords', [])[:3]}...")
    
    def demo_chat_with_luna(self):
        """演示与露娜的对话"""
        print("\n💬 与露娜·天城对话演示")
        print("=" * 50)
        
        test_messages = [
            "你好，露娜",
            "你今天心情怎么样？",
            "我想了解一下你的工作",
            "你会保护我吗？",
            "谢谢你一直陪伴着我"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n{i}. 用户: {message}")
            
            chat_data = {
                "message": message,
                "user_id": self.test_user_id,
                "llm_provider": "mock",
                "personality_type": "tsundere"
            }
            
            response = self.test_api_endpoint("POST", "/chat", chat_data)
            
            if "error" not in response:
                print(f"   露娜: {response.get('response')}")
                
                # 显示情感分析
                emotion = response.get('emotion_analysis', {})
                print(f"   情感: {emotion.get('emotion')} ({emotion.get('confidence', 0):.2f})")
                
                # 显示人格状态
                persona = response.get('persona_state', {})
                print(f"   人格: {persona.get('personality_type')}, 情绪: {persona.get('mood')}")
                
                # 显示思维过程（如果有）
                thinking = response.get('thinking_process', [])
                if thinking:
                    print(f"   思维: {thinking[0] if thinking else '无'}")
            else:
                print(f"   ❌ 对话失败: {response['error']}")
    
    def demo_character_customization(self):
        """演示角色自定义"""
        print("\n🎨 角色自定义演示")
        print("=" * 50)
        
        # 1. 更新机器人名字
        print("\n1. 更新机器人名字:")
        name_data = {"bot_name": "露娜·天城"}
        result = self.test_api_endpoint("PUT", f"/bot-profile/{self.test_user_id}/name", name_data)
        
        if "error" not in result:
            print(f"   ✅ 名字更新成功: {result.get('bot_name')}")
        
        # 2. 更新人格类型
        print("\n2. 更新人格类型:")
        personality_data = {
            "personality_type": "tsundere",
            "custom_traits": {
                "pride": 0.9,
                "shyness": 0.8,
                "caring": 0.8
            }
        }
        result = self.test_api_endpoint("PUT", f"/bot-profile/{self.test_user_id}/personality", personality_data)
        
        if "error" not in result:
            print(f"   ✅ 人格更新成功: {result.get('personality_type')}")
        
        # 3. 更新说话风格
        print("\n3. 更新说话风格:")
        style_data = {
            "speaking_style": {
                "use_cat_speech": True,
                "formality_level": 0.6,
                "enthusiasm_level": 0.4,
                "cuteness_level": 0.8,
                "tsundere_level": 0.9,
                "pride_level": 0.8
            }
        }
        result = self.test_api_endpoint("PUT", f"/bot-profile/{self.test_user_id}/speaking-style", style_data)
        
        if "error" not in result:
            print("   ✅ 说话风格更新成功")
    
    def demo_special_features(self):
        """演示特殊功能"""
        print("\n✨ 特殊功能演示")
        print("=" * 50)
        
        # 1. 重置人格状态
        print("\n1. 重置人格状态:")
        result = self.test_api_endpoint("POST", f"/session/{self.test_user_id}/test_session/reset-persona?personality_type=tsundere")
        
        if "error" not in result:
            print(f"   ✅ 人格重置成功: {result.get('new_personality')}")
        
        # 2. 获取会话摘要
        print("\n2. 获取会话摘要:")
        summary = self.test_api_endpoint("GET", f"/session/{self.test_user_id}/test_session/summary")
        
        if "error" not in summary:
            print(f"   会话ID: {summary.get('session_id')}")
            print(f"   消息数量: {summary.get('message_count')}")
            print(f"   当前人格: {summary.get('current_persona', {}).get('personality_type')}")
    
    def run_full_demo(self):
        """运行完整演示"""
        print("🚀 露娜·天城角色设定完整演示")
        print("=" * 60)
        
        demos = [
            ("角色配置", self.demo_character_configuration),
            ("人格类型", self.demo_personality_types),
            ("世界观设定", self.demo_worldview_settings),
            ("对话演示", self.demo_chat_with_luna),
            ("角色自定义", self.demo_character_customization),
            ("特殊功能", self.demo_special_features)
        ]
        
        for demo_name, demo_func in demos:
            try:
                demo_func()
            except Exception as e:
                print(f"\n❌ {demo_name} 演示失败: {e}")
        
        print("\n" + "=" * 60)
        print("🎉 露娜·天城角色设定演示完成!")
        print("✨ 傲娇猫耳女仆已准备就绪，随时为您服务喵～")


def main():
    """主函数"""
    print("🌙 露娜·天城角色设定演示")
    print("Luna TanCheng Character Configuration Demo")
    
    # 创建演示器并运行
    demo = LunaCharacterDemo()
    demo.run_full_demo()


if __name__ == "__main__":
    main() 