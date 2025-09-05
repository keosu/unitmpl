# 📡 前后端API集成指南

## 🎯 概述

本项目已完成前后端API的统一集成，支持Mock和真实API的无缝切换，方便本地开发和生产部署。

## 🏗️ 架构设计

### 配置层
- `src/config/api.js` - API环境配置
- `src/config/index.js` - 应用配置初始化

### 网络层  
- `src/api/http.js` - 统一HTTP请求工具
- `src/api/authService.js` - 认证服务API
- `src/api/chatService-v2.js` - 聊天服务API

### UI层
- `src/components/EnvSwitcher.vue` - 环境切换组件

## 🔧 环境配置

### 可用环境

```javascript
const ENV_CONFIG = {
  // 开发环境 - 连接后端API
  development: {
    baseURL: 'http://127.0.0.1:8000/api/v1',
    enableMock: false
  },
  
  // Mock环境 - 使用模拟数据
  mock: {
    baseURL: '',
    enableMock: true
  },
  
  // 生产环境
  production: {
    baseURL: 'https://api.lawchat.com/api/v1',
    enableMock: false
  }
}
```

### 环境切换

#### 方法1：通过UI组件（推荐）
1. 在应用右上角点击"🔧"按钮
2. 选择目标环境
3. 重启应用生效

#### 方法2：通过代码
```javascript
import { switchEnv } from '@/config/api.js'
switchEnv('development') // 切换到开发环境
```

#### 方法3：通过存储
```javascript
uni.setStorageSync('debug_env', 'mock')
```

## 🔌 API服务使用

### 认证服务

```javascript
import { authAPI } from '@/api/authService.js'

// 登录
const result = await authAPI.login('username', 'password')
if (result.success) {
  console.log('登录成功:', result.data)
}

// 注册
const registerResult = await authAPI.register({
  username: 'test',
  password: '123456',
  email: 'test@example.com'
})

// 检查登录状态
if (authAPI.isLoggedIn()) {
  console.log('用户已登录')
}

// 退出登录
await authAPI.logout()
```

### 聊天服务

```javascript
import { chatAPI } from '@/api/chatService-v2.js'

// 发送消息
const response = await chatAPI.sendMessage('你好', {
  theme: 'light'
})

if (response.success) {
  console.log('AI回复:', response.data.content)
}

// 获取聊天室列表
const rooms = await chatAPI.getChatRooms()

// 获取聊天记录
const messages = await chatAPI.getChatMessages('room_id')
```

## 📋 API端点映射

### 认证相关
- `POST /auth/login` - 用户登录
- `POST /auth/register` - 用户注册  
- `POST /auth/refresh` - 刷新Token
- `GET /users/profile` - 获取用户信息

### 聊天相关
- `POST /chat/message` - 发送消息
- `GET /chat/rooms` - 获取聊天室列表
- `GET /chat/rooms/{roomId}/messages` - 获取聊天记录
- `POST /chat/ai/conversation` - 创建AI对话

### 律师相关
- `GET /lawyers` - 获取律师列表
- `GET /lawyers/{id}` - 获取律师详情
- `POST /lawyers/search` - 搜索律师

## 🔄 Mock与真实API切换

### 自动切换逻辑

```javascript
// 在API服务中自动判断
if (config.enableMock) {
  // 使用Mock数据
  return mockAPI()
} else {
  // 使用真实API
  return http.post('/api/endpoint')
}
```

### Mock数据格式

Mock数据完全按照后端API响应格式设计：

```javascript
// 统一响应格式
{
  success: true,
  data: { /* 实际数据 */ },
  message: '操作成功'
}

// 错误响应格式  
{
  success: false,
  message: '错误信息',
  error_code: 'ERROR_CODE'
}
```

## 🚀 启动配置

### 开发环境启动

1. **启动后端服务**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

2. **启动前端应用**
```bash
pnpm dev:h5
```

3. **切换到开发环境**
- 点击右上角🔧按钮
- 选择"开发环境"
- 重启应用

### 纯前端开发

1. **启动前端应用**
```bash
pnpm dev:h5
```

2. **切换到Mock环境**
- 点击右上角🔧按钮
- 选择"Mock环境" 
- 重启应用

## 🔒 认证机制

### Token管理

- **存储**: 自动存储到 `localStorage`
- **刷新**: 自动处理Token过期和刷新
- **清除**: 登出时自动清除

### 请求拦截

```javascript
// 自动添加认证头
const token = getLocal('token')
if (token) {
  headers['Authorization'] = `Bearer ${token}`
}
```

### 错误处理

```javascript
// 401自动跳转登录
if (error.statusCode === 401) {
  removeLocal('token')
  uni.reLaunch({ url: '/pages/login/login' })
}
```

## 🐛 调试功能

### 环境信息显示

```javascript
// 在控制台查看当前环境
console.log(`当前环境: ${config.name}`)
console.log(`API地址: ${config.baseURL}`)  
console.log(`Mock模式: ${config.enableMock}`)
```

### 请求日志

所有API请求都会在控制台输出详细日志：

```
[开发环境] 请求: POST http://127.0.0.1:8000/api/v1/auth/login
[开发环境] 响应: 200 {success: true, data: {...}}
```

### 错误追踪

完整的错误堆栈和请求信息记录。

## 📦 生产部署

### 环境配置

1. **修改生产API地址**
```javascript
// src/config/api.js
production: {
  baseURL: 'https://your-api-domain.com/api/v1',
  enableMock: false
}
```

2. **构建生产版本**
```bash
pnpm build:h5
```

3. **自动切换到生产环境**
生产构建时会自动使用production配置。

## 🔧 自定义扩展

### 添加新的API服务

1. **创建服务文件**
```javascript
// src/api/newService.js
import { config, API_ENDPOINTS } from '@/config/api.js'
import { http } from '@/api/http.js'

export const newAPI = {
  async getData() {
    if (config.enableMock) {
      return mockData()
    } else {
      return http.get('/new/endpoint')
    }
  }
}
```

2. **添加端点配置**
```javascript
// src/config/api.js
API_ENDPOINTS: {
  NEW: {
    DATA: '/new/data'
  }
}
```

### 添加新环境

```javascript
// src/config/api.js
const ENV_CONFIG = {
  // 新增测试环境
  testing: {
    name: '测试环境',
    baseURL: 'http://test-api.domain.com/api/v1',
    enableMock: false
  }
}
```

## ⚠️ 注意事项

1. **环境切换后需重启应用**
2. **Mock数据仅用于前端开发调试**
3. **生产环境禁用环境切换功能**
4. **确保API响应格式一致**
5. **Token自动管理，无需手动处理**

## 📞 技术支持

如有问题，请参考：
1. 检查网络连接
2. 确认后端服务启动
3. 查看控制台日志
4. 验证API端点地址
5. 检查Token是否有效

---

*此文档随项目更新，请保持关注最新版本。*