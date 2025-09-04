<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useThemeStore } from '@/store/theme.js'
import { useUserStore } from '@/store/user.js'
import { getToken } from '@/utils/request/auth.js'
import { 
	mockPasswordLogin, 
	mockPhoneLogin, 
	mockSendSmsCode, 
	mockWechatLogin,
	mockRegister 
} from '@/utils/mockAuth.js'

const { t } = useI18n()
const themeStore = useThemeStore()
const userStore = useUserStore()

// 当前标签页
const currentTab = ref(0)
const showPassword = ref(false)
const showRegPassword = ref(false)
const countdown = ref(0)
let countdownTimer = null

// 登录表单
const loginForm = ref({
	username: '',
	password: ''
})

// 手机表单
const phoneForm = ref({
	phone: '',
	code: ''
})

// 注册表单
const registerForm = ref({
	username: '',
	phone: '',
	password: '',
	nickname: ''
})

// 标签页配置
const loginTabs = computed(() => [
	{ title: t('login.password_login') },
	{ title: t('login.phone_login') },
	{ title: t('login.register') }
])

// 计算属性
const canPasswordLogin = computed(() => 
	loginForm.value.username.trim() && loginForm.value.password.trim()
)

const canPhoneLogin = computed(() => 
	phoneForm.value.phone.trim() && phoneForm.value.code.trim()
)

const canSendCode = computed(() => 
	/^1[3-9]\d{9}$/.test(phoneForm.value.phone) && countdown.value === 0
)

const canRegister = computed(() => 
	registerForm.value.username.trim() && 
	registerForm.value.phone.trim() && 
	registerForm.value.password.trim()
)

onMounted(() => {
	if (getToken()) {
		uni.reLaunch({ url: '/pages/index/index?index=1' })
	}
})

// 切换标签页
const switchTab = (index) => {
	currentTab.value = index
	// 清空表单
	loginForm.value = { username: '', password: '' }
	phoneForm.value = { phone: '', code: '' }
	registerForm.value = { username: '', phone: '', password: '', nickname: '' }
}

// 密码登录
const handlePasswordLogin = async () => {
	if (!canPasswordLogin.value) return
	
	uni.showLoading({ title: t('login.logging_in') })
	try {
		const result = await mockPasswordLogin(
			loginForm.value.username,
			loginForm.value.password
		)
		
		await userStore.setUserInfo(result)
		uni.hideLoading()
		uni.showToast({ title: t('login.login_success'), icon: 'success' })
		
		setTimeout(() => {
			uni.reLaunch({ url: '/pages/index/index?index=1' })
		}, 1000)
	} catch (error) {
		uni.hideLoading()
		uni.showToast({ title: error.message, icon: 'error' })
	}
}

// 发送短信验证码
const sendSmsCode = async () => {
	if (!canSendCode.value) return
	
	try {
		const result = await mockSendSmsCode(phoneForm.value.phone)
		uni.showToast({ title: result.message, icon: 'success' })
		
		// 开发阶段自动填充验证码
		if (result.code) {
			phoneForm.value.code = result.code
		}
		
		// 开始倒计时
		countdown.value = 60
		countdownTimer = setInterval(() => {
			countdown.value--
			if (countdown.value <= 0) {
				clearInterval(countdownTimer)
			}
		}, 1000)
	} catch (error) {
		uni.showToast({ title: error.message, icon: 'error' })
	}
}

// 手机登录
const handlePhoneLogin = async () => {
	if (!canPhoneLogin.value) return
	
	uni.showLoading({ title: t('login.logging_in') })
	try {
		const result = await mockPhoneLogin(
			phoneForm.value.phone,
			phoneForm.value.code
		)
		
		await userStore.setUserInfo(result)
		uni.hideLoading()
		uni.showToast({ title: t('login.login_success'), icon: 'success' })
		
		setTimeout(() => {
			uni.reLaunch({ url: '/pages/index/index?index=1' })
		}, 1000)
	} catch (error) {
		uni.hideLoading()
		uni.showToast({ title: error.message, icon: 'error' })
	}
}

