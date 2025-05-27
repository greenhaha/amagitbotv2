# 赛博女仆「天城」V2.0
<p align="center">

![yjtp](./image/image.png)

</p>
一个支持模块化的多功能聊天机器人系统，具备六大核心能力：智能对话、实时思维、情感表达、持久记忆、动态人格和知识学习。

## 🌟 系统特性

### 1️⃣ 智能对话系统（LLM 接入）
- 支持 DeepSeek 和 SiliconFlow 的 API 接入
- 动态切换调用的模型源
- 遵循 OpenAI 风格的 ChatCompletion 接口结构

### 2️⃣ 实时思维系统
- 模拟人类思考流程（Chain of Thought）
- 输出中间思考步骤
- 支持调试和解释模型推理过程

### 3️⃣ 情感表达系统
- 基于关键词的情感倾向分析
- 支持正面、中性、负面等多种情感类型
- 自动附加对应的 Emoji 表情反馈

### 4️⃣ 持久记忆系统（MongoDB）
- 使用 MongoDB 存储长期用户对话记录
- 支持人格状态持久化
- 提供插入、查询、上下文提取、记忆总结能力

### 5️⃣ 动态人格系统
- 支持8种人格类型：温柔、理性、幽默、外向、关怀、创造性、分析性、共情
- 根据用户情绪和上下文动态调整人格响应
- 人格状态实时更新并持久化存储

### 6️⃣ 知识库学习系统（基于向量检索）
- 使用 ChromaDB 进行向量存储和检索
- 支持历史对话内容的语义搜索
- 集成短期记忆（RAG）和长期记忆联动

## 🛠️ 技术栈

- **Python 3.10+**
- **FastAPI** - Web API 框架
- **MongoDB** - 记忆持久化存储
- **ChromaDB** - 向量数据库
- **SentenceTransformers** - 文本向量化
- **Loguru** - 日志记录
- **Pydantic** - 数据验证
- **Pytest** - 单元测试

## 📁 项目结构

```
├── llm/              # DeepSeek / SiliconFlow 接入封装
│   ├── __init__.py
│   ├── base.py       # LLM基础抽象类
│   ├── deepseek.py   # DeepSeek实现
│   ├── siliconflow.py # SiliconFlow实现
│   └── factory.py    # LLM工厂类
├── emotion/          # 情感识别模块
│   ├── __init__.py
│   └── analyzer.py   # 情感分析器
├── memory/           # MongoDB 记忆持久化
│   ├── __init__.py
│   ├── models.py     # 数据模型
│   └── manager.py    # 记忆管理器
├── persona/          # 人格状态处理
│   ├── __init__.py
│   └── manager.py    # 人格管理器
├── rag/              # 知识学习模块
│   ├── __init__.py
│   └── knowledge_base.py # 知识库管理器
├── core/             # 主逻辑和聊天控制器
│   ├── __init__.py
│   ├── config.py     # 配置管理
│   ├── logger.py     # 日志管理
│   └── chatbot.py    # 核心控制器
├── tests/            # 测试模块
│   ├── __init__.py
│   └── test_chatbot.py
├── main.py           # FastAPI 服务入口
├── requirements.txt  # 依赖包
├── env_example.txt   # 环境变量示例
└── README.md         # 项目文档
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd chatbot-system

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制环境变量示例文件
cp env_example.txt .env

# 编辑 .env 文件，填入你的API密钥和机器人配置
# DEEPSEEK_API_KEY=your_deepseek_api_key_here
# SILICONFLOW_API_KEY=your_siliconflow_api_key_here
```

#### 🤖 机器人个性化配置

本系统支持通过环境变量自定义机器人的默认个性、外观和行为特征：

```bash
# 在 .env 文件中添加机器人配置
DEFAULT_BOT_NAME=你的机器人名字
DEFAULT_BOT_PERSONALITY=gentle  # 人格类型
DEFAULT_BOT_DESCRIPTION=机器人的自我介绍
DEFAULT_USE_CAT_SPEECH=true     # 是否使用猫娘语气
DEFAULT_FORMALITY_LEVEL=0.3     # 正式程度 (0.0-1.0)
DEFAULT_ENTHUSIASM_LEVEL=0.8    # 热情程度 (0.0-1.0)
DEFAULT_CUTENESS_LEVEL=0.9      # 可爱程度 (0.0-1.0)
```

**支持的人格类型：**
- `gentle` - 温柔型
- `rational` - 理性型  
- `humorous` - 幽默型
- `outgoing` - 外向型
- `caring` - 关怀型
- `creative` - 创造型
- `analytical` - 分析型
- `empathetic` - 共情型

详细配置说明请参考：[机器人配置指南](docs/bot_configuration.md)

### 3. 启动MongoDB

