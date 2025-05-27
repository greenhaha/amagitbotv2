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