// 注册
const handleRegister = async () => {
	if (!canRegister.value) return
	
	uni.showLoading({ title: t('login.registering') })
	try {
		const result = await mockRegister(registerForm.value)
		
		await userStore.setUserInfo(result)
		uni.hideLoading()
		uni.showToast({ title: t('login.register_success'), icon: 'success' })
		
		setTimeout(() => {
			uni.reLaunch({ url: '/pages/index/index?index=1' })
		}, 1000)
	} catch (error) {
		uni.hideLoading()
		uni.showToast({ title: error.message, icon: 'error' })
	}
}

// 微信登录
const handleWechatLogin = async () => {
	uni.showLoading({ title: t('login.logging_in') })
	try {
		const result = await mockWechatLogin()
		
		await userStore.setUserInfo(result)
		uni.hideLoading()
		uni.showToast({ title: t('login.login_success'), icon: 'success' })
		
		setTimeout(() => {
			uni.reLaunch({ url: '/pages/index/index?index=1' })
		}, 1000)
	} catch (error) {
		uni.hideLoading()
		uni.showToast({ title: error.message, icon: 'error' })
	}
}

// 显示用户协议
const showAgreement = () => {
	uni.showModal({
		title: t('login.user_agreement'),
		content: t('login.agreement_content'),
		showCancel: false
	})
}

// 显示隐私政策
const showPrivacy = () => {
	uni.showModal({
		title: t('login.privacy_policy'),
		content: t('login.privacy_content'),
		showCancel: false
	})
}
</script>

