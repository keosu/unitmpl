<template>
	<view class="order-container" :class="`theme-${themeStore.currentTheme}`">
		<!-- 顶部搜索栏 -->
		<view class="search-header">
			<view class="search-box">
				<text class="search-icon">🔍</text>
				<input type="text"   :placeholder="t('order.search')" class="search-input" />
			</view>
		</view>

		<!-- 主要内容区域 -->
		<view class="main-content">
			<!-- 左侧分类导航 -->
			<view class="category-sidebar">
				<scroll-view class="sidebar-scroll" scroll-y show-scrollbar="false">
					<view 
						class="category-item" 
						:class="{ active: activeTab === index }"
						v-for="(tab, index) in categoryTabs" 
						:key="index"
						@click="switchTab(index)"
					>
						<view class="category-icon" :style="{ backgroundColor: getCategoryColor(tab.name) }">
							<text class="category-icon-text">{{ getCategoryIcon(tab.name) }}</text>
						</view>
						<text class="category-name">{{ tab.name }}</text>
						<text class="category-count" v-if="getCategoryCount(tab.name) > 0">{{ getCategoryCount(tab.name) }}</text>
					</view>
				</scroll-view>
			</view>

			<!-- 右侧商品区域 -->
			<view class="products-area">
				<!-- 分类标题和筛选 -->
				<view class="category-header">
					<view class="category-title">
						<text class="title-text">{{ categoryTabs[activeTab].name }}</text>
						<text class="title-subtitle">{{ t('order.subtitle') }}</text>
					</view>
					<view class="filter-actions">
						<view class="filter-btn" @click="showSortModal">
							<text class="filter-text">{{ currentSort }}</text>
							<text class="filter-arrow">▼</text>
						</view>
						<view class="filter-btn" @click="showPriceModal">
							<text class="filter-text">{{ currentPrice }}</text>
							<text class="filter-arrow">▼</text>
						</view>
					</view>
				</view>

				<!-- 商品列表 -->
				<scroll-view class="products-scroll" scroll-y show-scrollbar="false">
					<view class="products-list" v-if="filteredProducts.length > 0">
						<view 
							class="product-item" 
							v-for="(product, index) in filteredProducts" 
							:key="index"
							@click="selectProduct(product)"
						>
							<view class="product-image-wrapper">
								<image :src="product.image" class="product-image" mode="aspectFill" />
								<view class="product-badge" v-if="product.badge">{{ product.badge }}</view>
							</view>
							<view class="product-info">
								<text class="product-name">{{ product.name }}</text>
								<view class="product-price-section">
									<text class="product-price">¥{{ product.price }}</text>
									<text class="product-original" v-if="product.originalPrice">¥{{ product.originalPrice }}</text>
								</view>
								<view class="product-tags" v-if="product.tags && product.tags.length > 0">
									<text class="tag" v-for="(tag, tagIndex) in product.tags.slice(0, 2)" :key="tagIndex">{{ tag }}</text>
								</view>
							</view>
						</view>
					</view>

					<!-- 加载更多 -->
					<view class="load-more" v-if="hasMore && filteredProducts.length > 0">
						<view class="load-btn">
							<text class="load-text">{{ t('order.load_more') }}</text>
						</view>
					</view>

					<!-- 空状态 -->
					<view class="empty-state" v-if="filteredProducts.length === 0">
						<text class="empty-icon">📦</text>
						<text class="empty-title">{{ t('order.empty_title') }}</text>
						<text class="empty-desc">{{ t('order.empty_desc') }}</text>
					</view>
				</scroll-view>
			</view>
		</view>
	</view>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { getLocal, setLocal } from '@/utils/localStorage.js'
import { useThemeStore } from '@/store/theme.js'

const { t } = useI18n()

const activeTab = ref(0)
const categoryTabs = computed(() => [
	{ name: t('order.all'), id: 'all' },
	{ name: t('order.digital'), id: 'digital' },
	{ name: t('order.clothing'), id: 'clothing' },
	{ name: t('order.home'), id: 'home' },
	{ name: t('order.beauty'), id: 'beauty' },
	{ name: t('order.sports'), id: 'sports' },
	{ name: t('order.books'), id: 'books' },
	{ name: t('order.food'), id: 'food' },
	{ name: t('order.baby'), id: 'baby' },
	{ name: t('order.auto'), id: 'auto' },
	{ name: t('order.medicine'), id: 'medicine' },
	{ name: t('order.jewelry'), id: 'jewelry' }
])

