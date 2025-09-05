/**
 * API配置文件
 * 用于统一管理API地址和环境切换
 */

// 环境配置
const ENV_CONFIG = {
  // 开发环境
  development: {
    name: '开发环境',
    baseURL: 'http://127.0.0.1:8000/api/v1',
    wsURL: 'ws://127.0.0.1:8000/ws',
    enableMock: false, // 是否启用Mock数据
    timeout: 10000
  },
  
  // 本地Mock环境 (用于纯前端开发和调试)
  mock: {
    name: 'Mock环境',
    baseURL: '',
    wsURL: '',
    enableMock: true, // 启用Mock数据
    timeout: 1000
  },
  
  // 生产环境
  production: {
    name: '生产环境',
    baseURL: 'https://api.lawchat.com/api/v1',
    wsURL: 'wss://api.lawchat.com/ws',
    enableMock: false,
    timeout: 15000
  }
}

// 当前环境 - 可以通过环境变量或者手动切换
const getCurrentEnv = () => {
  // 优先从环境变量读取
  // #ifdef H5
  if (process.env.NODE_ENV === 'production') {
    return 'production'
  }
  // #endif
  
  // 从本地存储读取用户设置的环境
  const savedEnv = uni.getStorageSync('debug_env')
  if (savedEnv && ENV_CONFIG[savedEnv]) {
    return savedEnv
  }
  
  // 默认环境
  // #ifdef H5
  return 'development'
  // #endif
  
  // #ifndef H5
  return 'development'
  // #endif
}

// 当前配置
export const currentEnv = getCurrentEnv()
export const config = ENV_CONFIG[currentEnv]

/**
 * 切换环境（仅开发阶段使用）
 * @param {string} env 环境名称
 */
export const switchEnv = (env) => {
  if (ENV_CONFIG[env]) {
    uni.setStorageSync('debug_env', env)
    uni.showToast({
      title: `已切换到${ENV_CONFIG[env].name}`,
      icon: 'success'
    })
    
    // 提示重启应用
    setTimeout(() => {
      uni.showModal({
        title: '环境切换',
        content: '环境已切换，建议重启应用以确保生效',
        confirmText: '重启',
        success: (res) => {
          if (res.confirm) {
            // #ifdef H5
            window.location.reload()
            // #endif
            
            // #ifndef H5
            uni.reLaunch({
              url: '/pages/index/index'
            })
            // #endif
          }
        }
      })
    }, 1000)
  }
}

/**
 * 获取所有可用环境
 */
export const getAvailableEnvs = () => {
  return Object.keys(ENV_CONFIG).map(key => ({
    key,
    name: ENV_CONFIG[key].name,
    current: key === currentEnv
  }))
}

/**
 * API端点配置
 */
export const API_ENDPOINTS = {
  // 认证相关
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    REFRESH: '/auth/refresh',
    LOGOUT: '/auth/logout',
    PROFILE: '/auth/profile',
    CHANGE_PASSWORD: '/auth/change-password'
  },
  
  // 用户相关
  USER: {
    PROFILE: '/users/profile',
    UPDATE_PROFILE: '/users/profile',
    AVATAR_UPLOAD: '/users/avatar'
  },
  
  // 律师相关
  LAWYER: {
    LIST: '/lawyers',
    DETAIL: '/lawyers/{id}',
    SEARCH: '/lawyers/search',
    FILTERS: '/lawyers/filters'
  },
  
  // 聊天相关
  CHAT: {
    ROOMS: '/chat/rooms',
    MESSAGES: '/chat/rooms/{roomId}/messages',
    SEND_MESSAGE: '/chat/message',
    AI_CONVERSATION: '/chat/ai/conversation'
  },
  
  // 案例相关
  CASE: {
    LIST: '/cases',
    DETAIL: '/cases/{id}',
    CREATE: '/cases',
    UPDATE: '/cases/{id}',
    DELETE: '/cases/{id}'
  }
}

export default {
  config,
  currentEnv,
  switchEnv,
  getAvailableEnvs,
  API_ENDPOINTS
}