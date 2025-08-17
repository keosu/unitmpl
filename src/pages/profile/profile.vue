<template>
  <view class="profile-container">
    <view class="header">
      <text class="title">个人中心</text>
    </view>

    <!-- 基本信息 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">基本信息</text>
      </view>
      <view class="info-item">
        <text class="label">用户名:</text>
        <text class="value">{{ userInfo.username || '未设置' }}</text>
      </view>
      <view class="info-item">
        <text class="label">邮箱:</text>
        <text class="value">{{ userInfo.email || '未设置' }}</text>
      </view>
      <view class="info-item">
        <text class="label">注册时间:</text>
        <text class="value">{{ userInfo.registerDate || '未知' }}</text>
      </view>
    </view>

    <!-- 登录/注册 -->
    <view class="section" v-if="!isLogin">
      <view class="section-header">
        <text class="section-title">登录/注册</text>
      </view>
      
      <!-- 微信登录 -->
      <view class="login-methods">
        <button 
          v-if="isWeixin" 
          class="btn wechat-login-btn" 
          open-type="getUserInfo" 
          @getuserinfo="handleWechatLogin"
        >
          <text class="wechat-login-text">微信一键登录</text>
        </button>
        
        <!-- 手机号一键登录 -->
        <button 
          v-if="isWeixin" 
          class="btn phone-login-btn" 
          open-type="getPhoneNumber" 
          @getphonenumber="handlePhoneNumberLogin"
        >
          <text class="phone-login-text">手机号一键登录</text>
        </button>
      </view>
      
      <view class="divider">
        <text class="divider-text">或</text>
      </view>
      
      <view class="form-group">
        <input 
          class="input" 
          type="text" 
          placeholder="用户名" 
          v-model="loginForm.username"
        />
      </view>
      <view class="form-group">
        <input 
          class="input" 
          type="password" 
          placeholder="密码" 
          v-model="loginForm.password"
        />
      </view>
      <view class="button-group">
        <button class="btn primary" @click="handleLogin">登录</button>
        <button class="btn secondary" @click="handleRegister">注册</button>
      </view>
    </view>

    <!-- 已登录状态 -->
    <view class="section" v-else>
      <view class="section-header">
        <text class="section-title">账户操作</text>
      </view>
      <view class="button-group">
        <button class="btn danger" @click="handleLogout">退出登录</button>
      </view>
    </view>

    <!-- 设置 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">设置</text>
      </view>
      <view class="setting-item">
        <text class="setting-label">主题模式</text>
        <view class="switch-container">
          <text :class="['theme-label', { active: themeMode === 'light' }]">明亮</text>
          <switch 
            :checked="themeMode === 'dark'" 
            @change="toggleTheme"
            color="#007AFF"
          />
          <text :class="['theme-label', { active: themeMode === 'dark' }]">暗黑</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// 用户信息
const userInfo = ref({
  username: '',
  email: '',
  registerDate: ''
})

// 登录表单
const loginForm = ref({
  username: '',
  password: ''
})

// 登录状态
const isLogin = ref(false)

// 是否为微信环境
const isWeixin = ref(false)

// 主题模式
const themeMode = ref('light')

// 主题变化监听函数
let themeChangeListener

// 页面加载时初始化
onMounted(() => {
  // 检查是否在微信环境
  // #ifdef MP-WEIXIN
  isWeixin.value = true
  // #endif
  
  // 从本地存储获取主题设置
  const savedTheme = uni.getStorageSync('themeMode')
  if (savedTheme) {
    themeMode.value = savedTheme
  } else {
    // 如果没有保存的主题设置，则获取系统主题
    try {
      const systemInfo = uni.getSystemInfoSync()
      if (systemInfo.theme) {
        themeMode.value = systemInfo.theme
      }
    } catch (e) {
      console.error('获取系统主题信息失败:', e)
    }
  }
  
  // 应用主题
  applyTheme()
  
  // 监听主题变化
  themeChangeListener = (res) => {
    // 如果用户没有手动设置主题，则跟随系统主题变化
    const savedTheme = uni.getStorageSync('themeMode')
    if (!savedTheme) {
      themeMode.value = res.theme
      applyTheme()
    }
  }
  
  uni.onThemeChange(themeChangeListener)
  
  // 检查登录状态
  checkLoginStatus()
})

