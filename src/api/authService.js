/**
 * 认证服务API
 * 支持Mock和后端API的自动切换
 */

import { config, API_ENDPOINTS } from '@/config/api.js'
import { http } from '@/api/http.js'
import { 
  mockPasswordLogin, 
  mockPhoneLogin, 
  mockSendSmsCode, 
  mockRegister, 
  mockWechatLogin,
  mockValidateToken 
} from '@/utils/mockAuth.js'
import { setLocal, getLocal, removeLocal } from '@/utils/localStorage.js'

/**
 * 认证API服务
 */
export const authAPI = {
  /**
   * 密码登录
   * @param {string} username 用户名或邮箱
   * @param {string} password 密码
   * @returns {Promise<Object>}
   */
  async login(username, password) {
    if (config.enableMock) {
      // 使用Mock数据
      try {
        const result = await mockPasswordLogin(username, password)
        // 保存登录信息
        setLocal('token', result.token)
        setLocal('user', result.user)
        return {
          success: true,
          data: result,
          message: '登录成功'
        }
      } catch (error) {
        return {
          success: false,
          message: error.message
        }
      }
    } else {
      // 使用后端API
      try {
        const response = await http.post(API_ENDPOINTS.AUTH.LOGIN, {
          username,
          password
        })
        
        if (response.access_token) {
          // 保存登录信息
          setLocal('token', response.access_token)
          setLocal('refresh_token', response.refresh_token)
          setLocal('user', {
            id: response.user_id,
            username: response.username,
            role: response.role
          })
          
          return {
            success: true,
            data: response,
            message: '登录成功'
          }
        } else {
          return {
            success: false,
            message: '登录失败'
          }
        }
      } catch (error) {
        return {
          success: false,
          message: error.message || '登录失败'
        }
      }
    }
  },

  /**
   * 手机验证码登录
   * @param {string} phone 手机号
   * @param {string} code 验证码
   * @returns {Promise<Object>}
   */
  async phoneLogin(phone, code) {
    if (config.enableMock) {
      try {
        const result = await mockPhoneLogin(phone, code)
        setLocal('token', result.token)
        setLocal('user', result.user)
        return {
          success: true,
          data: result,
          message: '登录成功'
        }
      } catch (error) {
        return {
          success: false,
          message: error.message
        }
      }
    } else {
      // TODO: 实现后端手机登录API
      try {
        const response = await http.post('/auth/phone-login', {
          phone,
          code
        })
        
        if (response.access_token) {
          setLocal('token', response.access_token)
          setLocal('refresh_token', response.refresh_token)
          setLocal('user', {
            id: response.user_id,
            username: response.username,
            role: response.role
          })
          
          return {
            success: true,
            data: response,
            message: '登录成功'
          }
        } else {
          return {
            success: false,
            message: '登录失败'
          }
        }
      } catch (error) {
        return {
          success: false,
          message: error.message || '登录失败'
        }
      }
    }
  },

  /**
   * 发送短信验证码
   * @param {string} phone 手机号
   * @returns {Promise<Object>}
   */
  async sendSmsCode(phone) {
    if (config.enableMock) {
      try {
        const result = await mockSendSmsCode(phone)
        return {
          success: true,
          data: result,
          message: '验证码发送成功'
        }
      } catch (error) {
        return {
          success: false,
          message: error.message
        }
      }
    } else {
      // TODO: 实现后端发送短信API
      try {
        const response = await http.post('/auth/send-sms', {
          phone
        })
        
        return {
          success: true,
          data: response,
          message: '验证码发送成功'
        }
      } catch (error) {
        return {
          success: false,
          message: error.message || '验证码发送失败'
        }
      }
    }
  },

  /**
   * 用户注册
   * @param {Object} userData 用户数据
   * @returns {Promise<Object>}
   */
  async register(userData) {
    if (config.enableMock) {
      try {
        const result = await mockRegister(userData)
        setLocal('token', result.token)
        setLocal('user', result.user)
        return {
          success: true,
          data: result,
          message: '注册成功'
        }
      } catch (error) {
        return {
          success: false,
          message: error.message
        }
      }
    } else {
      try {
        const response = await http.post(API_ENDPOINTS.AUTH.REGISTER, {
          username: userData.username,
          password: userData.password,
          confirm_password: userData.password,
          email: userData.email || `${userData.username}@example.com`,
          full_name: userData.nickname || userData.username,
          phone: userData.phone || ''
        })
        
        if (response.success && response.data) {
          const tokenData = response.data
          setLocal('token', tokenData.access_token)
          setLocal('refresh_token', tokenData.refresh_token)
          setLocal('user', {
            id: tokenData.user_id,
            username: tokenData.username,
            role: tokenData.role
          })
          
          return {
            success: true,
            data: tokenData,
            message: '注册成功'
          }
        } else {
          return {
            success: false,
            message: response.message || '注册失败'
          }
        }
      } catch (error) {
        return {
          success: false,
          message: error.message || '注册失败'
        }
      }
    }
  },

  /**
   * 微信登录
   * @returns {Promise<Object>}
   */
  async wechatLogin() {
    if (config.enableMock) {
      try {
        const result = await mockWechatLogin()
        setLocal('token', result.token)
        setLocal('user', result.user)
        return {
          success: true,
          data: result,
          message: '微信登录成功'
        }
      } catch (error) {
        return {
          success: false,
          message: error.message
        }
      }
    } else {
      // TODO: 实现微信登录
      return {
        success: false,
        message: '微信登录暂未实现'
      }
    }
  },

  /**
   * 刷新Token
   * @returns {Promise<Object>}
   */
  async refreshToken() {
    if (config.enableMock) {
      // Mock环境直接返回成功
      return {
        success: true,
        message: 'Token刷新成功'
      }
    } else {
      try {
        const refreshToken = getLocal('refresh_token')
        if (!refreshToken) {
          throw new Error('无刷新令牌')
        }
        
        const response = await http.post(API_ENDPOINTS.AUTH.REFRESH, {
          refresh_token: refreshToken
        })
        
        if (response.access_token) {
          setLocal('token', response.access_token)
          setLocal('refresh_token', response.refresh_token)
          
          return {
            success: true,
            data: response,
            message: 'Token刷新成功'
          }
        } else {
          throw new Error('Token刷新失败')
        }
      } catch (error) {
        // Token刷新失败，清除登录信息
        this.logout()
        return {
          success: false,
          message: error.message || 'Token刷新失败'
        }
      }
    }
  },

  /**
   * 获取当前用户信息
   * @returns {Promise<Object>}
   */
  async getCurrentUser() {
    if (config.enableMock) {
      const user = getLocal('user')
      if (user) {
        return {
          success: true,
          data: user,
          message: '获取用户信息成功'
        }
      } else {
        return {
          success: false,
          message: '用户未登录'
        }
      }
    } else {
      try {
        const response = await http.get(API_ENDPOINTS.USER.PROFILE)
        return {
          success: true,
          data: response,
          message: '获取用户信息成功'
        }
      } catch (error) {
        return {
          success: false,
          message: error.message || '获取用户信息失败'
        }
      }
    }
  },

  /**
   * 检查登录状态
   * @returns {boolean}
   */
  isLoggedIn() {
    const token = getLocal('token')
    if (!token) return false
    
    if (config.enableMock) {
      return mockValidateToken(token)
    } else {
      // 简单检查token是否存在，更严格的验证应该请求后端
      return true
    }
  },

  /**
   * 退出登录
   */
  async logout() {
    if (!config.enableMock) {
      try {
        // 调用后端登出接口
        await http.post(API_ENDPOINTS.AUTH.LOGOUT)
      } catch (error) {
        console.error('后端登出失败:', error)
      }
    }
    
    // 清除本地存储
    removeLocal('token')
    removeLocal('refresh_token')
    removeLocal('user')
    
    // 跳转到登录页面
    uni.reLaunch({
      url: '/pages/login/login'
    })
  }
}

export default authAPI