<template>
	<view class="login-container" :class="`theme-${themeStore.currentTheme}`">
		<!-- 头部信息 -->
		<view class="header-section">
			<view class="logo-wrapper">
				<text class="logo-icon">🎯</text>
			</view>
			<view class="app-title">{{ t('login.app_name') }}</view>
			<view class="app-subtitle">{{ t('login.welcome') }}</view>
		</view>

		<!-- 登录表单 -->
		<view class="form-section">
			<!-- 登录方式切换 -->
			<view class="login-tabs">
				<view 
					v-for="(tab, index) in loginTabs" 
					:key="index"
					class="tab-item"
					:class="{ active: currentTab === index }"
					@click="switchTab(index)"
				>
					{{ tab.title }}
				</view>
			</view>

			<!-- 密码登录 -->
			<view v-if="currentTab === 0" class="form-content">
				<view class="input-group">
					<view class="input-wrapper">
						<text class="input-icon">👤</text>
						<input 
							v-model="loginForm.username"
							type="text" 
							:placeholder="t('login.username_placeholder')"
							class="form-input"
							maxlength="20"
						/>
					</view>
				</view>
				<view class="input-group">
					<view class="input-wrapper">
						<text class="input-icon">🔒</text>
						<input 
							v-model="loginForm.password"
							:type="showPassword ? 'text' : 'password'"
							:placeholder="t('login.password_placeholder')"
							class="form-input"
							maxlength="20"
						/>
						<text 
							class="password-toggle"
							@click="showPassword = !showPassword"
						>
							{{ showPassword ? '🙈' : '👁️' }}
						</text>
					</view>
				</view>
				<button 
					class="login-btn"
					:class="{ disabled: !canPasswordLogin }"
					:disabled="!canPasswordLogin"
					@click="handlePasswordLogin"
				>
					{{ t('login.login') }}
				</button>
			</view>

			<!-- 手机登录 -->
			<view v-if="currentTab === 1" class="form-content">
				<view class="input-group">
					<view class="input-wrapper">
						<text class="input-icon">📱</text>
						<input 
							v-model="phoneForm.phone"
							type="number" 
							:placeholder="t('login.phone_placeholder')"
							class="form-input"
							maxlength="11"
						/>
					</view>
				</view>
				<view class="input-group">
					<view class="input-wrapper code-wrapper">
						<text class="input-icon">💬</text>
						<input 
							v-model="phoneForm.code"
							type="number" 
							:placeholder="t('login.code_placeholder')"
							class="form-input"
							maxlength="6"
						/>
						<button 
							class="code-btn"
							:class="{ disabled: !canSendCode }"
							:disabled="!canSendCode"
							@click="sendSmsCode"
						>
							{{ countdown > 0 ? `${countdown}s` : t('login.send_code') }}
						</button>
					</view>
				</view>
				<button 
					class="login-btn"
					:class="{ disabled: !canPhoneLogin }"
					:disabled="!canPhoneLogin"
					@click="handlePhoneLogin"
				>
					{{ t('login.login') }}
				</button>
			</view>

			<!-- 注册表单 -->
			<view v-if="currentTab === 2" class="form-content">
				<view class="input-group">
					<view class="input-wrapper">
						<text class="input-icon">👤</text>
						<input 
							v-model="registerForm.username"
							type="text" 
							:placeholder="t('login.username_placeholder')"
							class="form-input"
							maxlength="20"
						/>
					</view>
				</view>
				<view class="input-group">
					<view class="input-wrapper">
						<text class="input-icon">📱</text>
						<input 
							v-model="registerForm.phone"
							type="number" 
							:placeholder="t('login.phone_placeholder')"
							class="form-input"
							maxlength="11"
						/>
					</view>
				</view>
				<view class="input-group">
					<view class="input-wrapper">
						<text class="input-icon">🔒</text>
						<input 
							v-model="registerForm.password"
							:type="showRegPassword ? 'text' : 'password'"
							:placeholder="t('login.password_placeholder')"
							class="form-input"
							maxlength="20"
						/>
						<text 
							class="password-toggle"
							@click="showRegPassword = !showRegPassword"
						>
							{{ showRegPassword ? '🙈' : '👁️' }}
						</text>
					</view>
				</view>
				<view class="input-group">
					<view class="input-wrapper">
						<text class="input-icon">😊</text>
						<input 
							v-model="registerForm.nickname"
							type="text" 
							:placeholder="t('login.nickname_placeholder')"
							class="form-input"
							maxlength="20"
						/>
					</view>
				</view>
				<button 
					class="login-btn register-btn"
					:class="{ disabled: !canRegister }"
					:disabled="!canRegister"
					@click="handleRegister"
				>
					{{ t('login.register') }}
				</button>
			</view>
		</view>

		<!-- 第三方登录 -->
		<view class="social-login">
			<view class="divider">
				<text class="divider-text">{{ t('login.or') }}</text>
			</view>
			<view class="social-buttons">
				<button 
					class="social-btn wechat-btn"
					@click="handleWechatLogin"
				>
					<text class="social-icon">💬</text>
					<text class="social-text">{{ t('login.wechat_login') }}</text>
				</button>
			</view>
		</view>

		<!-- 用户协议 -->
		<view class="agreement">
			<text class="agreement-text">
				{{ t('login.agreement_prefix') }}
				<text class="agreement-link" @click="showAgreement">{{ t('login.user_agreement') }}</text>
				{{ t('login.and') }}
				<text class="agreement-link" @click="showPrivacy">{{ t('login.privacy_policy') }}</text>
			</text>
		</view>
	</view>
</template>



<style lang="scss" scoped>
.login-container {
	min-height: 100vh;
	background: #667eea;
	padding: 80rpx 60rpx;
}

.header-section {
	text-align: center;
	margin-bottom: 60px;
	padding-top: 80px;
}

.logo-wrapper {
	margin-bottom: 20px;
}

.logo-icon {
	font-size: 60px;
}

.app-title {
	font-size: 28px;
	font-weight: bold;
	color: #fff;
	margin-bottom: 10px;
}

.app-subtitle {
	font-size: 16px;
	color: rgba(255, 255, 255, 0.8);
}

.form-section {
	background: rgba(255, 255, 255, 0.95);
	border-radius: 20px;
	padding: 30px;
	margin-bottom: 30px;
	backdrop-filter: blur(10px);
}