// 页面卸载时取消监听
onUnmounted(() => {
  if (themeChangeListener) {
    uni.offThemeChange(themeChangeListener)
  }
})

// 检查登录状态
const checkLoginStatus = () => {
  const token = uni.getStorageSync('token')
  if (token) {
    // 模拟获取用户信息
    userInfo.value = {
      username: '已登录用户',
      email: 'user@example.com',
      registerDate: '2025-01-01'
    }
    isLogin.value = true
  }
}

// 切换主题
const toggleTheme = (e) => {
  const isDark = e.detail.value
  themeMode.value = isDark ? 'dark' : 'light'
  
  // 保存主题设置到本地存储
  uni.setStorageSync('themeMode', themeMode.value)
  
  // 应用主题
  applyTheme()
}

// 应用主题
const applyTheme = () => {
  // 使用UniApp官方API设置导航栏颜色
  if (themeMode.value === 'dark') {
    uni.setNavigationBarColor({
      frontColor: '#ffffff',
      backgroundColor: '#1a1a1a'
    })
  } else {
    uni.setNavigationBarColor({
      frontColor: '#000000',
      backgroundColor: '#F8F8F8'
    })
  }
}

// 处理微信登录
const handleWechatLogin = (e) => {
  if (e.detail.errMsg === 'getUserInfo:ok') {
    uni.showLoading({
      title: '登录中...'
    })
    
    // 微信登录流程
    uni.login({
      provider: 'weixin',
      success: (loginRes) => {
        // 这里应该将登录凭证发送到后端进行验证
        // loginRes.code 是登录凭证
        console.log('微信登录成功，code:', loginRes.code)
        
        // 模拟登录成功
        setTimeout(() => {
          uni.hideLoading()
          userInfo.value = {
            username: '微信用户',
            email: 'wechat@example.com',
            registerDate: new Date().toLocaleDateString()
          }
          isLogin.value = true
          
          // 保存登录状态
          uni.setStorageSync('token', 'wechat_login_token')
          
          uni.showToast({
            title: '微信登录成功',
            icon: 'success'
          })
        }, 1000)
      },
      fail: (err) => {
        uni.hideLoading()
        uni.showToast({
          title: '微信登录失败',
          icon: 'none'
        })
        console.error('微信登录失败:', err)
      }
    })
  } else {
    uni.showToast({
      title: '微信登录取消',
      icon: 'none'
    })
  }
}

// 处理手机号登录
const handlePhoneNumberLogin = (e) => {
  if (e.detail.errMsg === 'getPhoneNumber:ok') {
    uni.showLoading({
      title: '登录中...'
    })
    
    // 获取手机号码流程
    // 在新版微信小程序中，需要先调用 uni.login 获取 code
    uni.login({
      provider: 'weixin',
      success: (loginRes) => {
        // 将 code 和 encryptedData 发送到后端进行解密
        console.log('获取到code:', loginRes.code)
        console.log('获取到手机号加密数据:', e.detail)
        
        // 模拟发送到后端解密手机号
        setTimeout(() => {
          uni.hideLoading()
          userInfo.value = {
            username: '手机用户',
            email: 'phone@example.com',
            registerDate: new Date().toLocaleDateString()
          }
          isLogin.value = true
          
          // 保存登录状态
          uni.setStorageSync('token', 'phone_login_token')
          
          uni.showToast({
            title: '手机号登录成功',
            icon: 'success'
          })
        }, 1000)
      },
      fail: (err) => {
        uni.hideLoading()
        uni.showToast({
          title: '手机号获取失败',
          icon: 'none'
        })
        console.error('获取手机号失败:', err)
      }
    })
  } else {
    uni.showToast({
      title: '手机号获取失败',
      icon: 'none'
    })
  }
}

// 处理登录
const handleLogin = () => {
  if (!loginForm.value.username || !loginForm.value.password) {
    uni.showToast({
      title: '请输入用户名和密码',
      icon: 'none'
    })
    return
  }
  
  // 模拟登录逻辑
  userInfo.value = {
    username: loginForm.value.username,
    email: `${loginForm.value.username}@example.com`,
    registerDate: '2025-01-01'
  }
  isLogin.value = true
  
  // 保存登录状态
  uni.setStorageSync('token', 'normal_login_token')
  
  uni.showToast({
    title: '登录成功',
    icon: 'success'
  })
}

