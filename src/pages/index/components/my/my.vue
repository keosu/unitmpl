<template>
	<view class="my-container" :class="`theme-${themeStore.currentTheme}`">
		<!-- 用户信息头部 -->
		<view class="user-header">
			<view class="user-info">
				<view class="avatar-wrapper">
					<image src="https://picsum.photos/80/80?random=100" class="avatar" mode="aspectFill" />
					<view class="vip-badge">VIP</view>
				</view>
				<view class="user-details">
					<text class="username">{{ t('my.username') }}</text>
					<text class="user-level">{{ t('my.vip_level') }}</text>
					<text class="user-desc">{{ t('my.welcome_message') }}</text>
				</view>
				<view class="settings-btn">
					<text class="settings-icon">⚙️</text>
				</view>
			</view>
		</view>

		<!-- 数据统计卡片 -->
		<view class="stats-section">
			<view class="stats-card">
				<view class="stats-item">
					<text class="stats-number">128</text>
					<text class="stats-label">{{ t('my.favorites') }}</text>
				</view>
				<view class="stats-divider"></view>
				<view class="stats-item">
					<text class="stats-number">56</text>
					<text class="stats-label">{{ t('my.following') }}</text>
				</view>
				<view class="stats-divider"></view>
				<view class="stats-item">
					<text class="stats-number">89</text>
					<text class="stats-label">{{ t('my.footprints') }}</text>
				</view>
			</view>
		</view>

		<!-- 功能菜单 -->
		<view class="menu-section">
			<view class="menu-group">
				<view class="menu-item" v-for="(item, index) in menuList" :key="index" @click="handleMenuClick(item)">
					<view class="menu-icon" :style="{ backgroundColor: item.color }">
						<text class="menu-icon-text">{{ item.icon }}</text>
					</view>
					<view class="menu-content">
						<text class="menu-title">{{ item.title }}</text>
						<text class="menu-desc">{{ item.desc }}</text>
					</view>
					<text class="menu-arrow">→</text>
				</view>
			</view>
		</view>

		<!-- 语言切换 -->
		<view class="language-section">
			<view class="language-header">
				<text class="language-title">🌍 {{ t('my.language_settings') }}</text>
				<text class="language-subtitle">{{ t('my.language_subtitle') }}</text>
			</view>
			<view class="language-options">
				<view class="language-option" :class="{ active: currentLanguage === 'zh-cn' }"
					@click="switchLanguage('zh-cn')">
					<view class="language-flag">🇨🇳</view>
					<view class="language-info">
						<text class="language-name">{{ t('my.chinese_simplified') }}</text>
						<text class="language-desc">{{ t('my.chinese_desc') }}</text>
					</view>
					<view class="language-check" v-if="currentLanguage === 'zh-cn'">✓</view>
				</view>
				<view class="language-option" :class="{ active: currentLanguage === 'en-us' }"
					@click="switchLanguage('en-us')">
					<view class="language-flag">🇺🇸</view>
					<view class="language-info">
						<text class="language-name">{{ t('my.english') }}</text>
						<text class="language-desc">{{ t('my.english_desc') }}</text>
					</view>
					<view class="language-check" v-if="currentLanguage === 'en-us'">✓</view>
				</view>
			</view>
		</view>

		<!-- 主题设置 -->
		<view class="theme-section">
			<view class="theme-header">
				<text class="theme-title">🎨 {{ t('theme.title') }}</text>
				<text class="theme-subtitle">{{ t('theme.subtitle') }}</text>
			</view>
			<view class="theme-options">
				<view class="theme-option" :class="{ active: themeStore.currentTheme === 'light' }"
					@click="switchTheme('light')">
					<view class="theme-icon">☀️</view>
					<view class="theme-info">
						<text class="theme-name">{{ t('theme.light') }}</text>
						<text class="theme-desc">{{ t('theme.light_desc') }}</text>
					</view>
					<view class="theme-check" v-if="themeStore.currentTheme === 'light'">✓</view>
				</view>
				<view class="theme-option" :class="{ active: themeStore.currentTheme === 'dark' }"
					@click="switchTheme('dark')">
					<view class="theme-icon">🌙</view>
					<view class="theme-info">
						<text class="theme-name">{{ t('theme.dark') }}</text>
						<text class="theme-desc">{{ t('theme.dark_desc') }}</text>
					</view>
					<view class="theme-check" v-if="themeStore.currentTheme === 'dark'">✓</view>
				</view>
				<view class="theme-option" :class="{ active: themeStore.currentTheme === 'auto' }"
					@click="switchTheme('auto')">
					<view class="theme-icon">🔄</view>
					<view class="theme-info">
						<text class="theme-name">{{ t('theme.auto') }}</text>
						<text class="theme-desc">{{ t('theme.auto_desc') }}</text>
					</view>
					<view class="theme-check" v-if="themeStore.currentTheme === 'auto'">✓</view>
				</view>
			</view>
		</view>

		<!-- 快捷服务 -->
		<view class="service-section">
			<view class="service-header">
				<text class="service-title">💎 {{ t('my.exclusive_service') }}</text>
				<text class="service-subtitle">{{ t('my.service_subtitle') }}</text>
			</view>
			<view class="service-grid">
				<view class="service-item" v-for="(service, index) in serviceList" :key="index"
					@click="handleServiceClick(service)">
					<view class="service-icon-wrapper" :style="{ backgroundColor: service.color }">
						<text class="service-icon-text">{{ service.icon }}</text>
					</view>
					<text class="service-name">{{ service.name }}</text>
				</view>
			</view>
		</view>



		<!-- 底部信息 -->
		<view class="bottom-section">
			<view class="version-info">
				<text class="version-text">{{ t('my.current_version') }}</text>
			</view>
		</view>
	</view>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { getLocal, setLocal } from '@/utils/localStorage.js'
