

This project is a front-end project based on the UniApp framework, built using Vue3 and Vite. Below is a brief description and user guide for the project:

---

## 🌟 Project Overview

This is a UniApp project utilizing the Vue3 and Vite technology stack, suitable for cross-platform development (such as WeChat Mini Programs, H5, etc.). The project includes multiple page modules (home, product, service, order, user, etc.), along with commonly used utility and storage management modules.

---

## 📦 Key Functional Modules

- **Vue3 + Vite**: Modern front-end framework and build tool.
- **Page Components**: Includes multiple page components such as home, login, order, product, service, etc.
- **State Management**: Uses `store` to manage global and user states.
- **Map Functionality**: Integrates the Tencent Map WeChat Mini Program SDK (`qqmap-wx-jssdk.js`).
- **Network Requests**: Encapsulates the `request` module, supporting encrypted requests (SM2/SM3/SM4).
- **Local Storage**: Uses `localStorage` for managing local caches.

---

## 🛠️ Development Environment Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Start the Local Development Server

```bash
npm run dev
```

### 3. Build a Production Version

```bash
npm run build
```

---

## 📁 Project Structure

```
src/
├── App.vue             # Application root component
├── main.js             # Application entry point
├── pages/              # Page component directory
│   ├── index/          # Home page module
│   ├── login/          # Login page
│   └── ...             # Other page modules
├── components/         # Reusable components
├── store/              # Vuex state management module
├── utils/              # Utility modules
│   ├── request/        # Network request encapsulation
│   ├── localStorage.js # Local storage utility
│   └── utils.js        # Common utility functions
├── static/             # Static resource directory (images, map SDKs, etc.)
└── uni.scss            # Global style file
```

---

## 📡 Network Request Description

The project uses `src/utils/request/index.js` as the encapsulated request module, which supports encrypted requests provided by `src/utils/request/crypto.js`.

### Example Request

```javascript
import { request } from '@/utils/request/index'

request.get('/api/data').then(res => {
  console.log(res)
})
```

---

## 🗺️ Map Functionality

The project integrates the Tencent Map SDK (`qqmap-wx-jssdk.js`) and supports the following features:

- Location search
- Geocoding and reverse geocoding
- City/region list retrieval
- Distance calculation
- Route planning

---

## 📄 State Management

`Vuex` is used for state management, including the following modules:

- `global.js`: Global state
- `user.js`: User state

---

## 📜 License

This project is licensed under the MIT License. Please comply with the relevant open-source agreements.

---

## 🤝 Contribution Guidelines

We welcome pull requests and issue submissions. Please follow the project's coding standards and ensure code quality.

---

## 📞 Contact & Support

For any questions, please contact [yang19941208](https://gitee.com/yang19941208).

---

Thank you for using the uniapp-vite-vue3 project! 🚀