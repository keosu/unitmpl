<template>
  <view class="profile-container">
    <view class="header">
      <text class="title">个人中心</text>
    </view>

    <!-- 基本信息 -->
    <uv-cell-group title="基本信息" :border="true">
      <uv-cell title="用户名" :value="userInfo.username || '未设置'"></uv-cell>
      <uv-cell title="邮箱" :value="userInfo.email || '未设置'"></uv-cell>
      <uv-cell title="注册时间" :value="userInfo.registerDate || '未知'"></uv-cell>
    </uv-cell-group>

    <!-- 登录/注册 -->
    <uv-cell-group :title="isLogin ? '账户操作' : '登录/注册'" :border="true">
      <view v-if="!isLogin">
        <!-- 微信登录 -->
        <view class="login-methods">
          <uv-row v-if="isWeixin" class="login-row">
            <uv-col :span="24">
              <uv-button 
                type="success" 
                shape="circle" 
                icon="weixin"
                @click="handleWechatLogin"
              >
                微信一键登录
              </uv-button>
            </uv-col>
          </uv-row>
          
          <!-- 手机号一键登录 -->
          <uv-row v-if="isWeixin" class="login-row">
            <uv-col :span="24">
              <uv-button 
                type="primary" 
                shape="circle" 
                icon="phone"
                open-type="getPhoneNumber" 
                @getphonenumber="handlePhoneNumberLogin"
              >
                手机号一键登录
              </uv-button>
            </uv-col>
          </uv-row>
        </view>
        
        <uv-row class="divider-row">
          <uv-col :span="24">
            <uv-tabs 
              :list="tabList" 
              @click="changeTab"
              :current="currentTab"
              :bold="true"
              :fontSize="28"
            ></uv-tabs>
          </uv-col>
        </uv-row>
        
        <view v-if="currentSegment === 0">
          <uv-form ref="loginFormRef" :model="loginForm">
            <uv-form-item label="用户名">
              <uv-input 
                v-model="loginForm.username" 
                placeholder="请输入用户名" 
                border="surround"
                clearable
              />
            </uv-form-item>
            <uv-form-item label="密码">
              <uv-input 
                v-model="loginForm.password" 
                placeholder="请输入密码" 
                border="surround"
                clearable
                type="password"
              />
            </uv-form-item>
          </uv-form>
          
          <uv-row class="button-row">
            <uv-col :span="11">
              <uv-button 
                type="primary" 
                shape="circle"
                @click="handleLogin"
              >
                登录
              </uv-button>
            </uv-col>
            <uv-col :span="11" :offset="2">
              <uv-button 
                type="info" 
                shape="circle"
                @click="handleRegister"
              >
                注册
              </uv-button>
            </uv-col>
          </uv-row>
        </view>
        
        <view v-else>
          <uv-form ref="phoneFormRef" :model="phoneForm">
            <uv-form-item label="手机号">
              <uv-input 
                v-model="phoneForm.phoneNumber" 
                placeholder="请输入手机号" 
                border="surround"
                clearable
                type="number"
              />
            </uv-form-item>
            <uv-form-item label="验证码">
              <uv-row :gutter="10">
                <uv-col :span="14">
                  <uv-input 
                    v-model="phoneForm.verifyCode" 
                    placeholder="请输入验证码" 
                    border="surround"
                    clearable
                    type="number"
                  />
                </uv-col>
                <uv-col :span="10">
                  <uv-button 
                    type="warning" 
                    shape="circle"
                    :disabled="codeDisabled"
                    @click="sendVerifyCode"
                    size="mini"
                  >
                    {{ codeText }}
                  </uv-button>
                </uv-col>
              </uv-row>
            </uv-form-item>
          </uv-form>
          
          <uv-row class="button-row">
            <uv-col :span="24">
              <uv-button 
                type="primary" 
                shape="circle"
                @click="handlePhoneLogin"
              >
                登录
              </uv-button>
            </uv-col>
          </uv-row>
        </view>
      </view>
      
      <view v-else>
        <uv-row class="button-row">
          <uv-col :span="24">
            <uv-button 
              type="error" 
              shape="circle"
              @click="handleLogout"
            >
              退出登录
            </uv-button>
          </uv-col>
        </uv-row>
      </view>
    </uv-cell-group>

    <!-- 设置 -->
    <uv-cell-group title="设置" :border="true">
      <uv-cell title="主题模式">
        <template #value>
          <view class="switch-container">
            <text :class="['theme-label', { active: themeMode === 'light' }]">明亮</text>
            <uv-switch 
              :modelValue="themeMode === 'dark'" 
              @change="toggleTheme"
              activeColor="#007AFF"
            ></uv-switch>
            <text :class="['theme-label', { active: themeMode === 'dark' }]">暗黑</text>
          </view>
        </template>
      </uv-cell>
    </uv-cell-group>
  </view>
  
  <!-- 自定义 tabBar -->
  <custom-tab-bar ref="tabBar"></custom-tab-bar>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import CustomTabBar from '@/components/custom-tab-bar.vue'

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

