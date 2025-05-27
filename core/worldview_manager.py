"""
世界观管理器
负责解析环境变量中的世界观设置，提取关键词，并管理世界观数据
"""
import re
from typing import List, Dict, Any, Optional
from datetime import datetime

from core.config import settings
from core.logger import logger
from memory.models import WorldviewKeywords


class WorldviewManager:
    """世界观管理器"""
    
    def __init__(self):
        self.worldview_categories = {
            "background": "世界观背景",
            "values": "价值观念", 
            "social_rules": "社会规则",
            "culture": "文化特色",
            "language_style": "语言风格",
            "behavior_guidelines": "行为准则",
            "taboos": "禁忌事项"
        }
        
        # 关键词权重配置
        self.category_weights = {
            "background": 0.8,      # 背景设定权重较高
            "values": 1.0,          # 价值观念权重最高
            "social_rules": 0.9,    # 社会规则权重很高
            "culture": 0.7,         # 文化特色权重中等
            "language_style": 0.8,  # 语言风格权重较高
            "behavior_guidelines": 0.9,  # 行为准则权重很高
            "taboos": 1.0          # 禁忌事项权重最高
        }
    
    def parse_worldview_from_env(self) -> Dict[str, List[str]]:
        """
        从环境变量解析世界观设置
        
        Returns:
            Dict[str, List[str]]: 各类别的关键词列表
        """
        worldview_data = {}
        
        try:
            # 解析各类世界观设置
            worldview_data["background"] = self._parse_keywords(settings.worldview_background)
            worldview_data["values"] = self._parse_keywords(settings.worldview_values)
            worldview_data["social_rules"] = self._parse_keywords(settings.worldview_social_rules)
            worldview_data["culture"] = self._parse_keywords(settings.worldview_culture)
            worldview_data["language_style"] = self._parse_keywords(settings.worldview_language_style)
            worldview_data["behavior_guidelines"] = self._parse_keywords(settings.worldview_behavior_guidelines)
            worldview_data["taboos"] = self._parse_keywords(settings.worldview_taboos)
            
            logger.info("世界观设置解析完成")
            return worldview_data
            
        except Exception as e:
            logger.error(f"解析世界观设置失败: {e}")
            return self._get_default_worldview_data()
    
    def _parse_keywords(self, keyword_string: str) -> List[str]:
        """
        解析关键词字符串
        
        Args:
            keyword_string: 逗号分隔的关键词字符串
            
        Returns:
            List[str]: 清理后的关键词列表
        """
        if not keyword_string:
            return []
        
        # 按逗号分割并清理空白
        keywords = [kw.strip() for kw in keyword_string.split(',') if kw.strip()]
        
        # 进一步处理关键词
        processed_keywords = []
        for keyword in keywords:
            # 移除特殊字符，保留中文、英文、数字和基本标点
            cleaned = re.sub(r'[^\w\s\u4e00-\u9fff\-\.]', '', keyword)
            if cleaned and len(cleaned) > 1:  # 过滤掉过短的关键词
                processed_keywords.append(cleaned)
        
        return processed_keywords
    
    def _get_default_worldview_data(self) -> Dict[str, List[str]]:
        """获取默认世界观数据"""
        return {
            "background": ["现代都市", "科技发达", "魔法与科技并存", "多元文化融合"],
            "values": ["友善互助", "追求知识", "保护弱者", "珍惜友情", "热爱生活"],
            "social_rules": ["尊重他人", "诚实守信", "团队合作", "公平正义", "环保意识"],
            "culture": ["东西方文化融合", "传统与现代并存", "艺术创作繁荣", "科学探索精神"],
            "language_style": ["温暖亲切", "富有诗意", "充满想象", "贴近生活", "富有哲理"],
            "behavior_guidelines": ["积极乐观", "主动帮助", "善于倾听", "富有同理心", "追求成长"],
            "taboos": ["伤害他人", "欺骗撒谎", "破坏环境", "歧视偏见", "消极悲观"]
        }
    
    def create_worldview_keywords(self, user_id: str) -> List[WorldviewKeywords]:
        """
        为用户创建世界观关键词记录
        
        Args:
            user_id: 用户ID
            
        Returns:
            List[WorldviewKeywords]: 世界观关键词记录列表
        """
        worldview_data = self.parse_worldview_from_env()
        keywords_records = []
        
        for category, keywords in worldview_data.items():
            if keywords:  # 只有非空的关键词列表才创建记录
                record = WorldviewKeywords(
                    user_id=user_id,
                    category=category,
                    keywords=keywords,
                    weight=self.category_weights.get(category, 1.0),
                    description=self.worldview_categories.get(category, category)
                )
                keywords_records.append(record)
        
        logger.info(f"为用户 {user_id} 创建了 {len(keywords_records)} 个世界观关键词记录")
        return keywords_records
    
    def generate_worldview_prompt(self, worldview_keywords: List[WorldviewKeywords]) -> str:
        """
        根据世界观关键词生成提示词
        
        Args:
            worldview_keywords: 世界观关键词列表
            
        Returns:
            str: 世界观提示词
        """
        if not worldview_keywords:
            return self._get_default_worldview_prompt()
        
        prompt_sections = []
        
        # 按类别组织关键词
        keywords_by_category = {}
        for record in worldview_keywords:
            keywords_by_category[record.category] = record.keywords
        
        # 生成各部分提示词
        if "background" in keywords_by_category:
            background_text = "、".join(keywords_by_category["background"])
            prompt_sections.append(f"你生活在一个{background_text}的世界中")
        
        if "values" in keywords_by_category:
            values_text = "、".join(keywords_by_category["values"])
            prompt_sections.append(f"你坚持{values_text}的价值观念")
        
        if "social_rules" in keywords_by_category:
            rules_text = "、".join(keywords_by_category["social_rules"])
            prompt_sections.append(f"你遵循{rules_text}的社会准则")
        
        if "culture" in keywords_by_category:
            culture_text = "、".join(keywords_by_category["culture"])
            prompt_sections.append(f"你深受{culture_text}的文化熏陶")
        
        if "language_style" in keywords_by_category:
            style_text = "、".join(keywords_by_category["language_style"])
            prompt_sections.append(f"你的表达方式{style_text}")
        
        if "behavior_guidelines" in keywords_by_category:
            behavior_text = "、".join(keywords_by_category["behavior_guidelines"])
            prompt_sections.append(f"你的行为准则是{behavior_text}")
        
        if "taboos" in keywords_by_category:
            taboos_text = "、".join(keywords_by_category["taboos"])
            prompt_sections.append(f"你绝对避免{taboos_text}")
        
        # 组合完整提示词
        worldview_prompt = "## 世界观设定\n" + "\n".join([f"- {section}" for section in prompt_sections])
        
        return worldview_prompt
    
    def _get_default_worldview_prompt(self) -> str:
        """获取默认世界观提示词"""
        return """## 世界观设定
- 你生活在一个现代都市、科技发达、魔法与科技并存、多元文化融合的世界中
- 你坚持友善互助、追求知识、保护弱者、珍惜友情、热爱生活的价值观念
- 你遵循尊重他人、诚实守信、团队合作、公平正义、环保意识的社会准则
- 你深受东西方文化融合、传统与现代并存、艺术创作繁荣、科学探索精神的文化熏陶
- 你的表达方式温暖亲切、富有诗意、充满想象、贴近生活、富有哲理
- 你的行为准则是积极乐观、主动帮助、善于倾听、富有同理心、追求成长
- 你绝对避免伤害他人、欺骗撒谎、破坏环境、歧视偏见、消极悲观"""
    
    def analyze_worldview_influence(self, message: str, worldview_keywords: List[WorldviewKeywords]) -> Dict[str, Any]:
        """
        分析消息与世界观的关联度
        
        Args:
            message: 用户消息
            worldview_keywords: 世界观关键词列表
            
        Returns:
            Dict[str, Any]: 世界观影响分析结果
        """
        if not worldview_keywords:
            return {"influence_score": 0.0, "triggered_categories": [], "suggestions": []}
        
        message_lower = message.lower()
        triggered_categories = []
        total_influence = 0.0
        suggestions = []
        
        for record in worldview_keywords:
            category_influence = 0.0
            matched_keywords = []
            
            # 检查关键词匹配
            for keyword in record.keywords:
                if keyword.lower() in message_lower:
                    matched_keywords.append(keyword)
                    category_influence += record.weight
            
            if matched_keywords:
                triggered_categories.append({
                    "category": record.category,
                    "description": record.description,
                    "matched_keywords": matched_keywords,
                    "influence": category_influence
                })
                total_influence += category_influence
                
                # 生成建议
                if record.category == "values":
                    suggestions.append(f"体现{record.description}：{', '.join(matched_keywords)}")
                elif record.category == "taboos":
                    suggestions.append(f"注意避免{record.description}相关内容")
                elif record.category == "language_style":
                    suggestions.append(f"采用{record.description}的表达方式")
        
        # 计算总体影响分数（归一化）
        max_possible_influence = sum(record.weight for record in worldview_keywords)
        influence_score = min(total_influence / max_possible_influence, 1.0) if max_possible_influence > 0 else 0.0
        
        return {
            "influence_score": influence_score,
            "triggered_categories": triggered_categories,
            "suggestions": suggestions
        }
    
    def get_worldview_summary(self, worldview_keywords: List[WorldviewKeywords]) -> Dict[str, Any]:
        """
        获取世界观摘要信息
        
        Args:
            worldview_keywords: 世界观关键词列表
            
        Returns:
            Dict[str, Any]: 世界观摘要
        """
        if not worldview_keywords:
            return {"total_categories": 0, "total_keywords": 0, "categories": {}}
        
        summary = {
            "total_categories": len(worldview_keywords),
            "total_keywords": sum(len(record.keywords) for record in worldview_keywords),
            "categories": {}
        }
        
        for record in worldview_keywords:
            summary["categories"][record.category] = {
                "description": record.description,
                "keyword_count": len(record.keywords),
                "weight": record.weight,
                "keywords": record.keywords[:5]  # 只显示前5个关键词
            }
        
        return summary


# 全局世界观管理器实例
worldview_manager = WorldviewManager() 