```bash
# 使用Docker启动MongoDB
docker run -d -p 27017:27017 --name chatbot-mongo mongo:latest

# 或使用本地MongoDB服务
mongod --dbpath /path/to/your/db
```

### 4. 运行应用

```bash
# 启动FastAPI服务
python main.py

# 或使用uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. 访问API

打开浏览器访问：
- API文档：http://localhost:8000/docs
- 系统状态：http://localhost:8000/
- 健康检查：http://localhost:8000/health

## 📝 API 使用示例

### 聊天接口

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好，我今天心情不太好",
    "user_id": "user123",
    "enable_thinking": true,
    "personality_type": "empathetic"
  }'
```

### 响应示例

```json
{
  "response": "我能感受到你现在的心情不太好，这让我很关心你。😔 无论发生了什么，请记住这些情绪都是暂时的，我在这里陪伴你。你愿意和我分享一下是什么让你感到不开心吗？",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "thinking_process": [
    "1. 用户表达了负面情绪，需要给予关怀和支持",
    "2. 作为共情型人格，应该表现出理解和陪伴",
    "3. 提供开放性问题，鼓励用户进一步表达"
  ],
  "emotion_analysis": {
    "emotion": "sadness",
    "confidence": 0.75,
    "emoji": "😔",
    "description": "检测到悲伤难过的情绪"
  },
  "persona_state": {
    "personality_type": "empathetic",
    "mood": "concerned",
    "energy_level": 0.9,
    "main_traits": {
      "empathy": 0.95,
      "emotional_intelligence": 0.9,
      "understanding": 0.85
    }
  },
  "relevant_memories": [],
  "knowledge_base_action": "stored",
  "metadata": {
    "llm_model": "deepseek-chat",
    "processing_time": "2024-01-01T12:00:00Z"
  }
}
```

## 🧪 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_chatbot.py

# 运行测试并显示覆盖率
pytest --cov=.
```

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DEEPSEEK_API_KEY` | DeepSeek API密钥 | - |
| `SILICONFLOW_API_KEY` | SiliconFlow API密钥 | - |
| `DEFAULT_LLM_PROVIDER` | 默认LLM提供商 | `deepseek` |
| `MONGODB_URL` | MongoDB连接URL | `mongodb://localhost:27017` |
| `MONGODB_DATABASE` | MongoDB数据库名 | `chatbot_db` |
| `LOG_LEVEL` | 日志级别 | `INFO` |
| `CHROMA_PERSIST_DIRECTORY` | ChromaDB存储目录 | `./chroma_db` |

### 人格类型