// 手机号登录表单
const phoneForm = ref({
  phoneNumber: '',
  verifyCode: ''
})

// 登录状态
const isLogin = ref(false)

// 是否为微信环境
const isWeixin = ref(false)

// 主题模式
const themeMode = ref('light')

// 标签页
const currentTab = ref(0)
const tabList = ref([
  { name: '账号登录' },
  { name: '手机登录' }
])

// 验证码按钮状态
const codeDisabled = ref(false)
const codeText = ref('获取验证码')
let countdown = 60

// tabBar引用
const tabBar = ref(null)

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

// 切换标签页
const changeTab = (item) => {
  currentTab.value = item.index
}

// 发送验证码
const sendVerifyCode = () => {
  if (!phoneForm.value.phoneNumber) {
    uni.showToast({
      title: '请输入手机号',
      icon: 'none'
    })
    return
  }
  
  // 模拟发送验证码
  codeDisabled.value = true
  const timer = setInterval(() => {
    if (countdown > 0) {
      countdown--
      codeText.value = `${countdown}秒后重发`
    } else {
      clearInterval(timer)
      codeDisabled.value = false
      codeText.value = '获取验证码'
      countdown = 60
    }
  }, 1000)
  
  uni.showToast({
    title: '验证码已发送',
    icon: 'success'
  })
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

// 处理手机登录
const handlePhoneLogin = () => {
  if (!phoneForm.value.phoneNumber || !phoneForm.value.verifyCode) {
    uni.showToast({
      title: '请输入手机号和验证码',
      icon: 'none'
    })
    return
  }
  
  // 模拟登录逻辑
  userInfo.value = {
    username: phoneForm.value.phoneNumber,
    email: `${phoneForm.value.phoneNumber}@example.com`,
    registerDate: new Date().toLocaleDateString()
  }
  isLogin.value = true
  
  // 保存登录状态
  uni.setStorageSync('token', 'phone_login_token')
  
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
  phoneForm.value = {
    phoneNumber: '',
    verifyCode: ''
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

.button-row {
  margin-top: 20rpx;
}

.btn {
  width: 100%;
  height: 80rpx;
  border-radius: 10rpx;
  font-size: 32rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
}

.primary {
  background-color: #007AFF;
  color: white;
}

.secondary {
  background-color: #F8F8F8;
  color: #333;
  border: 1rpx solid #ddd;
}

.danger {
  background-color: #FF3B30;
  color: white;
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
  gap: 10rpx;
}

.wechat-login-text {
  font-size: 32rpx;
}

/* 手机号登录按钮样式 */
.phone-login-btn {
  background-color: #007AFF;
  color: white;
  margin-bottom: 20rpx;
  gap: 10rpx;
}

.phone-login-text {
  font-size: 32rpx;
}

/* 验证码按钮样式 */
.code-btn {
  background-color: #007AFF;
  color: white;
  height: 70rpx;
  font-size: 28rpx;
}

.code-btn[disabled] {
  background-color: #cccccc;
}

/* 登录方式行 */
.login-row {
  margin-bottom: 20rpx;
}

/* 分割行 */
.divider-row {
  margin: 30rpx 0;
}

/* 暗黑主题样式 - 使用媒体查询方式 */
@media (prefers-color-scheme: dark) {
  .profile-container {
    background-color: #1a1a1a;
    color: #fff;
  }

  .theme-label {
    color: #aaa;
  }
  
  .theme-label.active {
    color: #007AFF;
  }
}
</style>