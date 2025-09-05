/**
 * 统一HTTP请求工具
 * 支持Mock和真实API的无缝切换
 */

import { config } from '@/config/api.js'
import { getLocal, setLocal, removeLocal } from '@/utils/localStorage.js'

/**
 * 请求拦截器
 */
const requestInterceptor = (options) => {
  // 添加认证token
  const token = getLocal('token')
  if (token) {
    options.header = {
      ...options.header,
      'Authorization': `Bearer ${token}`
    }
  }
  
  // 添加基础URL
  if (!options.url.startsWith('http') && config.baseURL) {
    options.url = config.baseURL + options.url
  }
  
  // 设置超时时间
  options.timeout = options.timeout || config.timeout
  
  // 显示加载提示
  if (options.showLoading !== false) {
    uni.showLoading({
      title: '加载中...',
      mask: true
    })
  }
  
  console.log(`[${config.name}] 请求:`, options.method, options.url)
  
  return options
}

/**
 * 响应拦截器
 */
const responseInterceptor = (response, originalOptions) => {
  uni.hideLoading()
  
  const { statusCode, data } = response
  
  console.log(`[${config.name}] 响应:`, statusCode, data)
  
  // 成功响应
  if (statusCode >= 200 && statusCode < 300) {
    return data
  }
  
  // 处理错误响应
  const error = new Error(`HTTP ${statusCode}`)
  error.statusCode = statusCode
  error.data = data
  throw error
}

/**
 * 错误处理器
 */
const errorHandler = (error, originalOptions) => {
  uni.hideLoading()
  
  console.error(`[${config.name}] 请求错误:`, error)
  
  let message = '网络请求失败'
  
  // 根据状态码显示不同错误信息
  if (error.statusCode) {
    switch (error.statusCode) {
      case 401:
        message = '登录已过期，请重新登录'
        // 清除token并跳转登录
        removeLocal('token')
        removeLocal('user')
        uni.reLaunch({
          url: '/pages/login/login'
        })
        break
      case 403:
        message = '权限不足'
        break
      case 404:
        message = '请求的资源不存在'
        break
      case 500:
        message = '服务器内部错误'
        break
      default:
        message = error.data?.message || error.message || `请求失败(${error.statusCode})`
    }
  } else if (error.errMsg) {
    // 网络错误
    if (error.errMsg.includes('timeout')) {
      message = '请求超时，请检查网络连接'
    } else if (error.errMsg.includes('fail')) {
      message = '网络连接失败，请检查网络设置'
    }
  }
  
  // 显示错误提示
  if (originalOptions.showError !== false) {
    uni.showToast({
      title: message,
      icon: 'none',
      duration: 2000
    })
  }
  
  throw error
}

/**
 * 通用请求方法
 */
const request = (options) => {
  return new Promise((resolve, reject) => {
    // 应用请求拦截器
    const finalOptions = requestInterceptor({
      method: 'GET',
      header: {
        'Content-Type': 'application/json'
      },
      ...options
    })
    
    uni.request({
      ...finalOptions,
      success: (response) => {
        try {
          const result = responseInterceptor(response, finalOptions)
          resolve(result)
        } catch (error) {
          errorHandler(error, finalOptions)
          reject(error)
        }
      },
      fail: (error) => {
        errorHandler(error, finalOptions)
        reject(error)
      }
    })
  })
}

/**
 * HTTP方法封装
 */
export const http = {
  /**
   * GET请求
   */
  get(url, params = {}, options = {}) {
    return request({
      url,
      method: 'GET',
      data: params,
      ...options
    })
  },
  
  /**
   * POST请求
   */
  post(url, data = {}, options = {}) {
    return request({
      url,
      method: 'POST',
      data,
      ...options
    })
  },
  
  /**
   * PUT请求
   */
  put(url, data = {}, options = {}) {
    return request({
      url,
      method: 'PUT',
      data,
      ...options
    })
  },
  
  /**
   * DELETE请求
   */
  delete(url, params = {}, options = {}) {
    return request({
      url,
      method: 'DELETE',
      data: params,
      ...options
    })
  },
  
  /**
   * 文件上传
   */
  upload(url, filePath, formData = {}, options = {}) {
    return new Promise((resolve, reject) => {
      const token = getLocal('token')
      const header = { ...options.header }
      
      if (token) {
        header['Authorization'] = `Bearer ${token}`
      }
      
      const finalUrl = url.startsWith('http') ? url : config.baseURL + url
      
      if (options.showLoading !== false) {
        uni.showLoading({
          title: '上传中...',
          mask: true
        })
      }
      
      console.log(`[${config.name}] 上传:`, finalUrl)
      
      uni.uploadFile({
        url: finalUrl,
        filePath,
        name: 'file',
        formData,
        header,
        timeout: options.timeout || config.timeout,
        success: (response) => {
          uni.hideLoading()
          try {
            let data = response.data
            if (typeof data === 'string') {
              data = JSON.parse(data)
            }
            console.log(`[${config.name}] 上传成功:`, data)
            resolve(data)
          } catch (error) {
            console.error(`[${config.name}] 上传响应解析失败:`, error)
            reject(error)
          }
        },
        fail: (error) => {
          uni.hideLoading()
          console.error(`[${config.name}] 上传失败:`, error)
          if (options.showError !== false) {
            uni.showToast({
              title: '上传失败',
              icon: 'none'
            })
          }
          reject(error)
        }
      })
    })
  }
}

export default http