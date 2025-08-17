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
import { ref, onMounted } from 'vue'

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

// 主题模式
const themeMode = ref('light')

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
  // 这里可以添加实际的主题应用逻辑
  console.log('切换到主题:', themeMode.value)
  
  // 可以通过修改根元素的类名来应用主题
  if (themeMode.value === 'dark') {
    uni.setNavigationBarColor({
      frontColor: '#ffffff',
      backgroundColor: '#1a1a1a'
    })
  } else {
    uni.setNavigationBarColor({
      frontColor: '#000000',
      backgroundColor: '#ffffff'
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
  
  uni.showToast({
    title: '已退出登录',
    icon: 'success'
  })
}

// 页面加载时初始化
onMounted(() => {
  // 从本地存储获取主题设置
  const savedTheme = uni.getStorageSync('themeMode')
  if (savedTheme) {
    themeMode.value = savedTheme
  }
  
  // 应用主题
  applyTheme()
})
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

/* 暗黑主题样式 */
.dark .profile-container {
  background-color: #1a1a1a;
  color: #fff;
}

.dark .section {
  background-color: #2d2d2d;
  color: #fff;
}

.dark .section-title {
  color: #fff;
}

.dark .label {
  color: #aaa;
}

.dark .value {
  color: #fff;
}

.dark .input {
  background-color: #3a3a3a;
  color: #fff;
  border-color: #444;
}

.dark .secondary {
  background-color: #3a3a3a;
  color: #fff;
  border-color: #444;
}
</style>