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
		color: '#667eea'
	},
	{
		name: t('profile.theme_dark'),
		value: 'dark',
		color: '#2c3e50'
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
	padding-bottom: 20px;
}

.profile-header {
	position: relative;
	padding: 80rpx 40rpx 40rpx;
	margin-bottom: 40rpx;
}

.header-bg {
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	height: 300rpx;
	background: #667eea;
	border-radius: 0 0 60rpx 60rpx;
}

.user-info {
	position: relative;
	z-index: 2;
	display: flex;
	align-items: center;
	gap: 40rpx;
}

.avatar-wrapper {
	position: relative;
}

.user-avatar {
	width: 160rpx;
	height: 160rpx;
	border-radius: 80rpx;
	border: 8rpx solid rgba(255, 255, 255, 0.3);
}

.avatar-edit {
	position: absolute;
	bottom: 0;
	right: 0;
	width: 48rpx;
	height: 48rpx;
	background: #fff;
	border-radius: 24rpx;
	display: flex;
	align-items: center;
	justify-content: center;
}

.edit-icon {
	font-size: 24rpx;
}

.user-details {
	flex: 1;
}

.user-name {
	display: block;
	font-size: 48rpx;
	font-weight: bold;
	color: #fff;
	margin-bottom: 10rpx;
}

.user-desc {
	font-size: 28rpx;
	color: rgba(255, 255, 255, 0.8);
}

.stats-section {
	margin: 0 40rpx 40rpx;
	background: #fff;
	border-radius: 30rpx;
	padding: 40rpx;
	box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
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
	font-size: 48rpx;
	font-weight: bold;
	color: #333;
	margin-bottom: 10rpx;
}

.stat-label {
	font-size: 24rpx;
	color: #999;
}

.menu-section {
	margin: 0 40rpx 40rpx;
}

.menu-group {
	background: #fff;
	border-radius: 30rpx;
	margin-bottom: 30rpx;
	overflow: hidden;
	box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
}

.menu-item {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 30rpx 40rpx;
	border-bottom: 1rpx solid #f0f0f0;
}

.menu-item:last-child {
	border-bottom: none;
}

.menu-left {
	display: flex;
	align-items: center;
	gap: 30rpx;
}

.menu-icon {
	width: 72rpx;
	height: 72rpx;
	border-radius: 16rpx;
	display: flex;
	align-items: center;
	justify-content: center;
}

.icon-text {
	font-size: 36rpx;
	color: #fff;
}

.menu-title {
	font-size: 32rpx;
	color: #333;
}

.menu-right {
	display: flex;
	align-items: center;
	gap: 20rpx;
}

.menu-badge {
	background: #ff4757;
	color: #fff;
	font-size: 24rpx;
	padding: 4rpx 16rpx;
	border-radius: 20rpx;
	min-width: 40rpx;
	text-align: center;
}

.menu-arrow {
	font-size: 32rpx;
	color: #ccc;
}

.theme-section,
.language-section {
	margin: 0 40rpx 40rpx;
	background: #fff;
	border-radius: 30rpx;
	padding: 40rpx;
	box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
}

.section-title {
	font-size: 32rpx;
	font-weight: bold;
	color: #333;
	margin-bottom: 30rpx;
}

.theme-options,
.language-options {
	display: flex;
	gap: 30rpx;
}

.theme-option,
.language-option {
	flex: 1;
	padding: 30rpx;
	border: 4rpx solid #f0f0f0;
	border-radius: 20rpx;
	text-align: center;
}

.theme-option.active,
.language-option.active {
	border-color: #007aff;
	background: rgba(0, 122, 255, 0.1);
}

.theme-preview {
	width: 80rpx;
	height: 80rpx;
	border-radius: 40rpx;
	margin: 0 auto 20rpx;
}

.theme-name,
.language-name {
	display: block;
	font-size: 28rpx;
	color: #333;
}

.language-flag {
	display: block;
	font-size: 48rpx;
	margin-bottom: 10rpx;
}

.logout-section {
	margin: 0 40rpx 80rpx;
}

.logout-btn {
	width: 100%;
	padding: 30rpx;
	background: #ff4757;
	color: #fff;
	border: none;
	border-radius: 20rpx;
	font-size: 32rpx;
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