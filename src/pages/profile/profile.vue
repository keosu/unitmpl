<template>
	<view class="profile-container" :class="`theme-${themeStore.currentTheme}`">
		<!-- 用户信息头部 -->
		<view class="profile-header">
			<view class="header-bg"></view>
			<view class="user-info">
				<view class="avatar-wrapper" @click="changeAvatar">
					<image :src="userInfo.avatar" class="user-avatar" mode="aspectFill" />
					<view class="avatar-edit">
						<text class="edit-icon">📷</text>
					</view>
				</view>
				<view class="user-details">
					<text class="user-name">{{ userInfo.name }}</text>
					<text class="user-desc">{{ userInfo.description }}</text>
				</view>
			</view>
		</view>

		<!-- 统计信息 -->
		<view class="stats-section">
			<view class="stats-grid">
				<view class="stat-item" v-for="(stat, index) in statsData" :key="index">
					<text class="stat-number">{{ stat.value }}</text>
					<text class="stat-label">{{ stat.label }}</text>
				</view>
			</view>
		</view>

		<!-- 功能菜单 -->
		<view class="menu-section">
			<view class="menu-group" v-for="(group, groupIndex) in menuGroups" :key="groupIndex">
				<view 
					class="menu-item" 
					v-for="(item, index) in group" 
					:key="index"
					@click="handleMenuClick(item)"
				>
					<view class="menu-left">
						<view class="menu-icon" :style="{ backgroundColor: item.color }">
							<text class="icon-text">{{ item.icon }}</text>
						</view>
						<text class="menu-title">{{ item.title }}</text>
					</view>
					<view class="menu-right">
						<text v-if="item.badge" class="menu-badge">{{ item.badge }}</text>
						<text class="menu-arrow">→</text>
					</view>
				</view>
			</view>
		</view>

		<!-- 主题切换 -->
		<view class="theme-section">
			<view class="section-title">{{ t('profile.theme') }}</view>
			<view class="theme-options">
				<view 
					v-for="theme in themeOptions" 
					:key="theme.value"
					class="theme-option"
					:class="{ active: themeStore.currentTheme === theme.value }"
					@click="switchTheme(theme.value)"
				>
					<view class="theme-preview" :style="{ background: theme.color }"></view>
					<text class="theme-name">{{ theme.name }}</text>
				</view>
			</view>
		</view>

		<!-- 语言切换 -->
		<view class="language-section">
			<view class="section-title">{{ t('profile.language') }}</view>
			<view class="language-options">
				<view 
					v-for="lang in languageOptions" 
					:key="lang.value"
					class="language-option"
					:class="{ active: currentLanguage === lang.value }"
					@click="switchLanguage(lang.value)"
				>
					<text class="language-flag">{{ lang.flag }}</text>
					<text class="language-name">{{ lang.name }}</text>
				</view>
			</view>
		</view>

		<!-- 退出按钮 -->
		<view class="logout-section">
			<button class="logout-btn" @click="handleLogout">
				{{ t('profile.logout') }}
			</button>
		</view>
	</view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useThemeStore } from '@/store/theme.js'
import { useUserStore } from '@/store/user.js'

const { t, locale } = useI18n()
const themeStore = useThemeStore()
const userStore = useUserStore()

// 检查登录状态
onMounted(() => {
	if (!userStore.isLoggedIn) {
		uni.showToast({
			title: t('common.login_required'),
			icon: 'none'
		})
		
		setTimeout(() => {
			uni.navigateBack({
				delta: 1
			})
		}, 1500)
		return
	}
})

const userInfo = ref({
	avatar: 'https://picsum.photos/100/100?random=1',
	name: 'User Name',
	description: t('profile.user_desc')
})

const currentLanguage = computed(() => locale.value)

const statsData = computed(() => [
	{ label: t('profile.messages'), value: '156' },
	{ label: t('profile.friends'), value: '24' },
	{ label: t('profile.points'), value: '892' }
])

const menuGroups = computed(() => [
	[
		{
			icon: '👤',
			title: t('profile.edit_profile'),
			color: '#FF6B6B'
		},
		{
			icon: '🔔',
			title: t('profile.notifications'),
			color: '#4ECDC4',
			badge: '3'
		},
		{
			icon: '🔒',
			title: t('profile.privacy'),
			color: '#45B7D1'
		}
	],
	[
		{
			icon: '❤️',
			title: t('profile.favorites'),
			color: '#FF69B4'
		},
		{
			icon: '📂',
			title: t('profile.downloads'),
			color: '#FFA500'
		},
		{
			icon: '📊',
			title: t('profile.statistics'),
			color: '#9B59B6'
		}
	],
	[
		{
			icon: '❓',
			title: t('profile.help'),
			color: '#95A5A6'
		},
		{
			icon: '📧',
			title: t('profile.feedback'),
			color: '#34495E'
		},
		{
			icon: 'ℹ️',
			title: t('profile.about'),
			color: '#3498DB'
		}
	]
])

const themeOptions = computed(() => [
	{
		name: t('profile.theme_light'),
		value: 'light',
		color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
	},
	{
		name: t('profile.theme_dark'),
		value: 'dark',
		color: 'linear-gradient(135deg, #2c3e50 0%, #34495e 100%)'
	}
])

const languageOptions = computed(() => [
	{
		name: '中文',
		value: 'zh-cn',
		flag: '🇨🇳'
	},
	{
		name: 'English',
		value: 'en-us',
		flag: '🇺🇸'
	}
])