import { useThemeStore } from '@/store/theme.js'
import { showLoading, hideLoading, showToast, showModal } from '@/utils/utils'
const { t, locale } = useI18n()

const menuList = computed(() => [
	{ title: t('my.my_orders'), desc: t('my.orders_desc'), icon: '📋', color: '#FF6B6B' },
	{ title: t('my.my_favorites'), desc: t('my.favorites_desc'), icon: '❤️', color: '#FF8E8E' },
	{ title: t('my.coupons'), desc: t('my.coupons_desc'), icon: '🎫', color: '#4ECDC4' },
	{ title: t('my.points_mall'), desc: t('my.points_desc'), icon: '⭐', color: '#45B7D1' },
	{ title: t('my.customer_service'), desc: t('my.service_desc'), icon: '💬', color: '#96CEB4' },
	{ title: t('my.settings'), desc: t('my.settings_desc'), icon: '🔧', color: '#FFA726' }
])

const serviceList = computed(() => [
	{ name: t('my.online_service'), icon: '💬', color: '#FF6B6B' },
	{ name: t('my.feedback'), icon: '📝', color: '#4ECDC4' },
	{ name: t('my.help_center'), icon: '❓', color: '#45B7D1' },
	{ name: t('my.about_us'), icon: 'ℹ️', color: '#96CEB4' }
])



const handleMenuClick = (item) => {
	console.log('点击了菜单:', item.title)
	// 这里可以添加菜单点击逻辑
}

// 当前语言
const currentLanguage = ref('zh-cn')

// 获取主题 store
const themeStore = useThemeStore()

// 初始化语言和主题
onMounted(() => {
	const savedLanguage = getLocal('language')
	if (savedLanguage) {
		currentLanguage.value = savedLanguage
		locale.value = savedLanguage
	}
	
	// 初始化主题
	themeStore.initTheme()
})

