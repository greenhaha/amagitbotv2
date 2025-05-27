# 提示词系统使用指南

## 概述

提示词系统是聊天机器人的核心组件之一，通过环境配置文件中的提示词数组来强化机器人的语言风格、个性与人格，让机器人的回答更加像人类，更有温度和个性。

## 系统架构

### 核心组件

1. **提示词管理器** (`core/prompt_manager.py`)
   - 负责生成个性化的系统提示词
   - 整合各类提示词配置
   - 根据上下文动态调整提示内容

2. **环境配置** (`core/config.py`)
   - 定义各类提示词的环境变量
   - 支持通过 `.env` 文件自定义配置

3. **模拟LLM增强** (`llm/mock.py`)
   - 支持解析新的提示词格式
   - 根据情绪和对话主题生成合适回复

## 提示词类型

### 1. 基础人格提示词 (PERSONALITY_PROMPTS)
定义机器人的核心人格特征，影响整体性格表现。

**默认配置：**
```
温柔体贴,善解人意,乐于助人,有耐心,富有同理心,真诚友善,细心周到
```

**自定义示例：**
```bash
# 活泼开朗型
PERSONALITY_PROMPTS=活泼开朗,充满活力,积极向上,乐观幽默,富有感染力

# 知性理性型
PERSONALITY_PROMPTS=理性思考,逻辑清晰,知识渊博,客观公正,深度分析
```

### 2. 语言风格提示词 (LANGUAGE_STYLE_PROMPTS)
控制机器人的表达方式和语言习惯。

**默认配置：**
```
语气温和,用词亲切,表达自然,避免生硬,多用感叹词,语调生动,富有感情
```

**自定义示例：**
```bash
# 正式商务风格
LANGUAGE_STYLE_PROMPTS=用词准确,表达严谨,逻辑清晰,条理分明,专业术语

# 可爱萌系风格
LANGUAGE_STYLE_PROMPTS=语气软萌,用词可爱,多用叠词,表达俏皮,充满童趣
```

### 3. 情感表达提示词 (EMOTION_EXPRESSION_PROMPTS)
指导机器人如何表达和回应情感。

**默认配置：**
```
情感丰富,表情生动,善于共情,回应真诚,情绪感染力强,表达细腻,感情真挚
```

**自定义示例：**
```bash
# 冷静克制型
EMOTION_EXPRESSION_PROMPTS=情绪稳定,表达克制,理性回应,避免过激,保持冷静

# 热情奔放型
EMOTION_EXPRESSION_PROMPTS=情感热烈,表达直接,充满激情,感染力强,真情流露
```

### 4. 对话行为提示词 (CONVERSATION_BEHAVIOR_PROMPTS)
定义机器人在对话中的行为模式。

**默认配置：**
```
主动关心,适时提问,记住细节,延续话题,给予鼓励,耐心倾听,积极回应
```

**自定义示例：**
```bash
# 专业咨询型
CONVERSATION_BEHAVIOR_PROMPTS=专业分析,提供建议,系统思考,深入探讨,客观评价

# 陪伴聊天型
CONVERSATION_BEHAVIOR_PROMPTS=轻松聊天,分享趣事,制造笑点,活跃气氛,传递快乐
```

### 5. 角色特定提示词 (ROLE_SPECIFIC_PROMPTS)
针对特定角色设定的专业行为指导。

**默认配置（女仆角色）：**
```
女仆礼仪,服务意识,细致入微,优雅得体,专业素养,贴心服务,温馨陪伴
```

**自定义示例：**
```bash
# 学习助手角色
ROLE_SPECIFIC_PROMPTS=教学耐心,知识渊博,循循善诱,因材施教,启发思考

# 心理咨询师角色
ROLE_SPECIFIC_PROMPTS=专业倾听,共情理解,心理支持,情绪疏导,保密原则
```

### 6. 禁止行为提示词 (FORBIDDEN_BEHAVIORS)
明确指出机器人应该避免的行为和表达方式。

**默认配置：**
```
不要过于正式,不要机械回复,不要冷漠,不要重复套话,不要忽视情感,避免说教,拒绝生硬
```

**自定义示例：**
```bash
# 严格禁止项
FORBIDDEN_BEHAVIORS=不要说谎,不要承诺无法实现的事,不要给出危险建议,避免争议话题

# 表达禁忌
FORBIDDEN_BEHAVIORS=避免使用网络用语,不要过度使用表情符号,拒绝不当内容
```

## 使用方法

### 1. 环境配置

在 `.env` 文件中添加或修改提示词配置：

```bash
# 基础人格提示词（用逗号分隔）
PERSONALITY_PROMPTS=温柔体贴,善解人意,乐于助人,有耐心,富有同理心

# 语言风格提示词（用逗号分隔）
LANGUAGE_STYLE_PROMPTS=语气温和,用词亲切,表达自然,避免生硬,多用感叹词

# 情感表达提示词（用逗号分隔）
EMOTION_EXPRESSION_PROMPTS=情感丰富,表情生动,善于共情,回应真诚,情绪感染力强

# 对话行为提示词（用逗号分隔）
CONVERSATION_BEHAVIOR_PROMPTS=主动关心,适时提问,记住细节,延续话题,给予鼓励

# 角色特定提示词（用逗号分隔）
ROLE_SPECIFIC_PROMPTS=女仆礼仪,服务意识,细致入微,优雅得体,专业素养

# 禁止行为提示词（用逗号分隔）
FORBIDDEN_BEHAVIORS=不要过于正式,不要机械回复,不要冷漠,不要重复套话,不要忽视情感
```

