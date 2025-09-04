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
			<view class="theme-buttons">
				<up-button
					v-for="theme in themeOptions" 
					:key="theme.value"
					:type="themeStore.currentTheme === theme.value ? 'primary' : 'info'"
					:plain="themeStore.currentTheme !== theme.value"
					size="small"
					shape="round"
					customStyle="flex: 1; margin: 0 10rpx; height: 120rpx;"
					@click="switchTheme(theme.value)"
				>
					<view class="theme-button-content">
						<text class="theme-emoji">{{ theme.emoji }}</text>
						<text class="theme-name">{{ theme.name }}</text>
					</view>
				</up-button>
			</view>
		</view>

		<!-- 语言切换 -->
		<view class="language-section">
			<view class="section-title">{{ t('profile.language') }}</view>
			<view class="language-buttons">
				<up-button
					v-for="lang in languageOptions" 
					:key="lang.value"
					:type="currentLanguage === lang.value ? 'success' : 'info'"
					:plain="currentLanguage !== lang.value"
					size="small"
					shape="round"
					customStyle="flex: 1; margin: 0 10rpx; height: 120rpx;"
					@click="switchLanguage(lang.value)"
				>
					<view class="language-button-content">
						<text class="language-flag">{{ lang.flag }}</text>
						<text class="language-name">{{ lang.name }}</text>
					</view>
				</up-button>
			</view>
		</view>

		<!-- 退出按钮 -->
		<view class="logout-section">
			<up-button 
				type="error"
				size="large"
				shape="round"
				customStyle="width: 100%;"
				@click="handleLogout"
			>
				{{ t('profile.logout') }}
			</up-button>
		</view>
	</view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useThemeStore } from '@/store/theme.js'
import { useUserStore } from '@/store/user.js'
import { setLocal, getLocal } from '@/utils/localStorage.js'

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
		color: '#f8f9fa',
		emoji: '☀️' // 太阳emoji
	},
	{
		name: t('profile.theme_dark'),
		value: 'dark',
		color: '#2d3748',
		emoji: '🌙' // 月亮emoji
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
	// 保存语言设置到本地存储
	setLocal('language', lang)
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
/* 浅色主题（默认） */
.profile-container {
	min-height: 100vh;
	background: #f8f9fa;
	padding-bottom: 20px;
}

/* 暗色主题 */
.theme-dark .profile-container {
	background: #1a1a1a;
}

.theme-dark .header-bg {
	background: #4a5568 !important;
}

.theme-dark .stats-section,
.theme-dark .menu-group,
.theme-dark .theme-section,
.theme-dark .language-section {
	background: #2d3748;
	box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.3);
}

.theme-dark .stat-number {
	color: #63b3ed;
}

.theme-dark .stat-label,
.theme-dark .menu-title,
.theme-dark .section-title {
	color: #e2e8f0;
}

.theme-dark .menu-item {
	border-bottom-color: #4a5568;
}

.theme-dark .menu-arrow {
	color: #a0aec0;
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
	color: #007aff;
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

/* 主题按钮样式 */
.theme-buttons,
.language-buttons {
	display: flex;
	gap: 20rpx;
	align-items: center;
}

.theme-button-content,
.language-button-content {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 8rpx;
	padding: 10rpx 5rpx;
}

.theme-emoji {
	font-size: 48rpx;
	line-height: 1;
}

.theme-name,
.language-name {
	font-size: 20rpx;
	color: inherit;
	text-align: center;
	line-height: 1.2;
}

.language-flag {
	font-size: 28rpx;
	margin-bottom: 4rpx;
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

/* 响应式设计 - 小屏幕优化 */
@media (max-width: 750rpx) {
	.theme-buttons,
	.language-buttons {
		flex-direction: column;
		gap: 20rpx;
	}
	
	.theme-buttons > *, 
	.language-buttons > * {
		width: 100%;
		margin: 0;
	}
}
</style>