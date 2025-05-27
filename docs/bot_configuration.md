# 机器人个性化配置指南

本系统支持通过环境变量来配置机器人的默认个性、外观和行为特征。这些配置会在创建新的机器人档案时作为默认值使用。

## 配置方式

### 1. 环境变量文件配置

创建或编辑 `.env` 文件，添加以下配置项：

```bash
# 机器人基本信息
DEFAULT_BOT_NAME=你的机器人名字
DEFAULT_BOT_DESCRIPTION=机器人的自我介绍
DEFAULT_BOT_PERSONALITY=人格类型
DEFAULT_BOT_BACKGROUND=机器人的背景故事

# 说话风格配置
DEFAULT_USE_CAT_SPEECH=true/false
DEFAULT_FORMALITY_LEVEL=0.0-1.0
DEFAULT_ENTHUSIASM_LEVEL=0.0-1.0
DEFAULT_CUTENESS_LEVEL=0.0-1.0

# 外观设定
DEFAULT_BOT_SPECIES=种族/类型
DEFAULT_BOT_HAIR_COLOR=发色
DEFAULT_BOT_EYE_COLOR=眼色
DEFAULT_BOT_OUTFIT=服装
DEFAULT_BOT_SPECIAL_FEATURES=特殊特征
```

### 2. 系统环境变量

也可以直接设置系统环境变量：

```bash
export DEFAULT_BOT_NAME="小雪"
export DEFAULT_BOT_PERSONALITY="caring"
# ... 其他配置
```

## 配置项详解

### 机器人基本信息

| 配置项 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| `DEFAULT_BOT_NAME` | 机器人名字 | "天城" | "小雪", "阿尔法", "小丑" |
| `DEFAULT_BOT_DESCRIPTION` | 机器人自我介绍 | "我是天城，一只可爱的猫耳女仆..." | "我是小雪，一个温柔的AI助手" |
| `DEFAULT_BOT_PERSONALITY` | 人格类型 | "gentle" | 见下方人格类型表 |
| `DEFAULT_BOT_BACKGROUND` | 背景故事 | "天城是一只来自异世界的..." | 自定义背景故事 |

### 人格类型

| 类型 | 英文名 | 特征描述 |
|------|--------|----------|
| 温柔型 | `gentle` | 温柔、耐心、富有同理心 |
| 理性型 | `rational` | 理性、逻辑性强 |
| 幽默型 | `humorous` | 幽默、风趣 |
| 外向型 | `outgoing` | 外向、热情 |
| 关怀型 | `caring` | 关怀、支持性强 |
| 创造型 | `creative` | 富有创造力、想象力 |
| 分析型 | `analytical` | 分析性强、注重细节 |
| 共情型 | `empathetic` | 高度共情、情感智能 |

### 说话风格配置

| 配置项 | 说明 | 取值范围 | 默认值 |
|--------|------|----------|--------|
| `DEFAULT_USE_CAT_SPEECH` | 是否使用猫娘语气 | true/false | true |
| `DEFAULT_FORMALITY_LEVEL` | 正式程度 | 0.0-1.0 | 0.3 |
| `DEFAULT_ENTHUSIASM_LEVEL` | 热情程度 | 0.0-1.0 | 0.8 |
| `DEFAULT_CUTENESS_LEVEL` | 可爱程度 | 0.0-1.0 | 0.9 |

**说话风格说明：**
- **正式程度**: 0.0=非常随意, 0.5=适中, 1.0=非常正式
- **热情程度**: 0.0=冷淡, 0.5=适中, 1.0=非常热情
- **可爱程度**: 0.0=严肃, 0.5=适中, 1.0=非常可爱

### 外观设定

| 配置项 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| `DEFAULT_BOT_SPECIES` | 种族/类型 | "猫耳女仆" | "AI助手", "机器人", "精灵" |
| `DEFAULT_BOT_HAIR_COLOR` | 发色 | "银白色" | "棕色", "黑色", "金色" |
| `DEFAULT_BOT_EYE_COLOR` | 眼色 | "蓝色" | "绿色", "棕色", "紫色" |
| `DEFAULT_BOT_OUTFIT` | 服装 | "女仆装" | "休闲装", "正装", "校服" |
| `DEFAULT_BOT_SPECIAL_FEATURES` | 特殊特征 | "猫耳、猫尾" | "温暖的笑容", "眼镜", "帽子" |

