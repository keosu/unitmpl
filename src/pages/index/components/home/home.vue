<template>
	<view class="home-container" :class="`theme-${themeStore.currentTheme}`">
		<!-- 顶部搜索栏 -->
		<view class="search-bar">
			<view class="search-input">
				<text class="search-icon">🔍</text>
				<input type="text" :placeholder="t('home.search')" class="search-text" />
			</view>
		</view>

		<!-- 轮播图 -->
		<view class="banner-section">
			<swiper class="banner-swiper" indicator-dots autoplay circular>
				<swiper-item v-for="(item, index) in bannerList" :key="index">
					<image :src="item.image" class="banner-image" mode="aspectFill" />
				</swiper-item>
			</swiper>
		</view>

		<!-- 功能导航 -->
		<view class="nav-section">
			<view class="nav-grid">
				<view class="nav-item" v-for="(item, index) in navList" :key="index" @click="handleNavClick(item)">
					<view class="nav-icon" :style="{ backgroundColor: item.color }">
						<text class="nav-icon-text">{{ item.icon }}</text>
					</view>
					<text class="nav-text">{{ item.name }}</text>
				</view>
			</view>
		</view>

		<!-- 推荐商品 -->
		<view class="recommend-section">
			<view class="section-header">
				<view class="title-wrapper">
					<text class="section-title">🔥 {{ t('home.hot') }}</text>
					<text class="section-subtitle">{{ t('home.subtitle') }}</text>
				</view>
				<view class="more-btn">
					<text class="more-text">{{ t('home.more') }}</text>
					<text class="more-arrow">→</text>
				</view>
			</view>
			<scroll-view class="product-scroll" scroll-x show-scrollbar="false">
				<view class="product-list">
					<view class="product-item" v-for="(item, index) in productList" :key="index">
						<view class="product-image-wrapper">
							<image :src="item.image" class="product-image" mode="aspectFill" />
							<view class="product-badge">{{ t('home.hot_sale') }}</view>
						</view>
						<view class="product-info">
							<text class="product-name">{{ item.name }}</text>
							<view class="price-row">
								<text class="product-price">¥{{ item.price }}</text>
								<text class="product-original-price">¥{{ (parseFloat(item.price) * 1.2).toFixed(0)
								}}</text>
							</view>
							<view class="product-tags">
								<text class="tag">{{ t('home.free_shipping') }}</text>
								<text class="tag">{{ t('home.7_days_return') }}</text>
							</view>
						</view>
					</view>
				</view>
			</scroll-view>
		</view>

		<!-- 服务卡片 -->
		<view class="service-section">
			<view class="service-card">
				<view class="service-left">
					<text class="service-title">{{ t('home.professional_service') }}</text>
					<text class="service-desc">{{ t('home.provide_quality_service') }}</text>
					<button class="service-btn">{{ t('home.experience_now') }}</button>
				</view>
				<view class="service-right">
					<text class="service-icon">🚀</text>
				</view>
			</view>
		</view>

		<!-- 底部推荐 -->
		<view class="bottom-section">
			<view class="bottom-card">
				<text class="bottom-title">{{ t('home.today_special') }}</text>
				<text class="bottom-desc">{{ t('home.limited_time_discount') }}</text>
			</view>
		</view>
	</view>
</template>

<script setup>

import { useI18n } from "vue-i18n";
const { t } = useI18n();
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { getLocal, setLocal } from '@/utils/localStorage.js'
import { useThemeStore } from '@/store/theme.js'





const bannerList = ref([
	{ image: 'https://picsum.photos/400/200?random=1' },
	{ image: 'https://picsum.photos/400/200?random=2' },
	{ image: 'https://picsum.photos/400/200?random=3' },
	{ image: 'https://picsum.photos/400/200?random=4' }
])

const navList = computed(() => [
	{ name: t('home.product'), icon: '🛍️', color: '#FF6B6B' },
	{ name: t('home.service'), icon: '🔧', color: '#4ECDC4' },
	{ name: t('home.order'), icon: '📋', color: '#45B7D1' },
	{ name: t('home.my'), icon: '👤', color: '#96CEB4' }
])

const productList = computed(() => [
	{ name: t('home.product_1'), price: '99.00', image: 'https://picsum.photos/150/100?random=10' },
	{ name: t('home.product_2'), price: '199.00', image: 'https://picsum.photos/150/100?random=11' },
	{ name: t('home.product_3'), price: '299.00', image: 'https://picsum.photos/150/100?random=12' },
	{ name: t('home.product_4'), price: '399.00', image: 'https://picsum.photos/150/100?random=13' },
	{ name: t('home.product_5'), price: '499.00', image: 'https://picsum.photos/150/100?random=14' },
	{ name: t('home.product_6'), price: '599.00', image: 'https://picsum.photos/150/100?random=15' }
])

const handleNavClick = (item) => {
	console.log('点击了:', item.name)
	// 这里可以添加导航逻辑
}

// 获取主题 store
const themeStore = useThemeStore()

