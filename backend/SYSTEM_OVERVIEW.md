# 🏛️ 法律咨询应用 - 后端系统架构

## 📋 系统概述

基于 **FastAPI + SQLModel** 构建的现代化法律咨询平台后端系统，提供完整的用户管理、律师服务、案例管理和AI聊天功能。

## 🏗️ 技术栈

### 核心框架
- **FastAPI 0.104.1** - 现代化Python Web框架
- **SQLModel 0.0.14** - 类型安全的ORM框架
- **Uvicorn 0.24.0** - ASGI服务器
- **Pydantic 2.5.0** - 数据验证和序列化

### 数据库
- **PostgreSQL** - 主数据库（通过asyncpg异步驱动）
- **Redis 5.0.1** - 缓存和会话存储
- **Alembic 1.13.0** - 数据库迁移工具

### 认证与安全
- **PyJWT 2.8.0** - JWT令牌管理
- **Passlib + Bcrypt** - 密码加密
- **OAuth2 + Bearer Token** - API认证

### 其他工具
- **Celery 5.3.4** - 异步任务队列
- **WebSockets 12.0** - 实时通信
- **Docker** - 容器化部署

## 📁 项目结构

```
backend/
├── app/
│   ├── __init__.py           # 应用初始化
│   ├── main.py              # FastAPI应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   │
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   ├── base.py         # 基础模型
│   │   ├── user.py         # 用户模型
│   │   ├── lawyer.py       # 律师模型
│   │   ├── case.py         # 案例模型
│   │   └── chat.py         # 聊天模型
│   │
│   ├── schemas/             # Pydantic数据模型
│   │   ├── __init__.py
│   │   ├── common.py       # 通用模型
│   │   ├── auth.py         # 认证模型
│   │   ├── user.py         # 用户模型
│   │   ├── lawyer.py       # 律师模型
│   │   ├── case.py         # 案例模型
│   │   └── chat.py         # 聊天模型
│   │
│   ├── api/                 # API路由
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py     # 认证API
│   │       ├── users.py    # 用户API
│   │       ├── lawyers.py  # 律师API
│   │       ├── cases.py    # 案例API
│   │       └── chat.py     # 聊天API
│   │
│   ├── services/            # 业务逻辑服务
│   │   └── __init__.py
│   │
│   └── utils/              # 工具模块
│       ├── __init__.py
│       ├── dependencies.py # 依赖注入
│       └── exceptions.py   # 异常处理
│
├── requirements.txt         # Python依赖
├── Dockerfile              # Docker配置
├── docker-compose.yml      # Docker Compose配置
├── .env.example           # 环境变量示例
└── README.md              # 项目说明
```

## 🗄️ 数据模型设计

### 👥 用户系统
- **User** - 用户基本信息
  - 角色：admin（管理员）、lawyer（律师）、user（普通用户）
  - 状态：active、inactive、suspended、banned
- **UserPreferences** - 用户偏好设置
- **UserSession** - 用户会话记录

### ⚖️ 律师系统
- **Lawyer** - 律师专业信息
  - 执业证号、律师协会、专业领域
  - 级别：junior、intermediate、senior、partner
- **LawyerSpecialty** - 专业领域分类
- **LawyerCertification** - 资质认证
- **LawyerReview** - 律师评价

### 📋 案例系统
- **Case** - 法律案例核心信息
  - 类型：民事、刑事、行政、经济等
  - 状态：草稿、进行中、已完成等
  - 优先级：低、中、高、紧急
- **CaseDocument** - 案例文档
- **CaseUpdate** - 案例更新记录
- **CaseTemplate** - 案例模板

### 💬 聊天系统
- **ChatRoom** - 聊天室
  - 类型：私聊、AI对话、群聊、咨询等
- **ChatMessage** - 聊天消息
  - 支持文本、图片、文件、Markdown等格式
- **AIConversation** - AI对话会话
- **MessageReaction** - 消息反应
- **ChatSettings** - 聊天设置

## 🔌 API接口设计

### 🔐 认证模块 (`/api/v1/auth`)
- `POST /login` - 用户登录
- `POST /register` - 用户注册
- `POST /refresh` - 刷新令牌
- `POST /logout` - 用户登出
- `GET /me` - 获取当前用户信息
- `POST /change-password` - 修改密码