// 切换语言
const switchLanguage = (lang) => {
	if (lang !== currentLanguage.value) {
		currentLanguage.value = lang
		locale.value = lang
		setLocal('language', lang)

		// 显示切换成功提示
		showToast(t('my.language_switched'))

		//需要手动设置下标题title
		uni.setNavigationBarTitle({
			title: t('tabbar.my')
		})
	}
}

// 切换主题
const switchTheme = (theme) => {
	themeStore.switchTheme(theme)
	applyTheme(theme)
	
	// 显示切换成功提示
	showToast(t('theme.theme_switched'))
}

// 应用主题
const applyTheme = (theme) => {
	// 在 UniApp 中，我们通过动态类名来切换主题
	console.log('应用主题:', theme)
	
	// 处理 auto 模式
	if (theme === 'auto') {
		// 在 UniApp 中，我们可以通过系统信息来判断
		// 这里暂时设置为暗色主题作为默认值
		// 实际项目中可以通过 uni.getSystemInfo 获取系统信息
		console.log('自动主题模式')
	}
	
	// 可以在这里添加其他主题相关的逻辑
	// 比如更新状态管理、发送事件等
	
	// 强制重新渲染以确保样式更新
	nextTick(() => {
		console.log('主题切换完成:', theme)
	})
}

const handleServiceClick = (service) => {
	console.log('点击了服务:', service.name)
	// 这里可以添加服务点击逻辑
}
</script>

<style scoped>
/* CSS 变量定义 */
:root {
	--primary-bg: #1a1a1a;
	--secondary-bg: #2d2d2d;
	--text-primary: #ffffff;
	--text-secondary: #b0b0b0;
	--border-color: #404040;
}

/* 主题类 */
.theme-light {
	--primary-bg: #f8f9fa;
	--secondary-bg: #ffffff;
	--text-primary: #2c3e50;
	--text-secondary: #6c757d;
	--border-color: #e9ecef;
}

.theme-dark {
	--primary-bg: #1a1a1a;
	--secondary-bg: #2d2d2d;
	--text-primary: #ffffff;
	--text-secondary: #b0b0b0;
	--border-color: #404040;
}

.my-container {
	min-height: 100vh;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	padding-bottom: 40px;
	transition: all 0.3s ease;
}

/* 所有主题相关元素添加过渡效果 */
.user-header,
.stats-card,
.menu-group,
.language-section,
.theme-section,
.service-section,
.language-option,
.theme-option,
.version-info,
.avatar,
.stats-divider,
.menu-item,
.settings-btn {
	transition: all 0.3s ease;
}

