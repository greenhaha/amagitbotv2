#!/usr/bin/env python3
"""
控制台聊天机器人
支持直接在终端中与聊天机器人进行对话
"""
import requests
import json
import time
import os
import sys
from datetime import datetime

# API基础URL
BASE_URL = "http://localhost:8000"

class ConsoleChat:
    def __init__(self):
        self.user_id = "console_user"
        self.session_id = None
        self.current_personality = "gentle"
        self.current_provider = "siliconflow"  # 默认使用siliconflow
        self.current_model = None  # 使用默认模型
        self.enable_thinking = True
        self.conversation_count = 0
        
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """打印头部信息"""
        print("🤖" + "="*60 + "🤖")
        print("           智能聊天机器人 - 控制台版本")
        print("🤖" + "="*60 + "🤖")
        print(f"当前人格: {self.current_personality} | 思维链: {'开启' if self.enable_thinking else '关闭'}")
        print(f"LLM提供商: {self.current_provider} | 模型: {self.current_model or '默认'}")
        print(f"用户ID: {self.user_id} | 对话次数: {self.conversation_count}")
        if self.session_id:
            print(f"会话ID: {self.session_id[:8]}...")
        print("-" * 64)
    
    def print_help(self):
        """打印帮助信息"""
        print("\n📖 控制台聊天帮助:")
        print("  💬 直接输入消息进行对话")
        print("  🎭 /personality <类型> - 切换人格 (gentle/rational/humorous/outgoing/caring/creative/analytical/empathetic)")
        print("  🤖 /provider <提供商> - 切换LLM提供商 (deepseek/siliconflow)")
        print("  🔧 /model <模型名> - 切换模型（仅SiliconFlow支持）")
        print("  🧠 /thinking - 切换思维链显示")
        print("  🆔 /userid <ID> - 设置用户ID")
        print("  🔄 /reset - 重置会话")
        print("  📊 /status - 查看系统状态")
        print("  🎭 /personalities - 查看所有人格类型")
        print("  🤖 /providers - 查看所有LLM提供商")
        print("  🔧 /models - 查看所有可用模型")
        print("  🐱 /botname <名字> - 设置机器人名字")
        print("  🐾 /botinfo - 查看机器人档案")
        print("  🎨 /botstyle - 自定义机器人说话风格")
        print("  ⚙️ /config - 查看环境配置")
        print("  🔧 /test - 测试API连接")
        print("  🧹 /clear - 清屏")
        print("  ❓ /help - 显示此帮助")
        print("  🚪 /quit 或 /exit - 退出程序")
        print("-" * 64)
    
    def check_server(self):
        """检查服务器状态"""
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                return True
            else:
                print(f"❌ 服务器响应异常: {response.status_code}")
                return False
        except requests.exceptions.RequestException:
            print("❌ 无法连接到聊天机器人服务器")
            print("请确保服务器正在运行: python3 main.py")
            return False
    
    def send_message(self, message):
        """发送消息到聊天机器人"""
        url = f"{BASE_URL}/chat"
        
        payload = {
            "message": message,
            "user_id": self.user_id,
            "personality_type": self.current_personality,
            "llm_provider": self.current_provider,
            "enable_thinking": self.enable_thinking
        }
        
        if self.session_id:
            payload["session_id"] = self.session_id
            
        if self.current_model:
            payload["model"] = self.current_model
        
        # 尝试发送请求，如果失败则自动切换提供商重试
        providers_to_try = [self.current_provider]
        if self.current_provider == "deepseek":
            providers_to_try.append("siliconflow")
        elif self.current_provider == "siliconflow":
            providers_to_try.append("deepseek")
        
        for attempt, provider in enumerate(providers_to_try):
            try:
                if attempt == 0:
                    print("🤔 思考中...", end="", flush=True)
                else:
                    print(f"\r🔄 切换到 {provider} 重试...", end="", flush=True)
                
                payload["llm_provider"] = provider
                response = requests.post(url, json=payload, timeout=60)  # 增加超时时间
                print("\r" + " " * 30 + "\r", end="")  # 清除状态信息
                
                if response.status_code == 200:
                    result = response.json()
                    self.session_id = result.get('session_id')
                    self.conversation_count += 1
                    
                    # 如果切换了提供商，更新当前提供商
                    if attempt > 0:
                        self.current_provider = provider
                        self.current_model = None  # 重置模型选择
                        print(f"✅ 已自动切换到 {provider} 提供商")
                    
                    return result
                else:
                    error_detail = ""
                    try:
                        error_data = response.json()
                        error_detail = error_data.get('detail', response.text)
                    except:
                        error_detail = response.text
                    
                    if attempt == len(providers_to_try) - 1:  # 最后一次尝试
                        print(f"\r❌ 请求失败: {response.status_code}")
                        if "401" in str(response.status_code):
                            print("💡 提示: API密钥可能无效，请检查 .env 文件中的API密钥配置")
                        elif "timeout" in error_detail.lower():
                            print("💡 提示: 请求超时，可能是网络问题或模型响应较慢")
                        print(f"错误详情: {error_detail[:200]}...")
                        return None
                    
            except requests.exceptions.Timeout:
                if attempt == len(providers_to_try) - 1:
                    print("\r❌ 请求超时，请稍后重试")
                    print("💡 提示: 可以尝试切换LLM提供商或检查网络连接")
                    return None
            except requests.exceptions.RequestException as e:
                if attempt == len(providers_to_try) - 1:
                    print(f"\r❌ 网络错误: {e}")
                    return None
            except Exception as e:
                if attempt == len(providers_to_try) - 1:
                    print(f"\r❌ 处理错误: {e}")
                    return None
        
        return None
    
    def display_response(self, result):
        """显示机器人回复"""
        # 机器人回复
        print(f"🤖 {result['response']}")
        
        # 情感分析
        emotion = result.get('emotion_analysis', {})
        if emotion:
            print(f"😊 情感: {emotion.get('emotion', 'unknown')} "
                  f"({emotion.get('confidence', 0):.2f}) {emotion.get('emoji', '')}")
        
        # 人格状态
        persona = result.get('persona_state', {})
        if persona:
            print(f"🎭 状态: {persona.get('personality_type', 'unknown')} | "
                  f"情绪: {persona.get('mood', 'unknown')} | "
                  f"能量: {persona.get('energy_level', 0):.1f}")
        
        # 思维过程
        if self.enable_thinking and result.get('thinking_process'):
            print("🧠 思维过程:")
            for i, step in enumerate(result['thinking_process'], 1):
                print(f"   {i}. {step}")
        
        # 相关记忆
        memories = result.get('relevant_memories', [])
        if memories:
            print(f"💭 相关记忆: {len(memories)} 条")
        
        # 知识库操作
        kb_action = result.get('knowledge_base_action', '')
        if kb_action:
            print(f"📚 知识库: {kb_action}")
    
    def handle_command(self, command):
        """处理命令"""
        parts = command.split()
        cmd = parts[0].lower()
        
        if cmd in ['/quit', '/exit']:
            return False
        
        elif cmd == '/help':
            self.print_help()
        
        elif cmd == '/clear':
            self.clear_screen()
            self.print_header()
        
        elif cmd == '/thinking':
            self.enable_thinking = not self.enable_thinking
            status = "开启" if self.enable_thinking else "关闭"
            print(f"🧠 思维链显示已{status}")
        
        elif cmd == '/reset':
            self.session_id = None
            self.conversation_count = 0
            print("🔄 会话已重置")
        
        elif cmd == '/status':
            self.check_system_status()
        
        elif cmd == '/personalities':
            self.show_personalities()
        
        elif cmd == '/providers':
            self.show_providers()
        
        elif cmd == '/models':
            self.show_models()
        
        elif cmd == '/provider':
            if len(parts) > 1:
                new_provider = parts[1].lower()
                valid_providers = ['deepseek', 'siliconflow']
                if new_provider in valid_providers:
                    self.current_provider = new_provider
                    self.current_model = None  # 重置模型选择
                    print(f"🤖 已切换到 {new_provider} 提供商")
                else:
                    print(f"❌ 无效提供商。可用提供商: {', '.join(valid_providers)}")
            else:
                print("❌ 请指定提供商，例如: /provider siliconflow")
        
        elif cmd == '/model':
            if len(parts) > 1:
                new_model = ' '.join(parts[1:])  # 支持包含空格的模型名
                if self.current_provider == "siliconflow":
                    # 验证模型是否可用
                    available_models = self.get_available_models_for_provider("siliconflow")
                    if available_models and new_model in available_models:
                        self.current_model = new_model
                        print(f"🔧 已切换到模型: {new_model}")
                    else:
                        print(f"❌ 模型 {new_model} 不可用。使用 /models 查看可用模型")
                else:
                    print("❌ 只有SiliconFlow提供商支持模型切换")
            else:
                print("❌ 请指定模型名，例如: /model Qwen/Qwen2.5-14B-Instruct")
        
        elif cmd == '/personality':
            if len(parts) > 1:
                new_personality = parts[1].lower()
                valid_personalities = ['gentle', 'rational', 'humorous', 'outgoing', 
                                     'caring', 'creative', 'analytical', 'empathetic']
                if new_personality in valid_personalities:
                    self.current_personality = new_personality
                    print(f"🎭 已切换到 {new_personality} 人格")
                else:
                    print(f"❌ 无效人格类型。可用类型: {', '.join(valid_personalities)}")
            else:
                print("❌ 请指定人格类型，例如: /personality gentle")
        
        elif cmd == '/userid':
            if len(parts) > 1:
                self.user_id = parts[1]
                self.session_id = None  # 重置会话
                print(f"🆔 用户ID已设置为: {self.user_id}")
            else:
                print("❌ 请指定用户ID，例如: /userid my_user_123")
        
        elif cmd == '/botname':
            if len(parts) > 1:
                new_name = ' '.join(parts[1:])  # 支持包含空格的名字
                self.update_bot_name(new_name)
            else:
                print("❌ 请指定机器人名字，例如: /botname 小雪")
        
        elif cmd == '/botinfo':
            self.show_bot_info()
        
        elif cmd == '/botstyle':
            self.customize_bot_style()
        
        elif cmd == '/config':
            self.show_environment_config()
        
        elif cmd == '/test':
            self.test_api_connection()
        
        else:
            print(f"❌ 未知命令: {command}")
            print("输入 /help 查看可用命令")
        
        return True
    
    def check_system_status(self):
        """检查系统状态"""
        try:
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                info = response.json()
                print("✅ 系统状态: 正常运行")
                print(f"📦 版本: {info.get('version', 'unknown')}")
                print("🔧 功能特性:")
                for feature in info.get('features', []):
                    print(f"   • {feature}")
            else:
                print(f"❌ 系统状态异常: {response.status_code}")
        except Exception as e:
            print(f"❌ 无法获取系统状态: {e}")
    
    def show_personalities(self):
        """显示可用人格类型"""
        try:
            response = requests.get(f"{BASE_URL}/personalities")
            if response.status_code == 200:
                data = response.json()
                print("🎭 可用人格类型:")
                for personality in data.get('personalities', []):
                    description = data.get('descriptions', {}).get(personality, "")
                    current = " (当前)" if personality == self.current_personality else ""
                    print(f"   • {personality}: {description}{current}")
            else:
                print(f"❌ 获取人格类型失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 获取人格类型错误: {e}")
    
    def show_providers(self):
        """显示可用LLM提供商"""
        try:
            response = requests.get(f"{BASE_URL}/llm-providers")
            if response.status_code == 200:
                data = response.json()
                print("🤖 可用LLM提供商:")
                for provider in data.get('providers', []):
                    description = data.get('descriptions', {}).get(provider, "")
                    current = " (当前)" if provider == self.current_provider else ""
                    default = " (默认)" if provider == data.get('default') else ""
                    print(f"   • {provider}: {description}{current}{default}")
            else:
                print(f"❌ 获取提供商列表失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 获取提供商列表错误: {e}")
    
    def show_models(self):
        """显示可用模型"""
        try:
            response = requests.get(f"{BASE_URL}/models")
            if response.status_code == 200:
                data = response.json()
                print("🔧 可用模型:")
                
                for provider, model_info in data.get('models', {}).items():
                    if 'error' in model_info:
                        print(f"   {provider}: ❌ {model_info['error']}")
                        continue
                    
                    print(f"\n   📦 {provider}:")
                    models = model_info.get('models', [])
                    default_model = model_info.get('default_model')
                    
                    if provider == "siliconflow" and 'models_info' in model_info:
                        models_info = model_info['models_info']
                        for model in models[:5]:  # 只显示前5个模型
                            info = models_info.get(model, {})
                            name = info.get('name', model)
                            description = info.get('description', '')
                            current = " (当前)" if (provider == self.current_provider and model == self.current_model) else ""
                            default = " (默认)" if model == default_model else ""
                            print(f"     • {model}")
                            print(f"       {name}: {description}{current}{default}")
                        
                        if len(models) > 5:
                            print(f"     ... 还有 {len(models) - 5} 个模型")
                    else:
                        for model in models:
                            current = " (当前)" if (provider == self.current_provider and model == self.current_model) else ""
                            default = " (默认)" if model == default_model else ""
                            print(f"     • {model}{current}{default}")
            else:
                print(f"❌ 获取模型列表失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 获取模型列表错误: {e}")
    
    def get_available_models_for_provider(self, provider):
        """获取指定提供商的可用模型列表"""
        try:
            response = requests.get(f"{BASE_URL}/models/{provider}")
            if response.status_code == 200:
                data = response.json()
                return data.get('models', [])
            else:
                return []
        except Exception:
            return []
    
    def update_bot_name(self, new_name):
        """更新机器人名字"""
        try:
            response = requests.put(
                f"{BASE_URL}/bot-profile/{self.user_id}/name",
                json={"bot_name": new_name}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"🐱 {data['message']}")
            else:
                print(f"❌ 更新机器人名字失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 更新机器人名字错误: {e}")
    
    def show_bot_info(self):
        """显示机器人档案信息"""
        try:
            response = requests.get(f"{BASE_URL}/bot-profile/{self.user_id}")
            if response.status_code == 200:
                data = response.json()
                print("🐾 机器人档案信息:")
                print(f"   名字: {data.get('bot_name', '未知')}")
                print(f"   描述: {data.get('bot_description', '无')}")
                print(f"   人格类型: {data.get('personality_type', '未知')}")
                
                appearance = data.get('appearance', {})
                if appearance:
                    print("   外观:")
                    for key, value in appearance.items():
                        print(f"     {key}: {value}")
                
                speaking_style = data.get('speaking_style', {})
                if speaking_style:
                    print("   说话风格:")
                    for key, value in speaking_style.items():
                        if isinstance(value, bool):
                            value = "是" if value else "否"
                        elif isinstance(value, float):
                            value = f"{value:.1f}"
                        print(f"     {key}: {value}")
                
                preferences = data.get('preferences', {})
                if preferences:
                    print("   偏好:")
                    for key, value in preferences.items():
                        if isinstance(value, list):
                            value = "、".join(value)
                        print(f"     {key}: {value}")
                        
            else:
                print(f"❌ 获取机器人档案失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 获取机器人档案错误: {e}")
    
    def customize_bot_style(self):
        """自定义机器人说话风格"""
        print("🎨 自定义机器人说话风格:")
        print("请输入新的设置值 (直接回车保持当前值)")
        
        try:
            # 获取当前设置
            response = requests.get(f"{BASE_URL}/bot-profile/{self.user_id}")
            if response.status_code != 200:
                print("❌ 无法获取当前设置")
                return
            
            current_data = response.json()
            current_style = current_data.get('speaking_style', {})
            
            new_style = {}
            
            # 猫娘语气
            current_cat = current_style.get('use_cat_speech', True)
            cat_input = input(f"使用猫娘语气 (当前: {'是' if current_cat else '否'}) [y/n]: ").strip().lower()
            if cat_input:
                new_style['use_cat_speech'] = cat_input in ['y', 'yes', '是', '1', 'true']
            else:
                new_style['use_cat_speech'] = current_cat
            
            # 正式程度
            current_formality = current_style.get('formality_level', 0.3)
            formality_input = input(f"正式程度 (当前: {current_formality:.1f}) [0.0-1.0]: ").strip()
            if formality_input:
                try:
                    new_style['formality_level'] = max(0.0, min(1.0, float(formality_input)))
                except ValueError:
                    new_style['formality_level'] = current_formality
            else:
                new_style['formality_level'] = current_formality
            
            # 热情程度
            current_enthusiasm = current_style.get('enthusiasm_level', 0.8)
            enthusiasm_input = input(f"热情程度 (当前: {current_enthusiasm:.1f}) [0.0-1.0]: ").strip()
            if enthusiasm_input:
                try:
                    new_style['enthusiasm_level'] = max(0.0, min(1.0, float(enthusiasm_input)))
                except ValueError:
                    new_style['enthusiasm_level'] = current_enthusiasm
            else:
                new_style['enthusiasm_level'] = current_enthusiasm
            
            # 可爱程度
            current_cuteness = current_style.get('cuteness_level', 0.9)
            cuteness_input = input(f"可爱程度 (当前: {current_cuteness:.1f}) [0.0-1.0]: ").strip()
            if cuteness_input:
                try:
                    new_style['cuteness_level'] = max(0.0, min(1.0, float(cuteness_input)))
                except ValueError:
                    new_style['cuteness_level'] = current_cuteness
            else:
                new_style['cuteness_level'] = current_cuteness
            
            # 更新设置
            update_response = requests.put(
                f"{BASE_URL}/bot-profile/{self.user_id}/speaking-style",
                json={"speaking_style": new_style}
            )
            
            if update_response.status_code == 200:
                print("🎨 机器人说话风格已更新！")
            else:
                print(f"❌ 更新说话风格失败: {update_response.status_code}")
                
        except Exception as e:
            print(f"❌ 自定义说话风格错误: {e}")
    
    def show_environment_config(self):
        """显示环境配置信息"""
        try:
            response = requests.get(f"{BASE_URL}/config")
            if response.status_code == 200:
                data = response.json()
                print("⚙️ 当前环境配置:")
                
                # 机器人默认配置
                bot_config = data.get('bot_config', {})
                if bot_config:
                    print("  🤖 机器人默认配置:")
                    print(f"    名字: {bot_config.get('default_bot_name', '未设置')}")
                    print(f"    描述: {bot_config.get('default_bot_description', '未设置')}")
                    print(f"    人格: {bot_config.get('default_bot_personality', '未设置')}")
                    print(f"    背景: {bot_config.get('default_bot_background', '未设置')[:50]}...")
                
                # 说话风格配置
                style_config = data.get('speaking_style_config', {})
                if style_config:
                    print("  🗣️ 说话风格配置:")
                    print(f"    猫娘语气: {'是' if style_config.get('default_use_cat_speech') else '否'}")
                    print(f"    正式程度: {style_config.get('default_formality_level', 0):.1f}")
                    print(f"    热情程度: {style_config.get('default_enthusiasm_level', 0):.1f}")
                    print(f"    可爱程度: {style_config.get('default_cuteness_level', 0):.1f}")
                
                # 外观配置
                appearance_config = data.get('appearance_config', {})
                if appearance_config:
                    print("  👗 外观配置:")
                    print(f"    种族: {appearance_config.get('default_bot_species', '未设置')}")
                    print(f"    发色: {appearance_config.get('default_bot_hair_color', '未设置')}")
                    print(f"    眼色: {appearance_config.get('default_bot_eye_color', '未设置')}")
                    print(f"    服装: {appearance_config.get('default_bot_outfit', '未设置')}")
                    print(f"    特征: {appearance_config.get('default_bot_special_features', '未设置')}")
                
                # LLM配置
                llm_config = data.get('llm_config', {})
                if llm_config:
                    print("  🧠 LLM配置:")
                    print(f"    默认提供商: {llm_config.get('default_llm_provider', '未设置')}")
                
                print("\n💡 提示: 这些是环境变量中设置的默认值，会在创建新机器人档案时使用")
                print("💡 可以通过修改 .env 文件来更改这些默认值")
                
            else:
                print(f"❌ 获取环境配置失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 获取环境配置错误: {e}")
    
    def test_api_connection(self):
        """测试API连接"""
        print("🔧 测试API连接...")
        
        providers = ["deepseek", "siliconflow"]
        
        for provider in providers:
            print(f"\n📡 测试 {provider} 连接...")
            
            try:
                test_payload = {
                    "message": "测试连接",
                    "user_id": f"test_{provider}",
                    "llm_provider": provider,
                    "enable_thinking": False
                }
                
                response = requests.post(
                    f"{BASE_URL}/chat", 
                    json=test_payload, 
                    timeout=30
                )
                
                if response.status_code == 200:
                    print(f"✅ {provider} 连接正常")
                else:
                    error_detail = ""
                    try:
                        error_data = response.json()
                        error_detail = error_data.get('detail', response.text)
                    except:
                        error_detail = response.text
                    
                    print(f"❌ {provider} 连接失败: {response.status_code}")
                    if "401" in str(response.status_code):
                        print(f"   💡 API密钥可能无效")
                    elif "timeout" in error_detail.lower():
                        print(f"   💡 请求超时")
                    print(f"   详情: {error_detail[:100]}...")
                    
            except requests.exceptions.Timeout:
                print(f"❌ {provider} 连接超时")
            except requests.exceptions.RequestException as e:
                print(f"❌ {provider} 网络错误: {e}")
            except Exception as e:
                print(f"❌ {provider} 测试错误: {e}")
        
        print(f"\n💡 当前使用的提供商: {self.current_provider}")
        print("💡 如果某个提供商连接失败，系统会自动切换到可用的提供商")
    
    def run(self):
        """运行控制台聊天"""
        self.clear_screen()
        self.print_header()
        
        # 检查服务器连接
        if not self.check_server():
            print("\n请先启动聊天机器人服务器，然后重新运行此程序。")
            return
        
        print("✅ 服务器连接正常")
        print("\n💡 输入 /help 查看可用命令，输入 /quit 退出程序")
        print("🎯 开始聊天吧！")
        print("-" * 64)
        
        while True:
            try:
                # 获取用户输入
                user_input = input(f"\n👤 您: ").strip()
                
                if not user_input:
                    continue
                
                # 处理命令
                if user_input.startswith('/'):
                    if not self.handle_command(user_input):
                        break
                    continue
                
                # 发送消息
                result = self.send_message(user_input)
                if result:
                    print()  # 空行分隔
                    self.display_response(result)
                
            except KeyboardInterrupt:
                print("\n\n👋 再见！感谢使用聊天机器人！")
                break
            except EOFError:
                print("\n\n👋 再见！感谢使用聊天机器人！")
                break
            except Exception as e:
                print(f"\n❌ 发生错误: {e}")
                print("请重试或输入 /help 查看帮助")

def main():
    """主函数"""
    chat = ConsoleChat()
    chat.run()

if __name__ == "__main__":
    main() 