### 👤 用户管理 (`/api/v1/users`)
- `GET /users` - 获取用户列表
- `POST /users` - 创建用户
- `GET /users/{id}` - 获取用户详情
- `PUT /users/{id}` - 更新用户信息
- `DELETE /users/{id}` - 删除用户

### ⚖️ 律师管理 (`/api/v1/lawyers`)
- `GET /lawyers` - 获取律师列表
- `POST /lawyers` - 创建律师资料
- `GET /lawyers/{id}` - 获取律师详情
- `PUT /lawyers/{id}` - 更新律师信息
- `POST /lawyers/{id}/reviews` - 添加律师评价

### 📋 案例管理 (`/api/v1/cases`)
- `GET /cases` - 获取案例列表
- `POST /cases` - 创建案例
- `GET /cases/{id}` - 获取案例详情
- `PUT /cases/{id}` - 更新案例
- `POST /cases/{id}/documents` - 上传案例文档
- `POST /cases/{id}/updates` - 添加案例更新

### 💬 聊天服务 (`/api/v1/chat`)
- `POST /message` - 发送聊天消息（兼容前端mock API）
- `GET /rooms` - 获取聊天室列表
- `POST /rooms` - 创建聊天室
- `GET /rooms/{id}/messages` - 获取聊天记录
- `POST /ai/conversation` - 创建AI对话
- `GET /settings` - 获取聊天设置

## 🔒 安全特性

### JWT认证
- 访问令牌：30分钟有效期
- 刷新令牌：7天有效期
- 支持令牌刷新和撤销

### 数据验证
- Pydantic模型自动验证
- 输入数据类型检查
- SQL注入防护

### 权限控制
- 基于角色的访问控制（RBAC）
- API端点权限保护
- 数据访问权限验证

## 🌐 与前端集成

### 聊天API兼容性
- 完全兼容前端mock API格式
- 支持主题感知回复
- 支持Markdown格式响应
- 实时延迟模拟

### 响应格式
```json
{
  "success": true,
  "data": {
    "content": "AI回复内容",
    "timestamp": "2024-01-01T12:00:00Z",
    "format": "markdown",
    "metadata": {
      "ai_model": "legal-assistant-v1",
      "confidence": 0.95
    }
  }
}
```

## 🚀 部署指南

### 本地开发
```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
cp .env.example .env

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker部署
```bash
# 构建镜像
docker build -t lawchat-backend .

# 使用Docker Compose
docker-compose up -d
```

### 生产环境
- 使用PostgreSQL作为主数据库
- 配置Redis缓存
- 设置环境变量
- 启用HTTPS
- 配置负载均衡

## 📊 监控和日志

### 健康检查
- `GET /health` - 系统健康状态
- 数据库连接检查
- Redis连接检查

### 日志系统
- 结构化日志记录
- 请求/响应日志
- 错误日志和异常追踪

### 性能监控
- API响应时间监控
- 数据库查询性能
- 内存和CPU使用率

## 🔧 开发工具

### 代码质量
- **Black** - 代码格式化
- **isort** - import排序
- **Flake8** - 代码检查

### 测试
- **Pytest** - 单元测试框架
- **Pytest-asyncio** - 异步测试支持

### API文档
- 自动生成的OpenAPI文档：`/docs`
- ReDoc格式文档：`/redoc`

## 🔮 未来扩展

### 计划功能
- 文件上传和管理
- 邮件通知系统
- 短信验证
- 微信集成
- 在线支付
- 视频通话
- 文档智能分析

### 技术优化
- 数据库读写分离
- 微服务架构
- GraphQL支持
- 全文搜索（Elasticsearch）
- 消息队列优化

---

## 🎯 核心优势

✅ **现代化架构** - 基于FastAPI的异步高性能设计
✅ **类型安全** - SQLModel提供端到端类型检查
✅ **完整功能** - 覆盖用户、律师、案例、聊天全业务流程
✅ **标准化API** - RESTful设计，自动生成文档
✅ **高度兼容** - 与前端UniApp无缝集成
✅ **可扩展性** - 模块化设计，便于功能扩展
✅ **生产就绪** - 包含安全、监控、部署等完整方案

这个后端系统为法律咨询平台提供了坚实的技术基础，支持快速开发和灵活扩展。🚀