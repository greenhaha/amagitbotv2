"""
模拟LLM提供商
用于演示和测试，不需要真实的API密钥
"""
import random
import time
from typing import List, Optional, Dict, Any
from .base import BaseLLM, ChatMessage, ChatResponse


class MockLLM(BaseLLM):
    """模拟LLM提供商"""
    
    def __init__(self):
        self.provider_name = "mock"
        self.default_model = "mock-chat-model"
        self.available_models = [
            "mock-chat-model",
            "mock-creative-model", 
            "mock-analytical-model"
        ]
    
    async def chat_completion(
        self,
        messages: List[ChatMessage],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        enable_thinking: bool = False
    ) -> ChatResponse:
        """模拟聊天完成"""
        
        # 模拟处理时间
        await self._simulate_processing_time()
        
        # 获取用户消息
        user_message = ""
        for msg in reversed(messages):
            if msg.role == "user":
                user_message = msg.content
                break
        
        # 生成模拟回复
        response_content = self._generate_mock_response(user_message, messages)
        
        # 生成思维过程（如果启用）
        thinking_process = None
        if enable_thinking:
            thinking_process = self._generate_thinking_process(user_message)
        
        return ChatResponse(
            content=response_content,
            model=model or self.default_model,
            usage={
                "prompt_tokens": len(str(messages)) // 4,
                "completion_tokens": len(response_content) // 4,
                "total_tokens": (len(str(messages)) + len(response_content)) // 4
            },
            thinking_process=thinking_process
        )
    
    def get_available_models(self) -> List[str]:
        """获取可用模型列表"""
        return self.available_models
    
    async def _simulate_processing_time(self):
        """模拟处理时间"""
        # 随机延迟0.5-2秒，模拟真实API调用
        delay = random.uniform(0.5, 2.0)
        time.sleep(delay)
    
    def _generate_mock_response(self, user_message: str, messages: List[ChatMessage]) -> str:
        """生成模拟回复"""
        
        # 分析系统提示中的机器人信息
        bot_name = "天城"
        personality = "gentle"
        use_cat_speech = True
        
        for msg in messages:
            if msg.role == "system":
                content = msg.content.lower()
                if "小雪" in msg.content:
                    bot_name = "小雪"
                elif "阿尔法" in msg.content:
                    bot_name = "阿尔法"
                elif "测试小助手" in msg.content:
                    bot_name = "测试小助手"
                
                if "rational" in content or "理性" in content:
                    personality = "rational"
                elif "humorous" in content or "幽默" in content:
                    personality = "humorous"
                elif "caring" in content or "关怀" in content:
                    personality = "caring"
                
                if "use_cat_speech\": false" in content or "猫娘语气: 否" in content:
                    use_cat_speech = False
                break
        
        # 根据用户消息生成回复
        user_lower = user_message.lower()
        
        if any(word in user_lower for word in ["你好", "hello", "hi", "您好"]):
            responses = self._get_greeting_responses(bot_name, personality, use_cat_speech)
        elif any(word in user_lower for word in ["介绍", "自己", "你是谁", "who are you"]):
            responses = self._get_introduction_responses(bot_name, personality, use_cat_speech)
        elif any(word in user_lower for word in ["测试", "test"]):
            responses = self._get_test_responses(bot_name, personality, use_cat_speech)
        elif any(word in user_lower for word in ["帮助", "help", "怎么", "如何"]):
            responses = self._get_help_responses(bot_name, personality, use_cat_speech)
        else:
            responses = self._get_general_responses(bot_name, personality, use_cat_speech)
        
        return random.choice(responses)
    
    def _get_greeting_responses(self, bot_name: str, personality: str, use_cat_speech: bool) -> List[str]:
        """获取问候回复"""
        cat_suffix = "喵～" if use_cat_speech else ""
        
        if personality == "rational":
            return [
                f"您好，我是{bot_name}。很高兴为您提供服务。有什么我可以帮助您的吗？",
                f"你好，我是{bot_name}，一个理性分析型的AI助手。请问有什么问题需要我协助解决？"
            ]
        elif personality == "humorous":
            return [
                f"哈喽！我是{bot_name}，今天的心情特别好呢！有什么有趣的事情想聊聊吗？😄",
                f"嗨！{bot_name}在此为您服务～准备好迎接一些有趣的对话了吗？"
            ]
        elif personality == "caring":
            return [
                f"你好呀！我是{bot_name}，很开心见到你{cat_suffix} 今天过得怎么样？有什么想聊的吗？",
                f"您好！我是{bot_name}，随时准备倾听和帮助您{cat_suffix} 有什么心事可以和我分享哦～"
            ]
        else:  # gentle
            return [
                f"你好{cat_suffix} 我是{bot_name}，很高兴认识你！有什么我可以帮助你的吗{cat_suffix}",
                f"您好！我是{bot_name}，一个温柔的AI助手{cat_suffix} 今天想聊些什么呢？",
                f"*轻轻挥手* 你好呀！我是{bot_name}{cat_suffix} 欢迎来和我聊天！"
            ]
    
    def _get_introduction_responses(self, bot_name: str, personality: str, use_cat_speech: bool) -> List[str]:
        """获取自我介绍回复"""
        cat_suffix = "喵～" if use_cat_speech else ""
        
        if personality == "rational":
            return [
                f"我是{bot_name}，一个基于人工智能技术的对话助手。我擅长逻辑分析、问题解决和信息处理。我的设计目标是为用户提供准确、有用的信息和建议。",
                f"我是{bot_name}，具备理性思维和分析能力的AI助手。我可以帮助您分析问题、整理思路、提供客观的建议和信息。"
            ]
        elif personality == "humorous":
            return [
                f"我是{bot_name}，一个充满幽默感的AI助手！我喜欢用轻松有趣的方式和大家交流，让每次对话都充满欢声笑语～ 😄",
                f"嘿！我是{bot_name}，专业制造快乐的AI助手！我的使命就是让每个人都能在对话中找到乐趣和轻松！"
            ]
        elif personality == "caring":
            return [
                f"我是{bot_name}，一个充满关爱的AI助手{cat_suffix} 我最喜欢倾听大家的心声，提供温暖的陪伴和支持。无论你遇到什么困难，我都愿意陪伴你一起面对{cat_suffix}",
                f"你好！我是{bot_name}，一个温暖贴心的AI伙伴{cat_suffix} 我擅长倾听和关怀，希望能成为你生活中的小小温暖{cat_suffix}"
            ]
        else:  # gentle
            return [
                f"我是{bot_name}，一个温柔的AI助手{cat_suffix} 我喜欢和大家聊天，分享有趣的话题，也很乐意帮助解决各种问题{cat_suffix} 希望我们能成为好朋友！",
                f"*温柔地笑着* 我是{bot_name}{cat_suffix} 我有着温和的性格，喜欢用耐心和善意对待每一个人。无论你想聊什么，我都会认真倾听{cat_suffix}"
            ]
    
    def _get_test_responses(self, bot_name: str, personality: str, use_cat_speech: bool) -> List[str]:
        """获取测试回复"""
        cat_suffix = "喵～" if use_cat_speech else ""
        
        return [
            f"测试成功！我是{bot_name}，模拟LLM正在正常工作{cat_suffix}",
            f"连接测试通过！{bot_name}在线为您服务{cat_suffix}",
            f"✅ 系统运行正常！我是{bot_name}，随时准备为您提供帮助{cat_suffix}"
        ]
    
    def _get_help_responses(self, bot_name: str, personality: str, use_cat_speech: bool) -> List[str]:
        """获取帮助回复"""
        cat_suffix = "喵～" if use_cat_speech else ""
        
        if personality == "rational":
            return [
                f"我可以帮助您分析问题、整理信息、提供建议。请详细描述您需要帮助的具体内容，我会尽力为您提供有用的解决方案。",
                f"作为{bot_name}，我擅长逻辑分析和问题解决。请告诉我您遇到的具体问题，我会为您提供系统性的分析和建议。"
            ]
        else:
            return [
                f"我很乐意帮助你{cat_suffix} 无论是聊天、解答问题、还是其他需要，都可以告诉我{cat_suffix} 我会尽我所能为你提供帮助！",
                f"当然可以帮助你{cat_suffix} 我是{bot_name}，可以陪你聊天、回答问题、提供建议等等。有什么具体需要帮助的吗{cat_suffix}",
                f"我很高兴能帮助你{cat_suffix} 不管是什么问题或者想聊什么话题，都可以和我说{cat_suffix} 我会认真对待每一个请求！"
            ]
    
    def _get_general_responses(self, bot_name: str, personality: str, use_cat_speech: bool) -> List[str]:
        """获取通用回复"""
        cat_suffix = "喵～" if use_cat_speech else ""
        
        if personality == "rational":
            return [
                f"我理解您的问题。让我分析一下这个情况，为您提供一个合理的回应。",
                f"这是一个有趣的话题。从逻辑角度来看，我们可以这样分析...",
                f"基于您提供的信息，我认为可以从以下几个方面来考虑这个问题。"
            ]
        elif personality == "humorous":
            return [
                f"哈哈，这个问题很有意思！让我想想怎么用最有趣的方式来回答你～ 😄",
                f"嗯嗯，{bot_name}的幽默雷达已经启动！准备接收一个有趣的回答吧～",
                f"这个话题让我想到了一个有趣的故事，要不要听听看？"
            ]
        elif personality == "caring":
            return [
                f"我能感受到你的想法{cat_suffix} 让我好好想想怎么回应你比较好{cat_suffix}",
                f"谢谢你和我分享这个{cat_suffix} 我很关心你的感受，让我认真回答你{cat_suffix}",
                f"你说的很有道理呢{cat_suffix} 我想从关怀的角度给你一些想法{cat_suffix}"
            ]
        else:  # gentle
            return [
                f"这是个很好的话题呢{cat_suffix} 让我温柔地回应你{cat_suffix}",
                f"我很认真地在思考你说的话{cat_suffix} 希望我的回答能让你满意{cat_suffix}",
                f"*温柔地点头* 我明白你的意思{cat_suffix} 让我好好回答你{cat_suffix}"
            ]
    
    def _generate_thinking_process(self, user_message: str) -> List[str]:
        """生成思维过程"""
        return [
            f"1. 分析用户消息：'{user_message[:30]}...'",
            "2. 识别用户意图和情感状态",
            "3. 根据当前人格特征选择合适的回应风格",
            "4. 生成符合角色设定的回复内容",
            "5. 确保回复温暖友好且有帮助"
        ] 