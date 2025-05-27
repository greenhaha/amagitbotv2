# 聊天机器人使用指南

## 🚀 快速开始

### 1. 启动系统

```bash
# 启动聊天机器人服务
python3 main.py
```

服务将在 `http://localhost:8000` 启动

### 2. 检查系统状态

```bash
# 检查系统健康状态
curl http://localhost:8000/health

# 查看系统信息
curl http://localhost:8000/
```

## 💬 聊天对话方式

### 方式一：使用 curl 命令

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好！我今天心情很好",
    "user_id": "your_user_id",
    "personality_type": "gentle",
    "enable_thinking": true
  }'
```

### 方式二：使用测试脚本

```bash
# 运行交互式聊天工具
python3 test_chat.py
```

选择模式：
- **1. 演示对话** - 自动演示不同人格的对话效果
- **2. 交互式聊天** - 与机器人实时对话
- **3. 系统状态检查** - 查看系统运行状态

### 方式三：使用 Python 代码

```python
import requests

def chat_with_bot(message, user_id="demo_user", personality="gentle"):
    url = "http://localhost:8000/chat"
    payload = {
        "message": message,
        "user_id": user_id,
        "personality_type": personality,
        "enable_thinking": True
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        result = response.json()
        print(f"机器人回复: {result['response']}")
        return result
    else:
        print(f"错误: {response.text}")
        return None

# 示例使用
chat_with_bot("你好，今天天气不错")
```

## 🎭 人格类型

系统支持8种不同的人格类型：

| 人格类型 | 描述 | 适用场景 |
|---------|------|----------|
| `gentle` | 温柔、耐心、富有同理心 | 日常聊天、情感支持 |
| `rational` | 理性、逻辑性强 | 问题分析、决策建议 |
| `humorous` | 幽默、风趣 | 轻松聊天、娱乐互动 |
| `outgoing` | 外向、热情 | 积极交流、鼓励激励 |
| `caring` | 关怀、支持性强 | 心理安慰、贴心服务 |
| `creative` | 富有创造力、想象力 | 创意讨论、头脑风暴 |
| `analytical` | 分析性强、注重细节 | 技术问题、深度分析 |
| `empathetic` | 高度共情、情感智能 | 情感交流、心理支持 |

### 查看可用人格

```bash
curl http://localhost:8000/personalities
```

## 📝 API 接口

### 1. 聊天接口

**POST** `/chat`

请求参数：
```json
{
  "message": "用户消息",
  "user_id": "用户ID",
  "session_id": "会话ID（可选）",
  "personality_type": "人格类型（可选）",
  "enable_thinking": true,
  "llm_provider": "LLM提供商（可选）"
}
```

响应示例：
```json
{
  "response": "机器人回复 😊",
  "session_id": "会话ID",
  "thinking_process": ["思维步骤1", "思维步骤2"],
  "emotion_analysis": {
    "emotion": "joy",
    "confidence": 0.85,
    "emoji": "😊",
    "description": "检测到积极愉快的情绪"
  },
  "persona_state": {
    "personality_type": "gentle",
    "mood": "happy",
    "energy_level": 0.9,
    "main_traits": {
      "empathy": 0.9,
      "warmth": 0.8
    }
  },
  "relevant_memories": [],
  "knowledge_base_action": "stored"
}
```

### 2. 会话摘要

**GET** `/session/{user_id}/{session_id}/summary`

### 3. 重置人格

**POST** `/session/{user_id}/{session_id}/reset-persona?personality_type=gentle`

### 4. 系统信息

```bash
# 获取可用人格类型
GET /personalities

# 获取可用LLM提供商
GET /llm-providers

# 健康检查
GET /health
```

## 🔧 配置说明

### 环境变量配置

创建 `.env` 文件：

```bash
# 复制示例配置
cp env_example.txt .env

# 编辑配置文件
nano .env
```

主要配置项：

```env
# LLM API 配置（需要配置至少一个）
DEEPSEEK_API_KEY=your_deepseek_api_key_here
SILICONFLOW_API_KEY=your_siliconflow_api_key_here

# 默认LLM提供商
DEFAULT_LLM_PROVIDER=deepseek

# MongoDB 配置
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=chatbot_db

# 日志级别
LOG_LEVEL=INFO
```

### 启动 MongoDB

```bash
# 使用 Docker 启动 MongoDB
docker run -d -p 27017:27017 --name chatbot-mongo mongo:latest

# 或使用本地 MongoDB
mongod --dbpath /path/to/your/db
```

## 🎯 使用示例

### 基础对话

```bash
# 温柔人格聊天
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "我今天心情不太好",
    "user_id": "user123",
    "personality_type": "empathetic"
  }'
```

### 技术问题咨询

```bash
# 分析型人格处理技术问题
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "如何优化数据库查询性能？",
    "user_id": "user123",
    "personality_type": "analytical",
    "enable_thinking": true
  }'
```

### 轻松聊天

```bash
# 幽默人格轻松互动
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "讲个笑话给我听",
    "user_id": "user123",
    "personality_type": "humorous"
  }'
```

## 🔍 功能特性

### 1. 智能对话系统
- 支持 DeepSeek 和 SiliconFlow API
- 动态模型切换
- 思维链推理过程展示

### 2. 情感分析
- 9种情感类型识别
- 情感置信度评估
- 自动表情符号匹配

### 3. 动态人格系统
- 8种人格类型
- 根据用户情感动态调整
- 人格状态持久化

### 4. 记忆系统
- MongoDB 持久化存储
- 对话历史记录
- 上下文理解

### 5. 知识库学习
- 向量化存储
- 语义检索
- 相关记忆关联

## 🐛 故障排除

### 常见问题

1. **服务启动失败**
   ```bash
   # 检查端口占用
   lsof -i :8000
   
   # 检查依赖安装
   pip install -r requirements.txt
   ```

2. **API 调用失败**
   ```bash
   # 检查 API 密钥配置
   cat .env | grep API_KEY
   
   # 检查服务状态
   curl http://localhost:8000/health
   ```

3. **MongoDB 连接失败**
   ```bash
   # 检查 MongoDB 服务
   docker ps | grep mongo
   
   # 检查连接配置
   cat .env | grep MONGODB
   ```

### 日志查看

```bash
# 查看实时日志
tail -f logs/chatbot_$(date +%Y-%m-%d).log

# 查看错误日志
grep ERROR logs/chatbot_$(date +%Y-%m-%d).log
```

## 📚 更多资源

- [API 文档](http://localhost:8000/docs) - 启动服务后访问
- [项目 README](README.md) - 详细技术文档
- [演示脚本](demo.py) - 完整功能演示
- [测试用例](tests/) - 单元测试示例

---

🎉 **开始与您的智能聊天机器人对话吧！** 