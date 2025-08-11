

该项目是一个基于 UniApp 框架的前端项目，使用 Vue3 和 Vite 构建工具。以下是项目的简要说明和使用指南：

---

## 🌟 项目简介

这是一个 UniApp 项目，采用 Vue3 和 Vite 技术栈，适用于跨平台（如微信小程序、H5 等）开发。项目包含多个页面模块（主页、产品、服务、订单、用户等）以及常用工具模块和存储管理模块。

---

## 📦 主要功能模块

- **Vue3 + Vite**：现代化的前端框架和构建工具。
- **页面组件**：包含多个页面组件，如主页、登录、订单、产品、服务等。
- **状态管理**：使用 `store` 管理全局和用户状态。
- **地图功能**：集成腾讯地图微信小程序 SDK（`qqmap-wx-jssdk.js`）。
- **网络请求**：封装 `request` 模块，支持加密请求（SM2/SM3/SM4）。
- **本地存储**：使用 `localStorage` 管理本地缓存。

---

## 🛠️ 开发环境搭建

### 1. 安装依赖

```bash
npm install
```

### 2. 启动本地开发服务器

```bash
npm run dev
```

### 3. 构建生产版本

```bash
npm run build
```

---

## 📁 项目结构

```
src/
├── App.vue             # 应用根组件
├── main.js             # 应用入口
├── pages/              # 页面组件目录
│   ├── index/          # 首页模块
│   ├── login/          # 登录页
│   └── ...             # 其他页面模块
├── components/         # 可复用的组件
├── store/              # Vuex 状态管理模块
├── utils/              # 工具类模块
│   ├── request/        # 网络请求封装
│   ├── localStorage.js # 本地存储工具
│   └── utils.js        # 通用工具函数
├── static/             # 静态资源目录（图片、地图 SDK 等）
└── uni.scss            # 全局样式文件
```

---

## 📡 网络请求说明

项目中使用了 `src/utils/request/index.js` 作为请求封装，支持加密请求（由 `src/utils/request/crypto.js` 提供）。

### 示例请求

```javascript
import { request } from '@/utils/request/index'

request.get('/api/data').then(res => {
  console.log(res)
})
```

---

## 🗺️ 地图功能

项目集成了腾讯地图 SDK（`qqmap-wx-jssdk.js`），支持以下功能：

- 地点搜索
- 地理编码与逆地理编码
- 城市/地区列表获取
- 距离计算
- 路线规划

---

## 📄 状态管理

使用 `Vuex` 管理状态，包含以下模块：

- `global.js`：全局状态
- `user.js`：用户状态

---

## 📜 许可证

本项目采用 MIT 许可证，请遵守相关开源协议。

---

## 🤝 贡献指南

欢迎提交 PR 和 Issue，遵循项目代码规范并确保代码质量。

---

## 📞 联系与支持

如有任何问题，请联系 [yang19941208](https://gitee.com/yang19941208)。

--- 

感谢使用 uniapp-vite-vue3 项目！🚀