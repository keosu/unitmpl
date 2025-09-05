/**
 * 应用配置初始化
 */

import { config, currentEnv } from './api.js'

/**
 * 初始化应用配置
 */
export const initConfig = () => {
  // 设置当前环境信息
  console.log(`[应用启动] 当前环境: ${config.name}`)
  console.log(`[应用启动] API地址: ${config.baseURL || 'Mock数据'}`)
  console.log(`[应用启动] Mock模式: ${config.enableMock ? '开启' : '关闭'}`)
  
  // 开发环境下的额外配置
  if (currentEnv === 'development' || currentEnv === 'mock') {
    // 开发环境配置
    console.log('[开发模式] 已启用开发调试功能')
  }
  
  // 生产环境配置
  if (currentEnv === 'production') {
    // 生产环境配置
    console.log('[生产模式] 已启用生产环境优化')
  }
}

/**
 * 获取当前配置
 */
export const getConfig = () => config

/**
 * 获取当前环境
 */
export const getEnv = () => currentEnv

export default {
  initConfig,
  getConfig,
  getEnv
}