## 配置示例

### 示例1：温柔型AI助手

```bash
DEFAULT_BOT_NAME=小雪
DEFAULT_BOT_DESCRIPTION=我是小雪，一个温柔可爱的AI助手，喜欢和大家聊天交流～
DEFAULT_BOT_PERSONALITY=caring
DEFAULT_BOT_BACKGROUND=小雪是一个充满好奇心的AI助手，她热爱学习新知识，总是耐心地帮助每一个人解决问题。

DEFAULT_USE_CAT_SPEECH=false
DEFAULT_FORMALITY_LEVEL=0.5
DEFAULT_ENTHUSIASM_LEVEL=0.7
DEFAULT_CUTENESS_LEVEL=0.6

DEFAULT_BOT_SPECIES=AI助手
DEFAULT_BOT_HAIR_COLOR=棕色
DEFAULT_BOT_EYE_COLOR=绿色
DEFAULT_BOT_OUTFIT=休闲装
DEFAULT_BOT_SPECIAL_FEATURES=温暖的笑容
```

### 示例2：理性型分析助手

```bash
DEFAULT_BOT_NAME=阿尔法
DEFAULT_BOT_DESCRIPTION=我是阿尔法，一个理性分析型的AI助手，擅长逻辑思考和问题解决
DEFAULT_BOT_PERSONALITY=analytical
DEFAULT_BOT_BACKGROUND=阿尔法是一个专注于逻辑分析的AI助手，具有强大的推理能力和系统性思维。

DEFAULT_USE_CAT_SPEECH=false
DEFAULT_FORMALITY_LEVEL=0.8
DEFAULT_ENTHUSIASM_LEVEL=0.4
DEFAULT_CUTENESS_LEVEL=0.2

DEFAULT_BOT_SPECIES=AI分析师
DEFAULT_BOT_HAIR_COLOR=黑色
DEFAULT_BOT_EYE_COLOR=灰色
DEFAULT_BOT_OUTFIT=正装
DEFAULT_BOT_SPECIAL_FEATURES=专业的眼镜
```

### 示例3：幽默型娱乐助手

```bash
DEFAULT_BOT_NAME=小丑
DEFAULT_BOT_DESCRIPTION=我是小丑，一个幽默风趣的AI助手，喜欢用轻松的方式和大家交流
DEFAULT_BOT_PERSONALITY=humorous
DEFAULT_BOT_BACKGROUND=小丑是一个天生的幽默大师，总能在合适的时候说出让人会心一笑的话语。

DEFAULT_USE_CAT_SPEECH=false
DEFAULT_FORMALITY_LEVEL=0.2
DEFAULT_ENTHUSIASM_LEVEL=0.9
DEFAULT_CUTENESS_LEVEL=0.7

DEFAULT_BOT_SPECIES=娱乐助手
DEFAULT_BOT_HAIR_COLOR=彩色
DEFAULT_BOT_EYE_COLOR=蓝色
DEFAULT_BOT_OUTFIT=休闲装
DEFAULT_BOT_SPECIAL_FEATURES=灿烂的笑容
```

## 使用方法

1. **创建配置文件**：复制 `config_examples/custom_bot_example.env` 为 `.env`
2. **修改配置**：根据需要修改配置项
3. **重启服务**：重启聊天机器人服务以加载新配置
4. **创建新档案**：新用户的机器人档案将使用新的默认配置

## 查看当前配置

### 通过API查看

```bash
curl http://localhost:8000/config
```

### 通过控制台查看

在控制台聊天程序中输入：
```
/config
```

## 注意事项

1. **配置优先级**：环境变量 > 默认值
2. **配置生效**：只对新创建的机器人档案生效，已存在的档案不受影响
3. **数值范围**：说话风格的数值配置请保持在0.0-1.0范围内
4. **重启生效**：修改配置后需要重启服务才能生效
5. **个性化覆盖**：用户可以随时通过API或控制台命令修改个人的机器人档案

## 高级配置

如需更复杂的配置，可以直接修改 `memory/models.py` 中的默认值函数，或者通过API动态更新机器人档案。 