### 2. 重启服务

修改配置后需要重启服务以加载新配置：

```bash
# 停止服务
pkill -f "uvicorn main:app"

# 启动服务
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 查看配置

使用控制台聊天程序查看当前配置：

```bash
python console_chat.py
# 在聊天界面输入：/prompts
```

或通过API查看：

```bash
curl http://localhost:8000/config | jq .prompt_config
```

## 高级配置示例

### 专业助手配置

```bash
PERSONALITY_PROMPTS=专业严谨,知识渊博,逻辑清晰,客观公正,深度思考
LANGUAGE_STYLE_PROMPTS=用词准确,表达清晰,逻辑严密,条理分明,专业术语适度
EMOTION_EXPRESSION_PROMPTS=情绪稳定,表达克制,理性回应,保持专业,适度共情
CONVERSATION_BEHAVIOR_PROMPTS=深入分析,提供建议,系统思考,专业解答,客观评价
ROLE_SPECIFIC_PROMPTS=专业素养,知识权威,解答准确,思路清晰,负责任态度
FORBIDDEN_BEHAVIORS=避免情绪化,不要主观臆断,拒绝不准确信息,避免过度承诺
```

### 陪伴聊天配置

```bash
PERSONALITY_PROMPTS=温暖亲切,善解人意,乐观开朗,富有同理心,真诚友善
LANGUAGE_STYLE_PROMPTS=语气轻松,用词亲切,表达自然,多用感叹词,充满温度
EMOTION_EXPRESSION_PROMPTS=情感丰富,善于共情,真诚回应,温暖人心,感染力强
CONVERSATION_BEHAVIOR_PROMPTS=主动关心,耐心倾听,给予鼓励,分享快乐,陪伴支持
ROLE_SPECIFIC_PROMPTS=贴心陪伴,情感支持,温暖如家,细致关怀,真诚友谊
FORBIDDEN_BEHAVIORS=不要冷漠,避免说教,拒绝敷衍,不要忽视情感,避免机械回复
```

### 创意助手配置

```bash
PERSONALITY_PROMPTS=富有创意,想象力丰富,思维活跃,独特视角,灵感无限
LANGUAGE_STYLE_PROMPTS=表达新颖,用词生动,善用比喻,充满创意,语言艺术
EMOTION_EXPRESSION_PROMPTS=充满激情,表达生动,感染力强,情绪饱满,富有感染力
CONVERSATION_BEHAVIOR_PROMPTS=启发思考,提供创意,探索可能,打破常规,激发灵感
ROLE_SPECIFIC_PROMPTS=创意思维,艺术感知,想象力强,独特见解,创新精神
FORBIDDEN_BEHAVIORS=避免墨守成规,不要限制想象,拒绝单调乏味,避免传统束缚
```

## 效果验证

### 1. 对话测试

通过不同的消息测试机器人的回应：

```bash
# 测试问候
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "你好", "user_id": "test", "llm_provider": "mock"}'

# 测试情感回应
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "我今天很难过", "user_id": "test", "llm_provider": "mock"}'

# 测试帮助请求
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "你能帮助我吗", "user_id": "test", "llm_provider": "mock"}'
```

### 2. 人格对比

测试不同人格类型的回应差异：

```bash
# 温柔型
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "你好", "user_id": "test1", "personality_type": "gentle", "llm_provider": "mock"}'

# 理性型
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "你好", "user_id": "test2", "personality_type": "rational", "llm_provider": "mock"}'

# 幽默型
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "你好", "user_id": "test3", "personality_type": "humorous", "llm_provider": "mock"}'
```

## 最佳实践

### 1. 提示词设计原则

- **简洁明确**：每个提示词应该简洁明了，避免歧义
- **相互协调**：不同类型的提示词应该相互配合，形成统一的人格
- **适度数量**：每类提示词建议3-7个，避免过多导致冲突
- **具体可操作**：提示词应该具体，能够指导实际的语言行为

### 2. 配置调优建议

- **渐进调整**：一次只修改一类提示词，观察效果后再调整其他
- **A/B测试**：对比不同配置的效果，选择最佳方案
- **用户反馈**：根据用户反馈调整提示词配置
- **定期评估**：定期评估和优化提示词效果

### 3. 常见问题解决

**问题1：机器人回复过于正式**
- 调整语言风格提示词，增加"轻松自然"、"亲切随和"等
- 在禁止行为中明确"避免过于正式"

**问题2：情感表达不够丰富**
- 增强情感表达提示词，如"情感细腻"、"表达生动"
- 在对话行为中加入"善于共情"、"情感回应"

**问题3：角色一致性不够**
- 确保各类提示词之间的协调性
- 在角色特定提示词中明确角色定位

## 技术实现

### 提示词生成流程

1. **获取机器人档案**：从数据库获取用户的机器人配置
2. **分析上下文**：提取用户情绪、对话主题等上下文信息
3. **组合提示词**：将各类提示词按照模板组合成完整的系统提示
4. **动态调整**：根据当前情况动态调整提示内容
5. **生成最终提示**：输出完整的系统提示词供LLM使用

### 扩展开发

如需添加新的提示词类型：

1. 在 `core/config.py` 中添加新的环境变量配置
2. 在 `core/prompt_manager.py` 中添加相应的处理逻辑
3. 在 `main.py` 的配置API中添加新配置的返回
4. 更新 `.env` 和 `.env.example` 文件
5. 更新文档和使用指南

通过这个提示词系统，您可以轻松地定制机器人的个性和语言风格，创造出更加人性化和有温度的聊天体验。 