const changeAvatar = () => {
	uni.chooseImage({
		count: 1,
		sizeType: ['compressed'],
		sourceType: ['album', 'camera'],
		success: (res) => {
			userInfo.value.avatar = res.tempFilePaths[0]
			uni.showToast({
				title: t('profile.avatar_updated'),
				icon: 'success'
			})
		}
	})
}

const handleMenuClick = (item) => {
	uni.showToast({
		title: item.title,
		icon: 'none'
	})
}

const switchTheme = (theme) => {
	themeStore.setTheme(theme)
	uni.showToast({
		title: t('profile.theme_switched'),
		icon: 'success'
	})
}

const switchLanguage = (lang) => {
	locale.value = lang
	uni.showToast({
		title: t('profile.language_switched'),
		icon: 'success'
	})
}

const handleLogout = () => {
	uni.showModal({
		title: t('profile.logout_confirm'),
		content: t('profile.logout_message'),
		success: (res) => {
			if (res.confirm) {
				userStore.logout()
				uni.reLaunch({
					url: '/pages/login/login'
				})
			}
		}
	})
}
</script>

<style scoped>
.profile-container {
	min-height: 100vh;
	background: #f8f9fa;
	transition: all 0.3s ease;
}

.profile-header {
	position: relative;
	padding: 40px 20px 20px;
	margin-bottom: 20px;
}

.header-bg {
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	height: 150px;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	border-radius: 0 0 30px 30px;
}

.user-info {
	position: relative;
	z-index: 2;
	display: flex;
	align-items: center;
	gap: 20px;
}

.avatar-wrapper {
	position: relative;
}

.user-avatar {
	width: 80px;
	height: 80px;
	border-radius: 40px;
	border: 4px solid rgba(255, 255, 255, 0.3);
}

.avatar-edit {
	position: absolute;
	bottom: 0;
	right: 0;
	width: 24px;
	height: 24px;
	background: #fff;
	border-radius: 12px;
	display: flex;
	align-items: center;
	justify-content: center;
}

.edit-icon {
	font-size: 12px;
}

.user-details {
	flex: 1;
}

.user-name {
	display: block;
	font-size: 24px;
	font-weight: bold;
	color: #fff;
	margin-bottom: 5px;
}

.user-desc {
	font-size: 14px;
	color: rgba(255, 255, 255, 0.8);
}

.stats-section {
	margin: 0 20px 20px;
	background: #fff;
	border-radius: 15px;
	padding: 20px;
	box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.stats-grid {
	display: flex;
	justify-content: space-around;
}

.stat-item {
	text-align: center;
}

.stat-number {
	display: block;
	font-size: 24px;
	font-weight: bold;
	color: #333;
	margin-bottom: 5px;
}

.stat-label {
	font-size: 12px;
	color: #999;
}

.menu-section {
	margin: 0 20px 20px;
}

.menu-group {
	background: #fff;
	border-radius: 15px;
	margin-bottom: 15px;
	overflow: hidden;
	box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.menu-item {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 15px 20px;
	border-bottom: 1px solid #f0f0f0;
}

.menu-item:last-child {
	border-bottom: none;
}

.menu-left {
	display: flex;
	align-items: center;
	gap: 15px;
}

.menu-icon {
	width: 36px;
	height: 36px;
	border-radius: 8px;
	display: flex;
	align-items: center;
	justify-content: center;
}

.icon-text {
	font-size: 18px;
	color: #fff;
}

.menu-title {
	font-size: 16px;
	color: #333;
}

.menu-right {
	display: flex;
	align-items: center;
	gap: 10px;
}

.menu-badge {
	background: #ff4757;
	color: #fff;
	font-size: 12px;
	padding: 2px 8px;
	border-radius: 10px;
	min-width: 20px;
	text-align: center;
}

.menu-arrow {
	font-size: 16px;
	color: #ccc;
}

.theme-section,
.language-section {
	margin: 0 20px 20px;
	background: #fff;
	border-radius: 15px;
	padding: 20px;
	box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.section-title {
	font-size: 16px;
	font-weight: bold;
	color: #333;
	margin-bottom: 15px;
}

.theme-options,
.language-options {
	display: flex;
	gap: 15px;
}

.theme-option,
.language-option {
	flex: 1;
	padding: 15px;
	border: 2px solid #f0f0f0;
	border-radius: 10px;
	text-align: center;
	transition: all 0.3s ease;
}

.theme-option.active,
.language-option.active {
	border-color: #007aff;
	background: rgba(0, 122, 255, 0.1);
}

.theme-preview {
	width: 40px;
	height: 40px;
	border-radius: 20px;
	margin: 0 auto 10px;
}

.theme-name,
.language-name {
	display: block;
	font-size: 14px;
	color: #333;
}

.language-flag {
	display: block;
	font-size: 24px;
	margin-bottom: 5px;
}

.logout-section {
	margin: 0 20px 40px;
}

.logout-btn {
	width: 100%;
	padding: 15px;
	background: #ff4757;
	color: #fff;
	border: none;
	border-radius: 10px;
	font-size: 16px;
	font-weight: bold;
}

/* 主题样式 */
.theme-dark .profile-container {
	background: #1a1a1a;
}

.theme-dark .stats-section,
.theme-dark .menu-group,
.theme-dark .theme-section,
.theme-dark .language-section {
	background: #2a2a2a;
}

.theme-dark .stat-number,
.theme-dark .menu-title,
.theme-dark .section-title,
.theme-dark .theme-name,
.theme-dark .language-name {
	color: #fff;
}

.theme-dark .menu-item {
	border-bottom-color: #333;
}
</style>