// 处理注册
const handleRegister = () => {
  if (!loginForm.value.username || !loginForm.value.password) {
    uni.showToast({
      title: '请输入用户名和密码',
      icon: 'none'
    })
    return
  }
  
  // 模拟注册逻辑
  userInfo.value = {
    username: loginForm.value.username,
    email: `${loginForm.value.username}@example.com`,
    registerDate: new Date().toLocaleDateString()
  }
  isLogin.value = true
  
  // 保存登录状态
  uni.setStorageSync('token', 'register_token')
  
  uni.showToast({
    title: '注册成功',
    icon: 'success'
  })
}

// 处理退出登录
const handleLogout = () => {
  userInfo.value = {
    username: '',
    email: '',
    registerDate: ''
  }
  loginForm.value = {
    username: '',
    password: ''
  }
  isLogin.value = false
  
  // 清除登录状态
  uni.removeStorageSync('token')
  
  uni.showToast({
    title: '已退出登录',
    icon: 'success'
  })
}
</script>

<style scoped>
.profile-container {
  padding: 20rpx;
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 40rpx;
}

.title {
  font-size: 48rpx;
  font-weight: bold;
}

.section {
  background-color: #fff;
  border-radius: 10rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.section-header {
  border-bottom: 1rpx solid #eee;
  padding-bottom: 20rpx;
  margin-bottom: 30rpx;
}

.section-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #f5f5f5;
}

.info-item:last-child {
  border-bottom: none;
}

.label {
  font-size: 28rpx;
  color: #666;
}

.value {
  font-size: 28rpx;
  color: #333;
}

.form-group {
  margin-bottom: 30rpx;
}

.input {
  width: 100%;
  height: 80rpx;
  padding: 0 20rpx;
  border: 1rpx solid #ddd;
  border-radius: 10rpx;
  font-size: 28rpx;
  box-sizing: border-box;
}

.button-group {
  display: flex;
  gap: 20rpx;
}

.btn {
  flex: 1;
  height: 80rpx;
  border-radius: 10rpx;
  font-size: 32rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.primary {
  background-color: #007AFF;
  color: white;
  border: none;
}

.secondary {
  background-color: #F8F8F8;
  color: #333;
  border: 1rpx solid #ddd;
}

.danger {
  background-color: #FF3B30;
  color: white;
  border: none;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 0;
}

.setting-label {
  font-size: 28rpx;
  color: #333;
}

.switch-container {
  display: flex;
  align-items: center;
  gap: 10rpx;
}

.theme-label {
  font-size: 24rpx;
  color: #999;
}

.theme-label.active {
  color: #007AFF;
  font-weight: bold;
}

/* 微信登录按钮样式 */
.wechat-login-btn {
  background-color: #07c160;
  color: white;
  margin-bottom: 20rpx;
}

.wechat-login-text {
  font-size: 32rpx;
}

/* 手机号登录按钮样式 */
.phone-login-btn {
  background-color: #007AFF;
  color: white;
  margin-bottom: 20rpx;
}

.phone-login-text {
  font-size: 32rpx;
}

/* 分割线 */
.divider {
  text-align: center;
  position: relative;
  margin: 30rpx 0;
}

.divider-text {
  background-color: #fff;
  padding: 0 20rpx;
  color: #999;
  font-size: 28rpx;
}

.divider::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  width: 100%;
  height: 1rpx;
  background-color: #eee;
  z-index: 1;
}

.divider-text {
  position: relative;
  z-index: 2;
}

/* 暗黑主题样式 - 使用媒体查询方式 */
@media (prefers-color-scheme: dark) {
  .profile-container {
    background-color: #1a1a1a;
    color: #fff;
  }

  .section {
    background-color: #2d2d2d;
    color: #fff;
  }

  .section-title {
    color: #fff;
  }

  .label {
    color: #aaa;
  }

  .value {
    color: #fff;
  }

  .input {
    background-color: #3a3a3a;
    color: #fff;
    border-color: #444;
  }

  .secondary {
    background-color: #3a3a3a;
    color: #fff;
    border-color: #444;
  }
  
  .divider-text {
    background-color: #2d2d2d;
    color: #aaa;
  }
  
  .divider::before {
    background-color: #444;
  }
}
</style>