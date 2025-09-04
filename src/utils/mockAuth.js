// 模拟登录验证工具
import { setLocal, getLocal } from '@/utils/localStorage.js'

// 模拟用户数据库
const mockUsers = [
  {
    id: '1',
    username: 'admin',
    password: '123456',
    phone: '13800138000',
    avatar: 'https://picsum.photos/100/100?random=1',
    nickname: '管理员',
    email: 'admin@example.com'
  },
  {
    id: '2',
    username: 'user',
    password: '123456',
    phone: '13800138001',
    avatar: 'https://picsum.photos/100/100?random=2',
    nickname: '普通用户',
    email: 'user@example.com'
  }
]

// 模拟短信验证码存储
let smsCodeStore = {}

/**
 * 模拟密码登录
 * @param {string} username - 用户名或手机号
 * @param {string} password - 密码
 * @returns {Promise<Object>} 登录结果
 */
export function mockPasswordLogin(username, password) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const user = mockUsers.find(u => 
        u.username === username || u.phone === username
      )
      
      if (!user) {
        reject(new Error('用户不存在'))
        return
      }
      
      if (user.password !== password) {
        reject(new Error('密码错误'))
        return
      }
      
      const token = 'mock_token_' + Date.now()
      const result = {
        token,
        user: {
          id: user.id,
          username: user.username,
          nickname: user.nickname,
          avatar: user.avatar,
          phone: user.phone,
          email: user.email
        }
      }
      
      resolve(result)
    }, 1000) // 模拟网络延迟
  })
}

/**
 * 模拟手机验证码登录
 * @param {string} phone - 手机号
 * @param {string} code - 验证码
 * @returns {Promise<Object>} 登录结果
 */
export function mockPhoneLogin(phone, code) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const storedCode = smsCodeStore[phone]
      
      if (!storedCode) {
        reject(new Error('请先获取验证码'))
        return
      }
      
      if (storedCode.code !== code) {
        reject(new Error('验证码错误'))
        return
      }
      
      if (Date.now() - storedCode.timestamp > 5 * 60 * 1000) {
        reject(new Error('验证码已过期'))
        return
      }
      
      // 查找用户或创建新用户
      let user = mockUsers.find(u => u.phone === phone)
      if (!user) {
        user = {
          id: Date.now().toString(),
          username: phone,
          phone: phone,
          avatar: 'https://picsum.photos/100/100?random=' + Math.floor(Math.random() * 100),
          nickname: '用户' + phone.slice(-4),
          email: ''
        }
        mockUsers.push(user)
      }
      
      const token = 'mock_token_' + Date.now()
      const result = {
        token,
        user: {
          id: user.id,
          username: user.username,
          nickname: user.nickname,
          avatar: user.avatar,
          phone: user.phone,
          email: user.email
        }
      }
      
      // 清除验证码
      delete smsCodeStore[phone]
      
      resolve(result)
    }, 1000)
  })
}

/**
 * 发送手机验证码
 * @param {string} phone - 手机号
 * @returns {Promise<Object>} 发送结果
 */
export function mockSendSmsCode(phone) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (!/^1[3-9]\d{9}$/.test(phone)) {
        reject(new Error('手机号格式不正确'))
        return
      }
      
      const code = Math.floor(Math.random() * 900000 + 100000).toString()
      smsCodeStore[phone] = {
        code,
        timestamp: Date.now()
      }
      
      console.log(`模拟短信: 手机号 ${phone} 的验证码是: ${code}`)
      
      resolve({
        success: true,
        message: '验证码发送成功',
        code: code // 开发阶段返回验证码，生产环境应该移除
      })
    }, 500)
  })
}

/**
 * 模拟微信登录
 * @returns {Promise<Object>} 登录结果
 */
export function mockWechatLogin() {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // 模拟微信用户信息
      const wechatUser = {
        id: 'wx_' + Date.now(),
        username: 'wechat_user',
        nickname: '微信用户',
        avatar: 'https://picsum.photos/100/100?random=999',
        phone: '',
        email: '',
        openid: 'mock_openid_' + Date.now()
      }
      
      const token = 'mock_token_wx_' + Date.now()
      const result = {
        token,
        user: wechatUser
      }
      
      resolve(result)
    }, 1500)
  })
}

/**
 * 模拟用户注册
 * @param {Object} userData - 用户数据
 * @returns {Promise<Object>} 注册结果
 */
export function mockRegister(userData) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const { username, password, phone, nickname } = userData
      
      // 检查用户名是否已存在
      const existingUser = mockUsers.find(u => 
        u.username === username || u.phone === phone
      )
      
      if (existingUser) {
        reject(new Error('用户名或手机号已存在'))
        return
      }
      
      // 创建新用户
      const newUser = {
        id: Date.now().toString(),
        username,
        password,
        phone,
        nickname: nickname || '新用户',
        avatar: 'https://picsum.photos/100/100?random=' + Math.floor(Math.random() * 100),
        email: ''
      }
      
      mockUsers.push(newUser)
      
      const token = 'mock_token_' + Date.now()
      const result = {
        token,
        user: {
          id: newUser.id,
          username: newUser.username,
          nickname: newUser.nickname,
          avatar: newUser.avatar,
          phone: newUser.phone,
          email: newUser.email
        }
      }
      
      resolve(result)
    }, 1200)
  })
}

/**
 * 验证token有效性
 * @param {string} token - token
 * @returns {boolean} 是否有效
 */
export function mockValidateToken(token) {
  return token && token.startsWith('mock_token_')
}