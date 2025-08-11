import { defineStore } from 'pinia'
import { removeLocal } from '@/utils/localStorage.js'
import {
  getToken,
  setToken,
  removeToken,
  getUser,
  setUser,
  removeUser
} from '@/utils/request/auth'
import { ref, computed } from 'vue'
import request from '@/utils/request/index'

export const useUserStore = defineStore('user', () => {
  const token = ref(getToken() || '')
  const user = ref(getUser() || {})
  const isLoading = ref(false)
  
  // 计算属性：是否已登录
  const isLoggedIn = computed(() => !!token.value && !!user.value.id)

  function getTokenHandle() {
    return getToken() || ''
  }

  function login(jscode) {
    if (isLoading.value) {
      return Promise.reject(new Error('登录进行中，请稍候...'))
    }

    isLoading.value = true
    uni.showLoading({ title: '登录中...' })

    return new Promise((resolve, reject) => {
      wx.login({
        success: async (log) => {
          try {
            console.log('微信登录成功:', log)
            
            const openid = await request({
              url: '/login/getOpenId',
              method: 'post',
              data: { jscode: log.code }
            })
            
            const userInfo = await request({
              url: '/login/login',
              method: 'post',
              data: { jscode, openid }
            })
            
            // 保存用户信息和token
            token.value = userInfo.token
            setToken(userInfo.token)
            user.value = userInfo
            setUser(userInfo)
            
            uni.hideLoading()
            uni.showToast({ title: '登录成功', icon: 'success' })
            
            resolve(userInfo)
          } catch (error) {
            console.error('登录失败:', error)
            uni.hideLoading()
            uni.showToast({ 
              title: error.message || '登录失败，请重试', 
              icon: 'error' 
            })
            reject(error)
          } finally {
            isLoading.value = false
          }
        },
        fail: (err) => {
          console.error('微信登录失败:', err)
          uni.hideLoading()
          uni.showToast({ title: '微信登录失败', icon: 'error' })
          isLoading.value = false
          reject(err)
        }
      })
    })
  }

  function logout() {
    try {
      // 清除用户数据
      user.value = {}
      token.value = ''
      removeUser()
      removeToken()
      
      uni.showToast({ title: '已退出登录', icon: 'success' })
      
      // 跳转到首页
      setTimeout(() => {
        uni.switchTab({ url: '/pages/home/home' })
      }, 1000)
    } catch (error) {
      console.error('登出失败:', error)
    }
  }

  return {
    token,
    user,
    isLoading,
    isLoggedIn,
    login,
    logout,
    getTokenHandle
  }
})
