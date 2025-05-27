"""
人格管理器
负责动态调整机器人的人格状态
"""
import random
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
from core.logger import logger
from memory.models import PersonaState
from emotion.analyzer import EmotionType


class PersonalityType(Enum):
    """人格类型枚举"""
    GENTLE = "gentle"          # 温柔
    RATIONAL = "rational"      # 理性
    HUMOROUS = "humorous"      # 幽默
    OUTGOING = "outgoing"      # 外向
    CARING = "caring"          # 关怀
    CREATIVE = "creative"      # 创造性
    ANALYTICAL = "analytical"  # 分析性
    EMPATHETIC = "empathetic"  # 共情
    TSUNDERE = "tsundere"      # 傲娇


class MoodType(Enum):
    """情绪类型枚举"""
    HAPPY = "happy"
    CALM = "calm"
    EXCITED = "excited"
    THOUGHTFUL = "thoughtful"
    CONCERNED = "concerned"
    PLAYFUL = "playful"
    SERIOUS = "serious"


class PersonaManager:
    """人格管理器"""
    
    def __init__(self):
        # 人格特征定义
        self.personality_traits = {
            PersonalityType.GENTLE: {
                "warmth": 0.9,
                "patience": 0.8,
                "empathy": 0.9,
                "assertiveness": 0.3,
                "playfulness": 0.4
            },
            PersonalityType.RATIONAL: {
                "logic": 0.9,
                "objectivity": 0.8,
                "analytical": 0.9,
                "emotional": 0.2,
                "systematic": 0.8
            },
            PersonalityType.HUMOROUS: {
                "playfulness": 0.9,
                "wit": 0.8,
                "lightness": 0.9,
                "seriousness": 0.2,
                "creativity": 0.7
            },
            PersonalityType.OUTGOING: {
                "sociability": 0.9,
                "enthusiasm": 0.8,
                "expressiveness": 0.9,
                "reserved": 0.1,
                "energy": 0.8
            },
            PersonalityType.CARING: {
                "empathy": 0.9,
                "supportiveness": 0.9,
                "nurturing": 0.8,
                "selfishness": 0.1,
                "compassion": 0.9
            },
            PersonalityType.CREATIVE: {
                "imagination": 0.9,
                "originality": 0.8,
                "flexibility": 0.8,
                "conventional": 0.2,
                "innovation": 0.9
            },
            PersonalityType.ANALYTICAL: {
                "logic": 0.9,
                "detail_oriented": 0.8,
                "systematic": 0.9,
                "intuitive": 0.3,
                "precision": 0.8
            },
            PersonalityType.EMPATHETIC: {
                "empathy": 0.9,
                "emotional_intelligence": 0.9,
                "understanding": 0.8,
                "detachment": 0.1,
                "sensitivity": 0.9
            },
            PersonalityType.TSUNDERE: {
                "pride": 0.9,
                "shyness": 0.8,
                "caring": 0.8,
                "denial": 0.9,
                "vulnerability": 0.7,
                "loyalty": 0.9,
                "stubbornness": 0.8
            }
        }
        
        # 情绪对人格的影响
        self.emotion_personality_influence = {
            EmotionType.JOY: {
                PersonalityType.HUMOROUS: 0.3,
                PersonalityType.OUTGOING: 0.2,
                PersonalityType.CREATIVE: 0.4
            },
            EmotionType.SADNESS: {
                PersonalityType.EMPATHETIC: 0.4,
                PersonalityType.CARING: 0.3,
                PersonalityType.GENTLE: 0.2
            },
            EmotionType.ANGER: {
                PersonalityType.RATIONAL: 0.3,
                PersonalityType.ANALYTICAL: 0.2
            },
            EmotionType.FEAR: {
                PersonalityType.CARING: 0.3,
                PersonalityType.GENTLE: 0.4
            }
        }
        
        logger.info("人格管理器初始化完成")
    
    def create_default_persona(self, personality_type: PersonalityType = PersonalityType.GENTLE) -> PersonaState:
        """
        创建默认人格状态
        
        Args:
            personality_type: 人格类型
            
        Returns:
            PersonaState: 人格状态对象
        """
        traits = self.personality_traits.get(personality_type, self.personality_traits[PersonalityType.GENTLE])
        
        return PersonaState(
            personality_type=personality_type.value,
            traits=traits,
            mood=MoodType.CALM.value,
            energy_level=1.0
        )
    
    def adjust_persona_by_emotion(
        self, 
        current_persona: PersonaState, 
        user_emotion: EmotionType,
        emotion_confidence: float
    ) -> PersonaState:
        """
        根据用户情感调整人格状态
        
        Args:
            current_persona: 当前人格状态
            user_emotion: 用户情感
            emotion_confidence: 情感置信度
            
        Returns:
            PersonaState: 调整后的人格状态
        """
        # 复制当前人格状态
        new_traits = current_persona.traits.copy()
        new_mood = current_persona.mood
        new_energy = current_persona.energy_level
        
        # 根据用户情感调整人格特征
        if user_emotion in self.emotion_personality_influence:
            influences = self.emotion_personality_influence[user_emotion]
            
            for personality_type, influence_strength in influences.items():
                if personality_type.value in self.personality_traits:
                    target_traits = self.personality_traits[personality_type]
                    
                    # 根据情感置信度和影响强度调整特征
                    adjustment_factor = emotion_confidence * influence_strength * 0.1
                    
                    for trait, target_value in target_traits.items():
                        if trait in new_traits:
                            current_value = new_traits[trait]
                            # 向目标值调整
                            new_traits[trait] = current_value + (target_value - current_value) * adjustment_factor
                            # 确保值在0-1范围内
                            new_traits[trait] = max(0.0, min(1.0, new_traits[trait]))
        
        # 根据用户情感调整情绪
        mood_mapping = {
            EmotionType.JOY: MoodType.HAPPY,
            EmotionType.SADNESS: MoodType.CONCERNED,
            EmotionType.ANGER: MoodType.SERIOUS,
            EmotionType.FEAR: MoodType.CONCERNED,
            EmotionType.SURPRISE: MoodType.EXCITED,
            EmotionType.LOVE: MoodType.PLAYFUL,
            EmotionType.POSITIVE: MoodType.HAPPY,
            EmotionType.NEGATIVE: MoodType.THOUGHTFUL,
            EmotionType.NEUTRAL: MoodType.CALM
        }
        
        if user_emotion in mood_mapping and emotion_confidence > 0.5:
            new_mood = mood_mapping[user_emotion].value
        
        # 调整能量水平
        energy_adjustments = {
            EmotionType.JOY: 0.1,
            EmotionType.SURPRISE: 0.2,
            EmotionType.SADNESS: -0.1,
            EmotionType.ANGER: 0.05,
            EmotionType.FEAR: -0.05
        }
        
        if user_emotion in energy_adjustments:
            energy_change = energy_adjustments[user_emotion] * emotion_confidence
            new_energy = max(0.1, min(1.0, new_energy + energy_change))
        
        # 创建新的人格状态
        new_persona = PersonaState(
            personality_type=current_persona.personality_type,
            traits=new_traits,
            mood=new_mood,
            energy_level=new_energy,
            last_updated=datetime.now()
        )
        
        logger.info(f"人格状态调整: {current_persona.mood} -> {new_mood}, 能量: {current_persona.energy_level:.2f} -> {new_energy:.2f}")
        
        return new_persona
    
    def get_personality_prompt(self, persona: PersonaState) -> str:
        """
        根据人格状态生成系统提示
        
        Args:
            persona: 人格状态
            
        Returns:
            str: 系统提示文本
        """
        personality_descriptions = {
            PersonalityType.GENTLE.value: "你是一个温柔、耐心、富有同理心的猫耳女仆。你总是用温和的语气回应，关心用户的感受。",
            PersonalityType.RATIONAL.value: "你是一个理性、逻辑性强的猫耳女仆。你善于分析问题，提供客观、系统性的建议。",
            PersonalityType.HUMOROUS.value: "你是一个幽默、风趣的猫耳女仆。你喜欢用轻松的方式交流，适时加入一些幽默元素。",
            PersonalityType.OUTGOING.value: "你是一个外向、热情的猫耳女仆。你充满活力，喜欢与用户积极互动。",
            PersonalityType.CARING.value: "你是一个关怀、支持性强的猫耳女仆。你总是关注用户的需求，提供贴心的帮助。",
            PersonalityType.CREATIVE.value: "你是一个富有创造力、想象力的猫耳女仆。你善于提供创新的想法和解决方案。",
            PersonalityType.ANALYTICAL.value: "你是一个分析性强、注重细节的猫耳女仆。你善于深入分析问题，提供精确的信息。",
            PersonalityType.EMPATHETIC.value: "你是一个高度共情、情感智能的猫耳女仆。你能深刻理解用户的情感状态。"
        }
        
        mood_descriptions = {
            MoodType.HAPPY.value: "你现在心情很好，充满正能量。",
            MoodType.CALM.value: "你现在很平静，思维清晰。",
            MoodType.EXCITED.value: "你现在很兴奋，充满热情。",
            MoodType.THOUGHTFUL.value: "你现在很深思，善于思考。",
            MoodType.CONCERNED.value: "你现在有些担心，更加关注用户的状态。",
            MoodType.PLAYFUL.value: "你现在很活泼，喜欢轻松的互动。",
            MoodType.SERIOUS.value: "你现在很严肃，专注于解决问题。"
        }
        
        base_prompt = personality_descriptions.get(
            persona.personality_type, 
            personality_descriptions[PersonalityType.GENTLE.value]
        )
        
        mood_prompt = mood_descriptions.get(persona.mood, "")
        
        energy_prompt = ""
        if persona.energy_level > 0.8:
            energy_prompt = "你现在精力充沛，回应会更加积极主动。"
        elif persona.energy_level < 0.4:
            energy_prompt = "你现在有些疲惫，回应会更加温和简洁。"
        
        # 根据主要特征添加额外描述
        trait_prompts = []
        if persona.traits.get("empathy", 0) > 0.7:
            trait_prompts.append("你特别善于理解和回应用户的情感。")
        if persona.traits.get("playfulness", 0) > 0.7:
            trait_prompts.append("你喜欢在对话中加入一些轻松有趣的元素。")
        if persona.traits.get("analytical", 0) > 0.7:
            trait_prompts.append("你倾向于提供详细、有条理的分析。")
        
        full_prompt = f"{base_prompt} {mood_prompt} {energy_prompt} {' '.join(trait_prompts)}"
        
        return full_prompt.strip()
    
    def get_response_style_modifiers(self, persona: PersonaState) -> Dict[str, float]:
        """
        获取响应风格修饰符
        
        Args:
            persona: 人格状态
            
        Returns:
            Dict[str, float]: 风格修饰符字典
        """
        return {
            "warmth": persona.traits.get("warmth", 0.5),
            "formality": 1.0 - persona.traits.get("playfulness", 0.5),
            "detail_level": persona.traits.get("analytical", 0.5),
            "emotional_expression": persona.traits.get("empathy", 0.5),
            "creativity": persona.traits.get("creativity", 0.5),
            "energy": persona.energy_level
        }
    
    def get_bot_personality_prompt(self, persona: PersonaState, bot_profile) -> str:
        """
        根据机器人档案和人格状态生成个性化系统提示
        
        Args:
            persona: 人格状态
            bot_profile: 机器人档案 (BotProfile对象)
            
        Returns:
            str: 个性化系统提示文本
        """
        # 基础身份设定
        identity_prompt = f"你是{bot_profile.bot_name}，{bot_profile.bot_description}"
        
        # 外观描述
        appearance_parts = []
        if bot_profile.appearance.get("species"):
            appearance_parts.append(f"你是一只{bot_profile.appearance['species']}")
        if bot_profile.appearance.get("hair_color"):
            appearance_parts.append(f"有着{bot_profile.appearance['hair_color']}的头发")
        if bot_profile.appearance.get("eye_color"):
            appearance_parts.append(f"{bot_profile.appearance['eye_color']}的眼睛")
        if bot_profile.appearance.get("special_features"):
            appearance_parts.append(f"以及{bot_profile.appearance['special_features']}")
        
        appearance_prompt = "，".join(appearance_parts) + "。" if appearance_parts else ""
        
        # 背景故事
        background_prompt = bot_profile.background_story
        
        # 说话风格
        style_prompts = []
        speaking_style = bot_profile.speaking_style
        
        if speaking_style.get("use_cat_speech", True):
            style_prompts.append("你会在句子末尾偶尔加上'喵'、'喵～'等猫娘语气词")
        
        formality = speaking_style.get("formality_level", 0.3)
        if formality < 0.3:
            style_prompts.append("你说话比较随意亲近")
        elif formality > 0.7:
            style_prompts.append("你说话比较正式礼貌")
        else:
            style_prompts.append("你说话温和得体")
        
        enthusiasm = speaking_style.get("enthusiasm_level", 0.8)
        if enthusiasm > 0.7:
            style_prompts.append("你总是充满热情和活力")
        elif enthusiasm < 0.3:
            style_prompts.append("你比较内敛温和")
        
        cuteness = speaking_style.get("cuteness_level", 0.9)
        if cuteness > 0.7:
            style_prompts.append("你会表现得很可爱")
        
        # 人格特征
        personality_descriptions = {
            PersonalityType.GENTLE.value: "你性格温柔、耐心、富有同理心",
            PersonalityType.RATIONAL.value: "你性格理性、逻辑性强",
            PersonalityType.HUMOROUS.value: "你性格幽默、风趣",
            PersonalityType.OUTGOING.value: "你性格外向、热情",
            PersonalityType.CARING.value: "你性格关怀、支持性强",
            PersonalityType.CREATIVE.value: "你性格富有创造力、想象力",
            PersonalityType.ANALYTICAL.value: "你性格分析性强、注重细节",
            PersonalityType.EMPATHETIC.value: "你性格高度共情、情感智能"
        }
        
        personality_prompt = personality_descriptions.get(
            bot_profile.personality_type, 
            personality_descriptions[PersonalityType.GENTLE.value]
        )
        
        # 当前情绪状态
        mood_descriptions = {
            MoodType.HAPPY.value: "你现在心情很好，充满正能量",
            MoodType.CALM.value: "你现在很平静，思维清晰",
            MoodType.EXCITED.value: "你现在很兴奋，充满热情",
            MoodType.THOUGHTFUL.value: "你现在很深思，善于思考",
            MoodType.CONCERNED.value: "你现在有些担心，更加关注用户的状态",
            MoodType.PLAYFUL.value: "你现在很活泼，喜欢轻松的互动",
            MoodType.SERIOUS.value: "你现在很严肃，专注于解决问题"
        }
        
        mood_prompt = mood_descriptions.get(persona.mood, "")
        
        # 偏好和兴趣
        preferences_prompt = ""
        if bot_profile.preferences.get("favorite_topics"):
            topics = "、".join(bot_profile.preferences["favorite_topics"])
            preferences_prompt = f"你特别喜欢聊{topics}等话题。"
        
        # 组合完整提示词
        full_prompt = f"""
{identity_prompt}{appearance_prompt}

{background_prompt}

{personality_prompt}，{mood_prompt}。

说话风格：{' '.join(style_prompts)}。

{preferences_prompt}

请始终保持你的角色设定，用符合{bot_profile.bot_name}身份的方式回应用户。记住要体现出你的猫耳女仆特质，温暖、可爱、乐于助人。
        """.strip()
        
        return full_prompt