/* 使用全局主题样式 */
.my-container {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.theme-light .my-container {
	background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
}

/* 浅色主题下的样式调整 - 保持原有样式 */
.theme-light .user-header {
	background: rgba(0, 0, 0, 0.08);
	border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.theme-light .stats-card {
	background: rgba(255, 255, 255, 0.8);
	border: 1px solid rgba(0, 0, 0, 0.1);
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.theme-light .menu-group {
	background: rgba(255, 255, 255, 0.8);
	border: 1px solid rgba(0, 0, 0, 0.1);
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.theme-light .language-section,
.theme-light .theme-section,
.theme-light .service-section {
	background: rgba(255, 255, 255, 0.8);
	border: 1px solid rgba(0, 0, 0, 0.1);
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.theme-light .language-option,
.theme-light .theme-option {
	background: rgba(0, 0, 0, 0.03);
	border: 1px solid rgba(0, 0, 0, 0.05);
}

.theme-light .language-option.active,
.theme-light .theme-option.active {
	background: rgba(0, 0, 0, 0.08);
	border-color: rgba(0, 0, 0, 0.15);
}

.theme-light .version-info {
	background: rgba(255, 255, 255, 0.8);
	border: 1px solid rgba(0, 0, 0, 0.1);
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

/* 浅色主题下的文字颜色调整 */
.theme-light .language-title,
.theme-light .theme-title,
.theme-light .service-title {
	color: #2c3e50;
	text-shadow: none;
}

.theme-light .language-subtitle,
.theme-light .theme-subtitle,
.theme-light .service-subtitle {
	color: #6c757d;
}

.theme-light .language-name,
.theme-light .theme-name {
	color: #2c3e50;
}

.theme-light .language-desc,
.theme-light .theme-desc {
	color: #6c757d;
}

.theme-light .menu-arrow {
	color: #6c757d;
}

.theme-light .version-text {
	color: #6c757d;
}

/* 用户信息头部 */
.user-header {
	padding: 40px 20px 30px;
	background: rgba(255, 255, 255, 0.1);
	backdrop-filter: blur(10px);
}

/* 暗黑主题下的样式优化 */
.theme-dark .user-header {
	background: rgba(255, 255, 255, 0.15);
	border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.theme-dark .stats-card {
	background: rgba(255, 255, 255, 0.15);
	border: 1px solid rgba(255, 255, 255, 0.2);
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.theme-dark .menu-group {
	background: rgba(255, 255, 255, 0.15);
	border: 1px solid rgba(255, 255, 255, 0.2);
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.theme-dark .language-section,
.theme-dark .theme-section,
.theme-dark .service-section {
	background: rgba(255, 255, 255, 0.15);
	border: 1px solid rgba(255, 255, 255, 0.2);
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.theme-dark .language-option,
.theme-dark .theme-option {
	background: rgba(255, 255, 255, 0.1);
	border: 1px solid rgba(255, 255, 255, 0.1);
}

.theme-dark .language-option.active,
.theme-dark .theme-option.active {
	background: rgba(255, 255, 255, 0.2);
	border-color: rgba(255, 255, 255, 0.3);
}

.theme-dark .version-info {
	background: rgba(255, 255, 255, 0.15);
	border: 1px solid rgba(255, 255, 255, 0.2);
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.user-info {
	display: flex;
	align-items: center;
}

.avatar-wrapper {
	position: relative;
	margin-right: 20px;
}

.avatar {
	width: 80px;
	height: 80px;
	border-radius: 50%;
	border: 3px solid rgba(255, 255, 255, 0.3);
	transition: border-color 0.3s ease;
}

/* 浅色主题下的头像边框 */
.theme-light .avatar {
	border-color: rgba(0, 0, 0, 0.1);
}

.vip-badge {
	position: absolute;
	top: -5px;
	right: -5px;
	background: linear-gradient(45deg, #FFD700, #FFA500);
	color: #fff;
	font-size: 10px;
	padding: 3px 6px;
	border-radius: 10px;
	font-weight: bold;
	box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
}

.user-details {
	flex: 1;
}

.username {
	font-size: 24px;
	font-weight: bold;
	color: var(--text-primary);
	display: block;
	margin-bottom: 5px;
	text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
	transition: color 0.3s ease;
}

.user-level {
	background: linear-gradient(45deg, #FFD700, #FFA500);
	color: #fff;
	font-size: 12px;
	padding: 4px 8px;
	border-radius: 12px;
	display: inline-block;
	margin-bottom: 8px;
	font-weight: bold;
}

.user-desc {
	font-size: 14px;
	color: var(--text-secondary);
	display: block;
	transition: color 0.3s ease;
}

.settings-btn {
	width: 40px;
	height: 40px;
	background: rgba(255, 255, 255, 0.2);
	border-radius: 50%;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: all 0.3s ease;
}

.settings-btn:active {
	background: rgba(255, 255, 255, 0.3);
	transform: scale(0.95);
}

/* 浅色主题下的设置按钮 */
.theme-light .settings-btn {
	background: rgba(0, 0, 0, 0.1);
}

.theme-light .settings-btn:active {
	background: rgba(0, 0, 0, 0.15);
}

.settings-icon {
	font-size: 18px;
}

/* 数据统计卡片 */
.stats-section {
	margin: 20px;
}

.stats-card {
	background: rgba(255, 255, 255, 0.15);
	border-radius: 20px;
	padding: 25px;
	backdrop-filter: blur(10px);
	border: 1px solid rgba(255, 255, 255, 0.2);
	display: flex;
	justify-content: space-around;
	align-items: center;
}

.stats-item {
	text-align: center;
	flex: 1;
}

.stats-number {
	font-size: 28px;
	font-weight: bold;
	color: var(--text-primary);
	display: block;
	margin-bottom: 5px;
	text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
	transition: color 0.3s ease;
}

.stats-label {
	font-size: 12px;
	color: var(--text-secondary);
	transition: color 0.3s ease;
}

.stats-divider {
	width: 1px;
	height: 40px;
	background: rgba(255, 255, 255, 0.3);
	transition: background-color 0.3s ease;
}

/* 浅色主题下的分割线 */
.theme-light .stats-divider {
	background: rgba(0, 0, 0, 0.1);
}

/* 功能菜单 */
.menu-section {
	margin: 20px;
}

.menu-group {
	background: rgba(255, 255, 255, 0.15);
	border-radius: 20px;
	backdrop-filter: blur(10px);
	border: 1px solid rgba(255, 255, 255, 0.2);
	overflow: hidden;
}

.menu-item {
	display: flex;
	align-items: center;
	padding: 20px;
	border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	transition: all 0.3s ease;
}

/* 浅色主题下的菜单项边框 */
.theme-light .menu-item {
	border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.menu-item:last-child {
	border-bottom: none;
}

.menu-item:active {
	background: rgba(255, 255, 255, 0.1);
}

/* 浅色主题下的菜单项激活状态 */
.theme-light .menu-item:active {
	background: rgba(0, 0, 0, 0.05);
}

.menu-icon {
	width: 50px;
	height: 50px;
	border-radius: 15px;
	display: flex;
	align-items: center;
	justify-content: center;
	margin-right: 15px;
	box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.menu-icon-text {
	font-size: 20px;
}

.menu-content {
	flex: 1;
}

.menu-title {
	font-size: 16px;
	font-weight: 500;
	color: var(--text-primary);
	display: block;
	margin-bottom: 3px;
	transition: color 0.3s ease;
}

.menu-desc {
	font-size: 12px;
	color: var(--text-secondary);
	transition: color 0.3s ease;
}

.menu-arrow {
	font-size: 18px;
	color: rgba(255, 255, 255, 0.6);
	font-weight: bold;
}

/* 语言切换 */
.language-section {
	margin: 20px;
	background: rgba(255, 255, 255, 0.15);
	border-radius: 20px;
	padding: 25px;
	backdrop-filter: blur(10px);
	border: 1px solid rgba(255, 255, 255, 0.2);
}

.language-header {
	text-align: center;
	margin-bottom: 20px;
}

.language-title {
	font-size: 18px;
	font-weight: bold;
	color: #fff;
	display: block;
	margin-bottom: 5px;
	text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.language-subtitle {
	font-size: 12px;
	color: rgba(255, 255, 255, 0.7);
}

.language-options {
	display: flex;
	flex-direction: column;
	gap: 12px;
}

.language-option {
	display: flex;
	align-items: center;
	padding: 15px;
	background: rgba(255, 255, 255, 0.1);
	border-radius: 15px;
	border: 2px solid transparent;
	transition: all 0.3s ease;
	cursor: pointer;
}

.language-option.active {
	background: rgba(255, 255, 255, 0.2);
	border-color: rgba(255, 255, 255, 0.4);
	transform: translateX(5px);
}

.language-option:active {
	transform: scale(0.98);
}

.language-flag {
	font-size: 24px;
	margin-right: 15px;
}

.language-info {
	flex: 1;
}

.language-name {
	font-size: 16px;
	font-weight: 500;
	color: #fff;
	display: block;
	margin-bottom: 3px;
}

.language-desc {
	font-size: 12px;
	color: rgba(255, 255, 255, 0.7);
}

.language-check {
	width: 24px;
	height: 24px;
	background: linear-gradient(45deg, #4ECDC4, #44A08D);
	color: #fff;
	border-radius: 50%;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 14px;
	font-weight: bold;
	box-shadow: 0 2px 8px rgba(78, 205, 196, 0.3);
}

/* 主题设置 */
.theme-section {
	margin: 20px;
	background: rgba(255, 255, 255, 0.15);
	border-radius: 20px;
	padding: 25px;
	backdrop-filter: blur(10px);
	border: 1px solid rgba(255, 255, 255, 0.2);
}

.theme-header {
	text-align: center;
	margin-bottom: 20px;
}

.theme-title {
	font-size: 18px;
	font-weight: bold;
	color: #fff;
	display: block;
	margin-bottom: 5px;
	text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.theme-subtitle {
	font-size: 12px;
	color: rgba(255, 255, 255, 0.7);
}

.theme-options {
	display: flex;
	flex-direction: column;
	gap: 12px;
}

.theme-option {
	display: flex;
	align-items: center;
	padding: 15px;
	background: rgba(255, 255, 255, 0.1);
	border-radius: 15px;
	border: 2px solid transparent;
	transition: all 0.3s ease;
	cursor: pointer;
}

.theme-option.active {
	background: rgba(255, 255, 255, 0.2);
	border-color: rgba(255, 255, 255, 0.4);
	transform: translateX(5px);
}

.theme-option:active {
	transform: scale(0.98);
}

.theme-icon {
	font-size: 24px;
	margin-right: 15px;
}

.theme-info {
	flex: 1;
}

.theme-name {
	font-size: 16px;
	font-weight: 500;
	color: #fff;
	display: block;
	margin-bottom: 3px;
}

.theme-desc {
	font-size: 12px;
	color: rgba(255, 255, 255, 0.7);
}

.theme-check {
	width: 24px;
	height: 24px;
	background: linear-gradient(45deg, #4ECDC4, #44A08D);
	color: #fff;
	border-radius: 50%;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 14px;
	font-weight: bold;
	box-shadow: 0 2px 8px rgba(78, 205, 196, 0.3);
}

/* 快捷服务 */
.service-section {
	margin: 20px;
	background: rgba(255, 255, 255, 0.15);
	border-radius: 20px;
	padding: 25px;
	backdrop-filter: blur(10px);
	border: 1px solid rgba(255, 255, 255, 0.2);
}

.service-header {
	text-align: center;
	margin-bottom: 20px;
}

.service-title {
	font-size: 18px;
	font-weight: bold;
	color: #fff;
	display: block;
	margin-bottom: 5px;
	text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.service-subtitle {
	font-size: 12px;
	color: rgba(255, 255, 255, 0.7);
}

.service-grid {
	display: grid;
	grid-template-columns: repeat(4, 1fr);
	gap: 15px;
}

.service-item {
	text-align: center;
	transition: all 0.3s ease;
}

.service-item:active {
	transform: scale(0.95);
}

/* 浅色主题下的服务项激活状态 */
.theme-light .service-item:active {
	transform: scale(0.95);
}

.service-icon-wrapper {
	width: 50px;
	height: 50px;
	border-radius: 15px;
	display: flex;
	align-items: center;
	justify-content: center;
	margin: 0 auto 10px;
	box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.service-icon-text {
	font-size: 20px;
}

.service-name {
	font-size: 12px;
	color: var(--text-primary);
	font-weight: 500;
	transition: color 0.3s ease;
}



/* 底部信息 */
.bottom-section {
	margin: 20px;
	text-align: center;
}

.version-info {
	background: rgba(255, 255, 255, 0.1);
	border-radius: 15px;
	padding: 15px;
	backdrop-filter: blur(10px);
}

.version-text {
	font-size: 12px;
	color: rgba(255, 255, 255, 0.6);
}
</style>
