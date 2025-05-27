"""
情感分析器
分析用户输入的情感倾向并返回对应的表情符号
"""
import re
from typing import Dict, List, Tuple
from enum import Enum
from pydantic import BaseModel
from core.logger import logger


class EmotionType(Enum):
    """情感类型枚举"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    LOVE = "love"


class EmotionResult(BaseModel):
    """情感分析结果"""
    emotion: EmotionType
    confidence: float
    emoji: str
    description: str


class EmotionAnalyzer:
    """情感分析器"""
    
    def __init__(self):
        # 情感关键词字典
        self.emotion_keywords = {
            EmotionType.JOY: ["开心", "高兴", "快乐", "兴奋", "愉快", "欢乐", "喜悦", "满意", "棒", "好", "赞"],
            EmotionType.SADNESS: ["难过", "伤心", "悲伤", "沮丧", "失望", "痛苦", "忧郁", "哭", "泪"],
            EmotionType.ANGER: ["生气", "愤怒", "恼火", "烦躁", "气愤", "讨厌", "恨", "怒"],
            EmotionType.FEAR: ["害怕", "恐惧", "担心", "焦虑", "紧张", "不安", "惊慌"],
            EmotionType.SURPRISE: ["惊讶", "震惊", "意外", "吃惊", "惊奇", "不敢相信"],
            EmotionType.LOVE: ["爱", "喜欢", "爱心", "心动", "迷恋", "喜爱", "钟爱"]
        }
        
        # 情感对应的表情符号
        self.emotion_emojis = {
            EmotionType.JOY: "😊",
            EmotionType.SADNESS: "😢",
            EmotionType.ANGER: "😠",
            EmotionType.FEAR: "😰",
            EmotionType.SURPRISE: "😲",
            EmotionType.LOVE: "❤️",
            EmotionType.POSITIVE: "😊",
            EmotionType.NEGATIVE: "😔",
            EmotionType.NEUTRAL: "😐"
        }
        
        # 情感描述
        self.emotion_descriptions = {
            EmotionType.JOY: "检测到积极愉快的情绪",
            EmotionType.SADNESS: "检测到悲伤难过的情绪",
            EmotionType.ANGER: "检测到愤怒不满的情绪",
            EmotionType.FEAR: "检测到恐惧担忧的情绪",
            EmotionType.SURPRISE: "检测到惊讶意外的情绪",
            EmotionType.LOVE: "检测到爱意喜爱的情绪",
            EmotionType.POSITIVE: "检测到正面积极的情绪",
            EmotionType.NEGATIVE: "检测到负面消极的情绪",
            EmotionType.NEUTRAL: "检测到中性平和的情绪"
        }
    
    def analyze_emotion(self, text: str) -> EmotionResult:
        """
        分析文本的情感倾向
        
        Args:
            text: 待分析的文本
            
        Returns:
            EmotionResult: 情感分析结果
        """
        text = text.lower()
        emotion_scores = {}
        
        # 基于关键词的情感分析
        for emotion_type, keywords in self.emotion_keywords.items():
            score = 0
            for keyword in keywords:
                # 计算关键词在文本中的出现次数
                count = len(re.findall(keyword, text))
                score += count
            
            if score > 0:
                emotion_scores[emotion_type] = score
        
        # 如果没有检测到特定情感，进行简单的正负面判断
        if not emotion_scores:
            positive_indicators = ["好", "棒", "赞", "不错", "可以", "行", "对", "是的", "谢谢"]
            negative_indicators = ["不", "没", "别", "不要", "不行", "不好", "错", "坏"]
            
            positive_score = sum(1 for indicator in positive_indicators if indicator in text)
            negative_score = sum(1 for indicator in negative_indicators if indicator in text)
            
            if positive_score > negative_score:
                emotion_type = EmotionType.POSITIVE
                confidence = min(0.8, positive_score * 0.3)
            elif negative_score > positive_score:
                emotion_type = EmotionType.NEGATIVE
                confidence = min(0.8, negative_score * 0.3)
            else:
                emotion_type = EmotionType.NEUTRAL
                confidence = 0.5
        else:
            # 选择得分最高的情感
            emotion_type = max(emotion_scores, key=emotion_scores.get)
            max_score = emotion_scores[emotion_type]
            confidence = min(0.9, max_score * 0.2 + 0.3)
        
        result = EmotionResult(
            emotion=emotion_type,
            confidence=confidence,
            emoji=self.emotion_emojis[emotion_type],
            description=self.emotion_descriptions[emotion_type]
        )
        
        logger.info(f"情感分析结果: {emotion_type.value}, 置信度: {confidence:.2f}")
        
        return result
    
    def get_emotion_emoji(self, emotion: EmotionType) -> str:
        """获取情感对应的表情符号"""
        return self.emotion_emojis.get(emotion, "😐")
    
    def get_random_emoji_by_emotion(self, emotion: EmotionType) -> str:
        """根据情感类型获取随机表情符号"""
        emoji_sets = {
            EmotionType.JOY: ["😊", "😄", "😃", "😁", "🙂", "😌", "🥰"],
            EmotionType.SADNESS: ["😢", "😭", "😔", "😞", "😟", "🥺"],
            EmotionType.ANGER: ["😠", "😡", "🤬", "😤", "💢"],
            EmotionType.FEAR: ["😰", "😨", "😱", "😧", "😦"],
            EmotionType.SURPRISE: ["😲", "😮", "😯", "🤯", "😵"],
            EmotionType.LOVE: ["❤️", "💕", "💖", "💗", "🥰", "😍"],
            EmotionType.POSITIVE: ["😊", "👍", "✨", "🌟", "💫"],
            EmotionType.NEGATIVE: ["😔", "👎", "💔", "😕"],
            EmotionType.NEUTRAL: ["😐", "🙂", "😊"]
        }
        
        import random
        emojis = emoji_sets.get(emotion, ["😐"])
        return random.choice(emojis) 