- `gentle` - 温柔、耐心、富有同理心
- `rational` - 理性、逻辑性强
- `humorous` - 幽默、风趣
- `outgoing` - 外向、热情
- `caring` - 关怀、支持性强
- `creative` - 富有创造力、想象力
- `analytical` - 分析性强、注重细节
- `empathetic` - 高度共情、情感智能

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代、快速的Web框架
- [ChromaDB](https://www.trychroma.com/) - 向量数据库
- [SentenceTransformers](https://www.sbert.net/) - 文本嵌入模型
- [Loguru](https://loguru.readthedocs.io/) - 优雅的日志记录

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件至：[1498706069@qq.com]
- QQ群：731352652

## 🎨 个性化提示词系统

新增的提示词系统是本项目的核心特色之一，通过环境配置文件中的提示词数组来强化机器人的语言风格、个性与人格，让机器人回答更加像人类，更有温度和个性。

### 提示词类型

- **基础人格提示词** - 定义机器人的核心人格特征
- **语言风格提示词** - 控制表达方式和语言习惯
- **情感表达提示词** - 指导情感表达和回应
- **对话行为提示词** - 定义对话中的行为模式
- **角色特定提示词** - 针对特定角色的专业指导
- **禁止行为提示词** - 明确应避免的行为和表达

### 快速配置

在 `.env` 文件中自定义提示词：

```bash
# 基础人格提示词（用逗号分隔）
PERSONALITY_PROMPTS=温柔体贴,善解人意,乐于助人,有耐心,富有同理心

# 语言风格提示词（用逗号分隔）
LANGUAGE_STYLE_PROMPTS=语气温和,用词亲切,表达自然,避免生硬,多用感叹词

# 情感表达提示词（用逗号分隔）
EMOTION_EXPRESSION_PROMPTS=情感丰富,表情生动,善于共情,回应真诚,情绪感染力强
```

详细使用指南请参考：[提示词系统使用指南](docs/prompt_system_guide.md)

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd AmagitbotV2

# 安装依赖
pip install -r requirements.txt

# 复制配置文件
cp .env.example .env
```

### 2. 配置设置

编辑 `.env` 文件：

```bash
# LLM API 配置（可选，使用mock提供商无需配置）
DEEPSEEK_API_KEY=your_deepseek_api_key_here
SILICONFLOW_API_KEY=your_siliconflow_api_key_here

# 默认使用mock提供商（无需API密钥）
DEFAULT_LLM_PROVIDER=mock

# 自定义机器人人格和提示词
PERSONALITY_PROMPTS=温柔体贴,善解人意,乐于助人,有耐心,富有同理心
LANGUAGE_STYLE_PROMPTS=语气温和,用词亲切,表达自然,避免生硬,多用感叹词
```

### 3. 启动服务

```bash
# 启动Web服务
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 或使用控制台聊天
python console_chat.py
```

## 🎮 使用方法

### Web API

```bash
# 发送聊天消息
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好",
    "user_id": "user123",
    "llm_provider": "mock",
    "personality_type": "gentle"
  }'

# 查看提示词配置
curl "http://localhost:8000/config" | jq .prompt_config
```

### 控制台聊天

```bash
python console_chat.py

# 可用命令：
/help          # 查看帮助
/prompts       # 查看提示词配置
/personality   # 切换人格类型
/provider      # 切换LLM提供商
/thinking      # 切换思维链显示
/botname       # 设置机器人名字
/botstyle      # 自定义说话风格
```

## 🎭 人格类型

支持8种不同的人格类型：

- **gentle** - 温柔型：温和、耐心、善良
- **rational** - 理性型：逻辑、客观、分析
- **humorous** - 幽默型：风趣、活泼、机智
- **caring** - 关怀型：关心、共情、支持
- **outgoing** - 外向型：热情、积极、社交
- **creative** - 创造型：想象、灵感、艺术
- **analytical** - 分析型：细致、专业、系统
- **empathetic** - 共情型：理解、感知、同理

## 🛠️ 技术架构

```
├── core/                   # 核心模块
│   ├── chatbot.py         # 聊天机器人核心控制器
│   ├── config.py          # 配置管理
│   ├── prompt_manager.py  # 提示词管理器
│   └── logger.py          # 日志系统
├── llm/                   # LLM接口模块
│   ├── base.py           # 基础接口定义
│   ├── factory.py        # LLM工厂
│   ├── deepseek.py       # DeepSeek接口
│   ├── siliconflow.py    # SiliconFlow接口
│   └── mock.py           # 模拟LLM（用于演示）
├── emotion/              # 情感分析模块
├── memory/               # 记忆管理模块
├── persona/              # 人格管理模块
├── rag/                  # 知识库模块
└── docs/                 # 文档
```

## 📊 API文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔧 高级配置

### 专业助手配置示例

```bash
PERSONALITY_PROMPTS=专业严谨,知识渊博,逻辑清晰,客观公正,深度思考
LANGUAGE_STYLE_PROMPTS=用词准确,表达清晰,逻辑严密,条理分明,专业术语适度
EMOTION_EXPRESSION_PROMPTS=情绪稳定,表达克制,理性回应,保持专业,适度共情
CONVERSATION_BEHAVIOR_PROMPTS=深入分析,提供建议,系统思考,专业解答,客观评价
ROLE_SPECIFIC_PROMPTS=专业素养,知识权威,解答准确,思路清晰,负责任态度
FORBIDDEN_BEHAVIORS=避免情绪化,不要主观臆断,拒绝不准确信息,避免过度承诺
```

### 陪伴聊天配置示例

```bash
PERSONALITY_PROMPTS=温暖亲切,善解人意,乐观开朗,富有同理心,真诚友善
LANGUAGE_STYLE_PROMPTS=语气轻松,用词亲切,表达自然,多用感叹词,充满温度
EMOTION_EXPRESSION_PROMPTS=情感丰富,善于共情,真诚回应,温暖人心,感染力强
CONVERSATION_BEHAVIOR_PROMPTS=主动关心,耐心倾听,给予鼓励,分享快乐,陪伴支持
ROLE_SPECIFIC_PROMPTS=贴心陪伴,情感支持,温暖如家,细致关怀,真诚友谊
FORBIDDEN_BEHAVIORS=不要冷漠,避免说教,拒绝敷衍,不要忽视情感,避免机械回复
```

## 📝 开发指南

### 添加新的提示词类型

1. 在 `core/config.py` 中添加环境变量配置
2. 在 `core/prompt_manager.py` 中添加处理逻辑
3. 在 `main.py` 的配置API中添加返回
4. 更新 `.env` 和 `.env.example` 文件

### 添加新的LLM提供商

1. 在 `llm/` 目录下创建新的提供商文件
2. 继承 `BaseLLM` 类并实现接口
3. 在 `llm/factory.py` 中注册新提供商

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- 感谢所有贡献者的支持
- 感谢开源社区提供的优秀工具和库

---

**让AI更有温度，让对话更有灵魂** ❤️