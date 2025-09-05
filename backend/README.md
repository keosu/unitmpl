# 后端 API 服务

基于 FastAPI 和 SQLModel 构建的法律咨询应用后端服务。

## 技术栈

- **FastAPI**: 现代、快速的 Web 框架
- **SQLModel**: 类型安全的 ORM（由 FastAPI 作者开发）
- **PostgreSQL**: 主数据库
- **Redis**: 缓存和会话存储
- **Pydantic**: 数据验证
- **Alembic**: 数据库迁移
- **JWT**: 认证授权

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 应用入口
│   ├── config.py               # 配置管理
│   ├── database.py             # 数据库连接
│   ├── models/                 # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py            # 用户模型
│   │   ├── case.py            # 案例模型
│   │   ├── lawyer.py          # 律师模型
│   │   ├── chat.py            # 聊天模型
│   │   └── base.py            # 基础模型
│   ├── api/                   # API 路由
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py        # 认证路由
│   │   │   ├── users.py       # 用户路由
│   │   │   ├── lawyers.py     # 律师路由
│   │   │   ├── cases.py       # 案例路由
│   │   │   └── chat.py        # 聊天路由
│   ├── schemas/               # Pydantic 模式
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── lawyer.py
│   │   ├── case.py
│   │   └── chat.py
│   ├── services/              # 业务逻辑
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── lawyer.py
│   │   ├── case.py
│   │   └── chat.py
│   ├── utils/                 # 工具函数
│   │   ├── __init__.py
│   │   ├── security.py        # 安全相关
│   │   ├── dependencies.py    # 依赖注入
│   │   └── exceptions.py      # 自定义异常
│   └── migrations/            # 数据库迁移文件
├── requirements.txt           # Python 依赖
├── docker-compose.yml         # Docker 配置
├── Dockerfile                 # Docker 镜像
├── .env.example              # 环境变量模板
└── README.md                 # 说明文档
```

## 安装和运行

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 配置环境变量：
   ```bash
   cp .env.example .env
   # 编辑 .env 文件
   ```

3. 运行数据库迁移：
   ```bash
   alembic upgrade head
   ```

4. 启动开发服务器：
   ```bash
   uvicorn app.main:app --reload
   ```

## API 文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 核心功能

- 用户认证和授权（JWT）
- 用户管理（普通用户、律师、管理员）
- 案例管理
- 实时聊天
- 文件上传
- 搜索功能
- 消息推送