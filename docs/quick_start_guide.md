# 快速使用指南

## 🚀 5分钟快速上手

### 1. 基础设置

```bash
# 1. 克隆项目
git clone <repository-url>
cd AmagitbotV2

# 2. 安装依赖
pip install -r requirements.txt

# 3. 复制配置文件
cp env_example.txt .env
```

### 2. 配置API密钥

编辑 `.env` 文件，添加你的API密钥：

```bash
# 至少配置一个API密钥
DEEPSEEK_API_KEY=your_deepseek_api_key_here
# 或
SILICONFLOW_API_KEY=your_siliconflow_api_key_here
```

### 3. 自定义你的机器人（可选）

在 `.env` 文件中添加机器人个性化配置：

```bash
# 基本信息
DEFAULT_BOT_NAME=小雪
DEFAULT_BOT_DESCRIPTION=我是小雪，一个温柔的AI助手
DEFAULT_BOT_PERSONALITY=caring

# 说话风格
DEFAULT_USE_CAT_SPEECH=false
DEFAULT_FORMALITY_LEVEL=0.5
DEFAULT_ENTHUSIASM_LEVEL=0.7
DEFAULT_CUTENESS_LEVEL=0.6
```

### 4. 启动服务

```bash
# 启动MongoDB（如果没有运行）
docker run -d -p 27017:27017 --name chatbot-mongo mongo:latest

# 启动聊天机器人服务
python main.py
```

### 5. 开始聊天

#### 方式1：控制台聊天

```bash
python console_chat.py
```

#### 方式2：API调用

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好",
    "user_id": "user123"
  }'
```

#### 方式3：Web界面

访问 http://localhost:8000/docs 使用Swagger UI

## 🎯 常用命令

### 控制台聊天命令

```bash
/help          # 查看帮助
/config        # 查看环境配置
/botinfo       # 查看机器人档案
/botname 新名字 # 修改机器人名字
/botstyle      # 自定义说话风格
/personality gentle # 切换人格类型
/provider siliconflow # 切换LLM提供商
```

### API接口

```bash
# 查看机器人档案
GET /bot-profile/{user_id}

# 更新机器人名字
PUT /bot-profile/{user_id}/name
{"bot_name": "新名字"}

# 查看环境配置
GET /config

# 查看可用人格类型
GET /personalities

# 查看可用LLM提供商
GET /llm-providers
```

## 🎨 个性化配置示例

### 温柔型助手

```bash
DEFAULT_BOT_NAME=小雪
DEFAULT_BOT_PERSONALITY=caring
DEFAULT_USE_CAT_SPEECH=false
DEFAULT_FORMALITY_LEVEL=0.5
DEFAULT_ENTHUSIASM_LEVEL=0.7
DEFAULT_CUTENESS_LEVEL=0.6
```

### 理性型分析师

```bash
DEFAULT_BOT_NAME=阿尔法
DEFAULT_BOT_PERSONALITY=analytical
DEFAULT_USE_CAT_SPEECH=false
DEFAULT_FORMALITY_LEVEL=0.8
DEFAULT_ENTHUSIASM_LEVEL=0.4
DEFAULT_CUTENESS_LEVEL=0.2
```

### 幽默型伙伴

```bash
DEFAULT_BOT_NAME=小丑
DEFAULT_BOT_PERSONALITY=humorous
DEFAULT_USE_CAT_SPEECH=false
DEFAULT_FORMALITY_LEVEL=0.2
DEFAULT_ENTHUSIASM_LEVEL=0.9
DEFAULT_CUTENESS_LEVEL=0.7
```

### 经典猫耳女仆

```bash
DEFAULT_BOT_NAME=天城
DEFAULT_BOT_PERSONALITY=gentle
DEFAULT_USE_CAT_SPEECH=true
DEFAULT_FORMALITY_LEVEL=0.3
DEFAULT_ENTHUSIASM_LEVEL=0.8
DEFAULT_CUTENESS_LEVEL=0.9
```

## 🔧 故障排除

### 常见问题

1. **MongoDB连接失败**
   ```bash
   # 检查MongoDB是否运行
   docker ps | grep mongo
   # 或启动MongoDB
   docker run -d -p 27017:27017 --name chatbot-mongo mongo:latest
   ```

2. **API密钥错误**
   ```bash
   # 检查.env文件中的API密钥是否正确
   cat .env | grep API_KEY
   ```

3. **配置不生效**
   ```bash
   # 重启服务以加载新配置
   # Ctrl+C 停止服务，然后重新运行
   python main.py
   ```

4. **查看当前配置**
   ```bash
   # 在控制台聊天中输入
   /config
   # 或通过API查看
   curl http://localhost:8000/config
   ```

### 日志查看

服务运行时会输出详细日志，包括：
- 配置加载信息
- API调用状态
- 错误信息

## 📚 更多资源

- [完整配置指南](bot_configuration.md)
- [API文档](http://localhost:8000/docs)
- [项目README](../README.md)

## 💡 小贴士

1. **配置优先级**：环境变量 > .env文件 > 默认值
2. **配置生效**：修改配置后需要重启服务
3. **个人定制**：每个用户可以独立定制自己的机器人档案
4. **备份配置**：建议备份你的.env配置文件
5. **测试配置**：使用 `/config` 命令验证配置是否正确加载 