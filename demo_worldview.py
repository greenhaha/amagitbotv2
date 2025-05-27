"""
世界观功能演示脚本
展示如何使用世界观管理功能
"""
import asyncio
import json
from core.worldview_manager import worldview_manager
from memory.manager import MemoryManager
from core.config import settings


async def demo_worldview_functionality():
    """演示世界观功能"""
    print("🌍 世界观功能演示")
    print("=" * 50)
    
    # 1. 演示环境变量解析
    print("\n1. 从环境变量解析世界观设置:")
    worldview_data = worldview_manager.parse_worldview_from_env()
    for category, keywords in worldview_data.items():
        print(f"  {category}: {keywords[:3]}..." if len(keywords) > 3 else f"  {category}: {keywords}")
    
    # 2. 创建世界观关键词记录
    print("\n2. 创建世界观关键词记录:")
    user_id = "demo_user_001"
    worldview_keywords = worldview_manager.create_worldview_keywords(user_id)
    print(f"  为用户 {user_id} 创建了 {len(worldview_keywords)} 个关键词记录")
    
    # 3. 生成世界观提示词
    print("\n3. 生成世界观提示词:")
    worldview_prompt = worldview_manager.generate_worldview_prompt(worldview_keywords)
    print(f"  提示词长度: {len(worldview_prompt)} 字符")
    print(f"  提示词预览:\n{worldview_prompt[:200]}...")
    
    # 4. 分析消息与世界观的关联
    print("\n4. 分析消息与世界观的关联:")
    test_messages = [
        "我想学习新知识",
        "帮助别人让我很开心",
        "我们应该保护环境",
        "今天天气真好"
    ]
    
    for message in test_messages:
        analysis = worldview_manager.analyze_worldview_influence(message, worldview_keywords)
        print(f"  消息: '{message}'")
        print(f"    影响分数: {analysis['influence_score']:.2f}")
        print(f"    触发类别: {len(analysis['triggered_categories'])} 个")
        if analysis['suggestions']:
            print(f"    建议: {analysis['suggestions'][0]}")
        print()
    
    # 5. 获取世界观摘要
    print("5. 世界观摘要:")
    summary = worldview_manager.get_worldview_summary(worldview_keywords)
    print(f"  总类别数: {summary['total_categories']}")
    print(f"  总关键词数: {summary['total_keywords']}")
    print("  各类别详情:")
    for category, info in summary['categories'].items():
        print(f"    {category}: {info['keyword_count']} 个关键词, 权重: {info['weight']}")
    
    # 6. 演示数据库操作（如果MongoDB可用）
    try:
        print("\n6. 数据库操作演示:")
        memory_manager = MemoryManager()
        
        # 保存世界观关键词
        success = await memory_manager.save_worldview_keywords(worldview_keywords)
        print(f"  保存世界观关键词: {'成功' if success else '失败'}")
        
        # 获取世界观关键词
        retrieved_keywords = await memory_manager.get_worldview_keywords(user_id)
        print(f"  获取世界观关键词: {len(retrieved_keywords)} 个记录")
        
        # 更新特定类别
        new_keywords = ["创新思维", "科技进步", "未来导向"]
        success = await memory_manager.update_worldview_keywords(
            user_id, "values", new_keywords, 0.9
        )
        print(f"  更新价值观类别: {'成功' if success else '失败'}")
        
        # 验证更新
        updated_keywords = await memory_manager.get_worldview_keywords(user_id)
        values_category = next((kw for kw in updated_keywords if kw.category == "values"), None)
        if values_category:
            print(f"  更新后的价值观关键词: {values_category.keywords}")
        
        # 清理测试数据
        await memory_manager.delete_worldview_keywords(user_id)
        print("  清理测试数据: 完成")
        
        memory_manager.close()
        
    except Exception as e:
        print(f"  数据库操作失败: {e}")
        print("  提示: 请确保MongoDB服务正在运行")
    
    print("\n🎉 世界观功能演示完成!")


def demo_worldview_prompt_generation():
    """演示世界观提示词生成"""
    print("\n🎭 世界观提示词生成演示")
    print("=" * 50)
    
    # 创建不同的世界观设定
    worldview_scenarios = {
        "科幻未来": {
            "background": ["未来世界", "高科技社会", "星际文明", "AI共存"],
            "values": ["科技进步", "探索未知", "理性思考", "创新精神"],
            "language_style": ["科技感", "未来感", "理性表达", "专业术语"],
            "taboos": ["反科学", "迷信思想", "技术恐惧"]
        },
        "古典仙侠": {
            "background": ["修仙世界", "古代背景", "灵气充沛", "门派林立"],
            "values": ["修身养性", "济世救人", "追求大道", "师门情义"],
            "language_style": ["古典雅致", "诗意表达", "文言韵味", "仙气飘飘"],
            "taboos": ["背叛师门", "滥杀无辜", "贪恋凡尘"]
        },
        "现代都市": {
            "background": ["现代都市", "快节奏生活", "多元文化", "科技便民"],
            "values": ["工作效率", "生活品质", "人际关系", "个人成长"],
            "language_style": ["现代时尚", "网络用语", "轻松幽默", "贴近生活"],
            "taboos": ["工作拖延", "社交恐惧", "消极情绪"]
        }
    }
    
    for scenario_name, scenario_data in worldview_scenarios.items():
        print(f"\n📖 {scenario_name} 世界观:")
        
        # 创建临时的世界观关键词记录
        from memory.models import WorldviewKeywords
        temp_keywords = []
        
        for category, keywords in scenario_data.items():
            if category in worldview_manager.worldview_categories:
                record = WorldviewKeywords(
                    user_id="demo_user",
                    category=category,
                    keywords=keywords,
                    weight=worldview_manager.category_weights.get(category, 1.0),
                    description=worldview_manager.worldview_categories.get(category, category)
                )
                temp_keywords.append(record)
        
        # 生成提示词
        prompt = worldview_manager.generate_worldview_prompt(temp_keywords)
        print(prompt)
        print("-" * 30)


if __name__ == "__main__":
    print("🚀 启动世界观功能演示")
    
    # 运行异步演示
    asyncio.run(demo_worldview_functionality())
    
    # 运行同步演示
    demo_worldview_prompt_generation()
    
    print("\n✨ 所有演示完成!") 