onMounted(() => {
	// 初始化主题
	themeStore.initTheme()
})




</script>

<style scoped>
.home-container {
	min-height: 100vh;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	transition: all 0.3s ease;
}

/* 使用全局主题样式 */
.home-container {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.theme-light .home-container {
	background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
}

/* 所有主题相关元素添加过渡效果 */
.search-bar,
.recommend-section,
.bottom-card,
.section-title,
.section-subtitle,
.bottom-title,
.bottom-desc {
	transition: all 0.3s ease;
}

/* 搜索栏 */
.search-bar {
	padding: 20px 20px 10px;
	transition: all 0.3s ease;
}

/* 搜索栏使用全局主题样式 */
.search-bar {
	background: rgba(255, 255, 255, 0.1);
}

.theme-light .search-bar {
	background: rgba(0, 0, 0, 0.05);
}

.search-input {
	display: flex;
	align-items: center;
	background: rgba(255, 255, 255, 0.9);
	border-radius: 25px;
	padding: 12px 20px;
}

.search-icon {
	font-size: 18px;
	margin-right: 10px;
}

.search-text {
	flex: 1;
	font-size: 16px;
	color: #333;
}

/* 轮播图 */
.banner-section {
	margin: 20px;
	border-radius: 15px;
	overflow: hidden;
	box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.banner-swiper {
	height: 200px;
}

.banner-image {
	width: 100%;
	height: 100%;
}

/* 功能导航 */
.nav-section {
	margin: 30px 20px;
}

.nav-grid {
	display: flex;
	justify-content: space-between;
	flex-wrap: wrap;
}

.nav-item {
	display: flex;
	flex-direction: column;
	align-items: center;
	width: 22%;
	margin-bottom: 20px;
}

.nav-icon {
	width: 60px;
	height: 60px;
	border-radius: 50%;
	display: flex;
	align-items: center;
	justify-content: center;
	margin-bottom: 10px;
	box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.nav-icon-text {
	font-size: 24px;
}

.nav-text {
	font-size: 14px;
	color: #fff;
	font-weight: 500;
	transition: color 0.3s ease;
}

/* 导航文字使用全局主题样式 */
.nav-text {
	color: #fff;
}

.theme-light .nav-text {
	color: #2c3e50;
}

/* 推荐商品 */
.recommend-section {
	margin: 30px 20px;
	border-radius: 20px;
	padding: 25px;
	backdrop-filter: blur(10px);
	transition: all 0.3s ease;
}

/* 浅色主题下的推荐区域 */
.theme-light .recommend-section {
	background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 249, 250, 0.8) 100%);
	border: 1px solid rgba(0, 0, 0, 0.1);
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

/* 暗黑主题下的推荐区域 */
.theme-dark .recommend-section {
	background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%);
	border: 1px solid rgba(255, 255, 255, 0.2);
	box-shadow: none;
}

/* 更多按钮使用全局主题样式 */
.more-btn {
	background: rgba(255, 255, 255, 0.2);
}

.more-text,
.more-arrow {
	color: #fff;
}

.theme-light .more-btn {
	background: rgba(0, 0, 0, 0.1);
}

.theme-light .more-text,
.theme-light .more-arrow {
	color: #2c3e50;
}

.section-header {
	display: flex;
	justify-content: space-between;
	align-items: flex-start;
	margin-bottom: 25px;
}

.title-wrapper {
	flex: 1;
}

.section-title {
	font-size: 20px;
	font-weight: bold;
	display: block;
	margin-bottom: 5px;
	transition: color 0.3s ease;
}

/* 浅色主题下的标题 */
.theme-light .section-title {
	color: #2c3e50;
	text-shadow: none;
}

/* 暗黑主题下的标题 */
.theme-dark .section-title {
	color: #fff;
	text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.section-subtitle {
	font-size: 12px;
	display: block;
	transition: color 0.3s ease;
}

/* 浅色主题下的副标题 */
.theme-light .section-subtitle {
	color: #6c757d;
}

/* 暗黑主题下的副标题 */
.theme-dark .section-subtitle {
	color: rgba(255, 255, 255, 0.7);
}

.more-btn {
	display: flex;
	align-items: center;
	background: rgba(255, 255, 255, 0.2);
	border-radius: 20px;
	padding: 8px 16px;
	transition: all 0.3s ease;
}

.more-btn:active {
	background: rgba(255, 255, 255, 0.3);
	transform: scale(0.95);
}

.more-text {
	font-size: 14px;
	color: #fff;
	margin-right: 5px;
}

.more-arrow {
	font-size: 16px;
	color: #fff;
	font-weight: bold;
}

.product-scroll {
	width: 100%;
}

.product-list {
	display: flex;
	white-space: nowrap;
	padding: 5px 0;
}

.product-item {
	display: inline-block;
	width: 160px;
	margin-right: 18px;
	background: rgba(255, 255, 255, 0.95);
	border-radius: 15px;
	overflow: visible;
	box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
	transition: all 0.3s ease;
	border: 1px solid rgba(255, 255, 255, 0.3);
}

/* 商品卡片使用全局主题样式 */
.product-item {
	background: rgba(255, 255, 255, 0.95);
	border: 1px solid rgba(255, 255, 255, 0.3);
	box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.theme-light .product-item {
	background: rgba(255, 255, 255, 0.98);
	border: 1px solid rgba(0, 0, 0, 0.1);
	box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.product-item:active {
	transform: translateY(-2px);
	box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
}

.product-image-wrapper {
	position: relative;
	width: 100%;
	height: 120px;
	overflow: hidden;
	border-radius: 15px 15px 0 0;
}

.product-image {
	width: 100%;
	height: 100%;
}

.product-badge {
	position: absolute;
	top: 8px;
	right: 8px;
	background: linear-gradient(45deg, #FF6B6B, #FF8E8E);
	color: #fff;
	font-size: 10px;
	padding: 4px 8px;
	border-radius: 12px;
	font-weight: bold;
	box-shadow: 0 2px 8px rgba(255, 107, 107, 0.3);
	z-index: 10;
	white-space: nowrap;
}

.product-info {
	padding: 15px;
}

.product-name {
	font-size: 14px;
	color: #333;
	display: block;
	margin-bottom: 8px;
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
	font-weight: 500;
	line-height: 1.3;
}

.price-row {
	display: flex;
	align-items: center;
	margin-bottom: 10px;
	white-space: nowrap;
}

.product-price {
	font-size: 18px;
	color: #FF6B6B;
	font-weight: bold;
	margin-right: 8px;
	white-space: nowrap;
}

.product-original-price {
	font-size: 12px;
	color: #999;
	text-decoration: line-through;
	white-space: nowrap;
}

.product-tags {
	display: flex;
	flex-wrap: wrap;
	gap: 5px;
	margin-top: 5px;
}

.tag {
	background: rgba(255, 107, 107, 0.1);
	color: #FF6B6B;
	font-size: 10px;
	padding: 3px 8px;
	border-radius: 8px;
	border: 1px solid rgba(255, 107, 107, 0.2);
	white-space: nowrap;
	line-height: 1.2;
}

/* 服务卡片 */
.service-section {
	margin: 30px 20px;
}

.service-card {
	display: flex;
	background: rgba(255, 255, 255, 0.95);
	border-radius: 15px;
	padding: 25px;
	box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
	transition: all 0.3s ease;
}

/* 服务卡片使用全局主题样式 */
.service-card {
	background: rgba(255, 255, 255, 0.95);
	border: 1px solid rgba(255, 255, 255, 0.2);
	box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.theme-light .service-card {
	background: rgba(255, 255, 255, 0.98);
	border: 1px solid rgba(0, 0, 0, 0.1);
	box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
}

.service-left {
	flex: 1;
}

.service-title {
	font-size: 20px;
	font-weight: bold;
	color: #333;
	display: block;
	margin-bottom: 10px;
	transition: color 0.3s ease;
}

.service-desc {
	font-size: 14px;
	color: #666;
	display: block;
	margin-bottom: 20px;
	transition: color 0.3s ease;
}

/* 服务文字使用全局主题样式 */
.service-title {
	color: #333;
}

.service-desc {
	color: #666;
}

.theme-light .service-title {
	color: #2c3e50;
}

.theme-light .service-desc {
	color: #6c757d;
}

.service-btn {
	background: linear-gradient(45deg, #FF6B6B, #FF8E8E);
	color: #fff;
	border: none;
	border-radius: 25px;
	padding: 10px 25px;
	font-size: 14px;
	font-weight: 500;
}

.service-right {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 80px;
}

.service-icon {
	font-size: 40px;
}

/* 底部推荐 */
.bottom-section {
	margin: 30px 20px 40px;
	padding-bottom: 100px;
}

.bottom-card {
	border-radius: 15px;
	padding: 25px;
	text-align: center;
	backdrop-filter: blur(10px);
	transition: all 0.3s ease;
}

/* 浅色主题下的底部卡片 */
.theme-light .bottom-card {
	background: rgba(255, 255, 255, 0.9);
	border: 1px solid rgba(0, 0, 0, 0.1);
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

/* 暗黑主题下的底部卡片 */
.theme-dark .bottom-card {
	background: rgba(255, 255, 255, 0.1);
	border: none;
	box-shadow: none;
}

.bottom-title {
	font-size: 18px;
	font-weight: bold;
	display: block;
	margin-bottom: 10px;
	transition: color 0.3s ease;
}

.bottom-desc {
	font-size: 14px;
	transition: color 0.3s ease;
}

/* 浅色主题下的底部文字 */
.theme-light .bottom-title {
	color: #2c3e50;
}

.theme-light .bottom-desc {
	color: #6c757d;
}

/* 暗黑主题下的底部文字 */
.theme-dark .bottom-title {
	color: #fff;
}

.theme-dark .bottom-desc {
	color: rgba(255, 255, 255, 0.8);
}
</style>