const currentSort = computed(() => t('order.sort'))
const currentPrice = computed(() => t('order.price'))
const products = computed(() => [
	{
		name: t('order.digital_product'),
		category: t('order.digital'),
		price: '299',
		originalPrice: '399',
		image: 'https://picsum.photos/200/200?random=20',
		badge: t('order.hot_sale'),
		tags: [t('order.free_shipping'), t('order.7_days_return')]
	},
	{
		name: t('order.clothing_product'),
		category: t('order.clothing'),
		price: '89',
		originalPrice: '129',
		image: 'https://picsum.photos/200/200?random=21',
		badge: t('order.new_product'),
		tags: [t('order.free_shipping'), t('order.30_days_return')]
	},
	{
		name: '智能手表 运动健康监测',
		category: t('order.digital'),
		price: '899',
		originalPrice: '1299',
		image: 'https://picsum.photos/200/200?random=22',
		badge: t('order.limited_time_discount'),
		tags: [t('order.free_shipping'), t('order.7_days_return')]
	},
	{
		name: t('order.home_product'),
		category: t('order.home'),
		price: '199',
		image: 'https://picsum.photos/200/200?random=23',
		tags: [t('order.free_shipping'), t('order.15_days_return')]
	},
	{
		name: t('order.beauty_product'),
		category: t('order.beauty'),
		price: '299',
		originalPrice: '399',
		image: 'https://picsum.photos/200/200?random=24',
		badge: t('order.recommended'),
		tags: [t('order.free_shipping'), t('order.7_days_return')]
	},
	{
		name: t('order.sports_product'),
		category: t('order.sports'),
		price: '399',
		originalPrice: '599',
		image: 'https://picsum.photos/200/200?random=25',
		badge: t('order.hot_sale'),
		tags: [t('order.free_shipping'), t('order.30_days_return')]
	},
	{
		name: t('order.book_product'),
		category: t('order.books'),
		price: '59',
		image: 'https://picsum.photos/200/200?random=26',
		tags: [t('order.free_shipping'), t('order.7_days_return')]
	},
	{
		name: t('order.food_product'),
		category: t('order.food'),
		price: '99',
		originalPrice: '129',
		image: 'https://picsum.photos/200/200?random=27',
		badge: t('order.limited_time_discount'),
		tags: [t('order.free_shipping'), t('order.7_days_return')]
	},
	{
		name: t('order.baby_product'),
		category: t('order.baby'),
		price: '199',
		image: 'https://picsum.photos/200/200?random=28',
		tags: [t('order.free_shipping'), t('order.7_days_return')]
	},
	{
		name: t('order.auto_product'),
		category: t('order.auto'),
		price: '159',
		image: 'https://picsum.photos/200/200?random=29',
		tags: [t('order.free_shipping'), t('order.15_days_return')]
	}
])

const hasMore = ref(true)

// 计算属性
const filteredProducts = computed(() => {
	if (activeTab.value === 0) {
		return products.value
	}
	const category = categoryTabs.value[activeTab.value].name
	return products.value.filter(product => product.category === category)
})

// 方法
const switchTab = (index) => {
	activeTab.value = index
}

const getCategoryCount = (categoryName) => {
	if (categoryName === t('order.all')) {
		return products.value.length
	}
	return products.value.filter(product => product.category === categoryName).length
}

const getCategoryIcon = (categoryName) => {
	const iconMap = {
		[t('order.all')]: '🏠',
		[t('order.digital')]: '📱',
		[t('order.clothing')]: '👕',
		[t('order.home')]: '🏠',
		[t('order.beauty')]: '💄',
		[t('order.sports')]: '🏃',
		[t('order.books')]: '📚',
		[t('order.food')]: '🍎',
		[t('order.baby')]: '👶',
		[t('order.auto')]: '🚗',
		[t('order.medicine')]: '💊',
		[t('order.jewelry')]: '💎'
	}
	return iconMap[categoryName] || '🛍️'
}