.login-tabs {
	display: flex;
	margin-bottom: 30px;
	border-radius: 10px;
	background: #f5f5f5;
	padding: 4px;
}

.tab-item {
	flex: 1;
	text-align: center;
	padding: 12px;
	border-radius: 8px;
	transition: all 0.3s ease;
	font-size: 14px;
	color: #666;
	cursor: pointer;
}

.tab-item.active {
	background: #667eea;
	color: #fff;
}

.form-content {
	animation: fadeIn 0.3s ease;
}

.input-group {
	margin-bottom: 20px;
}

.input-wrapper {
	position: relative;
	display: flex;
	align-items: center;
	background: #f8f9fa;
	border-radius: 12px;
	padding: 0 15px;
	border: 2px solid transparent;
	transition: all 0.3s ease;
}

.input-wrapper:focus-within {
	border-color: #667eea;
	background: #fff;
}

.input-icon {
	font-size: 18px;
	margin-right: 12px;
	color: #999;
}

.form-input {
	flex: 1;
	height: 50px;
	border: none;
	background: transparent;
	font-size: 16px;
	color: #333;
}

.password-toggle {
	font-size: 18px;
	color: #999;
	cursor: pointer;
	padding: 10px;
}

.code-wrapper {
	padding-right: 5px;
}

.code-btn {
	padding: 8px 16px;
	background: #667eea;
	color: #fff;
	border: none;
	border-radius: 8px;
	font-size: 14px;
	margin-left: 10px;
	transition: all 0.3s ease;
}

.code-btn.disabled {
	background: #ccc;
}

.login-btn {
	width: 100%;
	height: 50px;
	background: #667eea;
	color: #fff;
	border: none;
	border-radius: 12px;
	font-size: 16px;
	font-weight: bold;
	transition: all 0.3s ease;
	margin-top: 10px;
}

.login-btn:hover {
	background: #5a6fd8;
}

.login-btn.disabled {
	background: #ccc;
}

.register-btn {
	background: #28a745;
}

.register-btn:hover {
	background: #218838;
}

.social-login {
	text-align: center;
	margin-bottom: 30px;
}

.divider {
	position: relative;
	margin: 20px 0;
}

.divider::before {
	content: '';
	position: absolute;
	top: 50%;
	left: 0;
	right: 0;
	height: 1px;
	background: rgba(255, 255, 255, 0.3);
}

.divider-text {
	background: transparent;
	padding: 0 20px;
	color: rgba(255, 255, 255, 0.8);
	font-size: 14px;
}

.social-buttons {
	display: flex;
	justify-content: center;
	gap: 20px;
}

.social-btn {
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 24rpx 48rpx;
	border: none;
	border-radius: 24rpx;
	background: rgba(255, 255, 255, 0.9);
}

.wechat-btn {
	background: #07c160;
	color: #fff;
}

.social-icon {
	font-size: 18px;
	margin-right: 8px;
}

.social-text {
	font-size: 14px;
}

.agreement {
	text-align: center;
	padding: 0 20px;
}

.agreement-text {
	font-size: 12px;
	color: rgba(255, 255, 255, 0.7);
	line-height: 1.5;
}

.agreement-link {
	color: #fff;
	text-decoration: underline;
	cursor: pointer;
}

@keyframes fadeIn {
	from {
		opacity: 0;
		transform: translateY(20px);
	}
	to {
		opacity: 1;
		transform: translateY(0);
	}
}

/* 主题样式 */
.theme-dark .form-section {
	background: rgba(42, 42, 42, 0.95);
}

.theme-dark .login-tabs {
	background: #333;
}

.theme-dark .tab-item {
	color: #ccc;
}

.theme-dark .input-wrapper {
	background: #444;
}

.theme-dark .form-input {
	color: #fff;
}

.theme-dark .social-btn {
	background: rgba(42, 42, 42, 0.9);
	color: #fff;
}

.theme-dark .wechat-btn {
	background: #07c160;
}
</style>