const getCategoryColor = (categoryName) => {
	const colorMap = {
		[t('order.all')]: '#FF6B6B',
		[t('order.digital')]: '#4ECDC4',
		[t('order.clothing')]: '#45B7D1',
		[t('order.home')]: '#96CEB4',
		[t('order.beauty')]: '#FFEAA7',
		[t('order.sports')]: '#DDA0DD',
		[t('order.books')]: '#98D8C8',
		[t('order.food')]: '#F7DC6F',
		[t('order.baby')]: '#BB8FCE',
		[t('order.auto')]: '#85C1E9',
		[t('order.medicine')]: '#F8C471',
		[t('order.jewelry')]: '#F1948A'
	}
	return colorMap[categoryName] || '#FF6B6B'
}

const showSortModal = () => {
	console.log('显示排序弹窗')
}

const showPriceModal = () => {
	console.log('显示价格弹窗')
}

const selectProduct = (product) => {
	console.log('选择商品:', product.name)
}

// 获取主题 store
const themeStore = useThemeStore()

onMounted(() => {
	// 初始化主题
	themeStore.initTheme()
})


</script>

<style scoped>
.order-container {
	min-height: 100vh;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	transition: all 0.3s ease;
}

/* 使用全局主题样式 */
.order-container {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.theme-light .order-container {
	background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
}

/* 所有主题相关元素添加过渡效果 */
.search-header,
.category-sidebar,
.products-area,
.category-header,
.title-text,
.title-subtitle,
.category-name,
.category-count,
.empty-title,
.empty-desc {
	transition: all 0.3s ease;
}

/* 搜索头部 */
.search-header {
	padding: 15px 15px 10px;
	backdrop-filter: blur(20px);
	transition: all 0.3s ease;
}

/* 搜索头部使用全局主题样式 */
.search-header {
	background: rgba(255, 255, 255, 0.1);
	border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.theme-light .search-header {
	background: rgba(0, 0, 0, 0.05);
	border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.search-box {
	display: flex;
	align-items: center;
	background: rgba(255, 255, 255, 0.9);
	border-radius: 20px;
	padding: 10px 16px;
	border: 1px solid rgba(255, 255, 255, 0.3);
	box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.search-icon {
	font-size: 16px;
	margin-right: 8px;
	color: #667eea;
}

.search-input {
	flex: 1;
	font-size: 14px;
	color: #333;
	font-weight: 500;
}

/* 主要内容区域 */
.main-content {
	display: flex;
	height: calc(100vh - 60px);
	width: 100%;
}

/* 左侧分类导航 */
.category-sidebar {
	width: 75px;
	backdrop-filter: blur(15px);
	flex-shrink: 0;
	min-width: 75px;
	padding-bottom: 60px;
	transition: all 0.3s ease;
}

/* 左侧导航使用全局主题样式 */
.category-sidebar {
	background: rgba(255, 255, 255, 0.1);
	border-right: 1px solid rgba(255, 255, 255, 0.1);
	box-shadow: none;
}

.theme-light .category-sidebar {
	background: rgba(255, 255, 255, 0.9);
	border-right: 1px solid rgba(0, 0, 0, 0.1);
	box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
}

.sidebar-scroll {
	height: 100%;

}

.category-item {
	position: relative;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 9px 8px;
	border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	transition: all 0.3s ease;
}

.category-item.active {
	background: rgba(255, 255, 255, 0.2);
	color: #fff;
	border-right: 3px solid #fff;
	box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2);
}

.category-icon {
	width: 40px;
	height: 40px;
	border-radius: 50%;
	display: flex;
	align-items: center;
	justify-content: center;
	margin-bottom: 6px;
	box-shadow: 0 3px 12px rgba(0, 0, 0, 0.1);
}

.category-icon-text {
	font-size: 16px;
}

.category-name {
	font-size: 11px;
	font-weight: 500;
	margin-bottom: 4px;
	text-align: center;
	line-height: 1.2;
	transition: color 0.3s ease;
}

/* 分类名称使用全局主题样式 */
.category-name {
	color: #fff;
}

.theme-light .category-name {
	color: #2c3e50;
}

.category-count {
	font-size: 9px;
	padding: 1px 5px;
	border-radius: 8px;
	backdrop-filter: blur(10px);
	transition: all 0.3s ease;
}

/* 分类数量使用全局主题样式 */
.category-count {
	color: rgba(255, 255, 255, 0.8);
	background: rgba(255, 255, 255, 0.2);
}

.theme-light .category-count {
	color: #6c757d;
	background: rgba(0, 0, 0, 0.1);
}

/* 右侧商品区域 */
.products-area {
	flex: 1;
	backdrop-filter: blur(15px);
	display: flex;
	flex-direction: column;
	min-width: 0;
	overflow: hidden;
	position: relative;
	transition: all 0.3s ease;
}

/* 右侧商品区域使用全局主题样式 */
.products-area {
	background: rgba(255, 255, 255, 0.1);
	border-left: 1px solid rgba(255, 255, 255, 0.1);
	box-shadow: none;
}

.theme-light .products-area {
	background: rgba(255, 255, 255, 0.9);
	border-left: 1px solid rgba(0, 0, 0, 0.1);
	box-shadow: -2px 0 10px rgba(0, 0, 0, 0.05);
}

.category-header {
	display: flex;
	justify-content: space-between;
	align-items: flex-start;
	padding: 18px 15px;
	width: 100%;
	box-sizing: border-box;
	position: sticky;
	top: 0;
	z-index: 10;
	transition: all 0.3s ease;
}

/* 分类标题区域使用全局主题样式 */
.category-header {
	background: rgba(255, 255, 255, 0.05);
	border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	box-shadow: none;
}

.theme-light .category-header {
	background: rgba(255, 255, 255, 0.9);
	border-bottom: 1px solid rgba(0, 0, 0, 0.1);
	box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.category-title {
	flex: 1;
}

.title-text {
	font-size: 18px;
	font-weight: bold;
	display: block;
	margin-bottom: 4px;
	transition: color 0.3s ease;
}

/* 标题使用全局主题样式 */
.title-text {
	color: #fff;
	text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.theme-light .title-text {
	color: #2c3e50;
	text-shadow: none;
}

.title-subtitle {
	font-size: 12px;
	display: block;
	transition: color 0.3s ease;
}

/* 副标题使用全局主题样式 */
.title-subtitle {
	color: rgba(255, 255, 255, 0.7);
}

.theme-light .title-subtitle {
	color: #6c757d;
}

.filter-actions {
	display: flex;
	gap: 15px;
}

.filter-btn {
	display: flex;
	align-items: center;
	background: rgba(255, 255, 255, 0.2);
	border-radius: 20px;
	padding: 8px 16px;
	border: 1px solid rgba(255, 255, 255, 0.3);
	backdrop-filter: blur(10px);
	transition: all 0.3s ease;
}

.filter-btn:active {
	background: rgba(255, 255, 255, 0.3);
	transform: scale(0.95);
}

.filter-text {
	font-size: 12px;
	color: #fff;
	margin-right: 5px;
	font-weight: 500;
}

.filter-arrow {
	font-size: 10px;
	color: rgba(255, 255, 255, 0.8);
}

/* 商品列表 */
.products-scroll {
	flex: 1;
	width: 100%;
	overflow-y: auto;
	-webkit-overflow-scrolling: touch;
	scrollbar-width: none;
	-ms-overflow-style: none;
}

.products-scroll::-webkit-scrollbar {
	display: none;
}

.products-list {
	padding: 16px;
	width: 100%;
	box-sizing: border-box;
	min-height: calc(100vh - 200px);
}

.product-item {
	display: flex;
	padding: 16px;
	margin-bottom: 16px;
	border-radius: 20px;
	background: linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(255, 255, 255, 0.92) 100%);
	box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08), 0 3px 12px rgba(0, 0, 0, 0.06);
	border: 1px solid rgba(255, 255, 255, 0.9);
	backdrop-filter: blur(16px);
	transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	width: 100%;
	box-sizing: border-box;
	position: relative;
	overflow: hidden;
}

.product-item::before {
	content: '';
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	height: 3px;
	background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
	opacity: 0;
	transition: opacity 0.3s ease;
}

.product-item:active::before {
	opacity: 1;
}

.product-item:active {
	transform: translateY(-3px) scale(1.01);
	box-shadow: 0 12px 28px rgba(0, 0, 0, 0.1), 0 5px 16px rgba(0, 0, 0, 0.08);
}

.product-item:last-child {
	margin-bottom: 0;
}

.product-image-wrapper {
	position: relative;
	width: 80px;
	height: 80px;
	margin-right: 16px;
	flex-shrink: 0;
	border-radius: 16px;
	overflow: hidden;
	box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
	background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.product-image {
	width: 100%;
	height: 100%;
	border-radius: 16px;
	transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	object-fit: cover;
}

.product-item:active .product-image {
	transform: scale(1.05);
}

.product-badge {
	position: absolute;
	top: 6px;
	left: 6px;
	background: linear-gradient(135deg, #FF6B6B, #FF8E8E);
	color: #fff;
	font-size: 10px;
	padding: 4px 8px;
	border-radius: 12px;
	font-weight: 700;
	box-shadow: 0 3px 12px rgba(255, 107, 107, 0.4);
	backdrop-filter: blur(10px);
	text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
	letter-spacing: 0.5px;
	border: 1px solid rgba(255, 255, 255, 0.3);
}

.product-info {
	flex: 1;
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	min-width: 0;
	padding: 4px 0;
}

.product-name {
	font-size: 15px;
	color: #0f172a;
	font-weight: 700;
	line-height: 1.4;
	margin-bottom: 12px;
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
	overflow: hidden;
	word-break: break-all;
	letter-spacing: 0.2px;
	text-shadow: 0 1px 2px rgba(15, 23, 42, 0.1);
}

.product-price-section {
	display: flex;
	align-items: baseline;
	margin-bottom: 14px;
	gap: 10px;
}

.product-price {
	font-size: 20px;
	color: #FF6B6B;
	font-weight: 800;
	text-shadow: 0 1px 2px rgba(255, 107, 107, 0.2);
	background: linear-gradient(135deg, #FF6B6B, #FF8E8E);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
}

.product-original {
	font-size: 14px;
	color: #94a3b8;
	text-decoration: line-through;
	font-weight: 500;
	opacity: 0.8;
}

.product-tags {
	display: flex;
	gap: 8px;
	flex-wrap: wrap;
}

.tag {
	background: linear-gradient(135deg, rgba(255, 107, 107, 0.1), rgba(255, 107, 107, 0.05));
	color: #FF6B6B;
	font-size: 11px;
	padding: 4px 10px;
	border-radius: 10px;
	border: 1px solid rgba(255, 107, 107, 0.2);
	font-weight: 600;
	box-shadow: 0 2px 6px rgba(255, 107, 107, 0.12);
	transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	backdrop-filter: blur(6px);
}

/* 加载更多 */
.load-more {
	text-align: center;
	padding: 20px;
}

.load-btn {
	background: rgba(255, 255, 255, 0.2);
	border-radius: 20px;
	padding: 12px 24px;
	border: 1px solid rgba(255, 255, 255, 0.3);
	backdrop-filter: blur(10px);
	transition: all 0.3s ease;
}

.load-btn:active {
	background: rgba(255, 255, 255, 0.3);
	transform: scale(0.95);
}

.load-text {
	font-size: 14px;
	color: #fff;
	font-weight: 500;
}

/* 空状态 */
.empty-state {
	text-align: center;
	padding: 60px 20px;
}

.empty-icon {
	font-size: 60px;
	display: block;
	margin-bottom: 20px;
}

.empty-title {
	font-size: 18px;
	font-weight: bold;
	display: block;
	margin-bottom: 10px;
	transition: color 0.3s ease;
}

.empty-desc {
	font-size: 14px;
	transition: color 0.3s ease;
}

/* 空状态文字使用全局主题样式 */
.empty-title {
	color: #fff;
	text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.empty-desc {
	color: rgba(255, 255, 255, 0.8);
}

.theme-light .empty-title {
	color: #2c3e50;
	text-shadow: none;
}

.theme-light .empty-desc {
	color: #6c757d;
}
</style>
