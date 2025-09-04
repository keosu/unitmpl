<template>
	<view class="search-container" :class="`theme-${themeStore.currentTheme}`">
		<!-- 搜索栏 -->
		<view class="search-header">
			<up-search 
				v-model="searchKeyword"
				:placeholder="t('search.placeholder')"
				@search="handleSearch"
				@clear="clearSearch"
				shape="round"
				bg-color="#f5f5f5"
				margin="20rpx"
				height="80rpx"
			></up-search>
		</view>

		<!-- 筛选器 -->
		<view class="filter-section" v-if="!searchKeyword">
			<view class="filter-title">{{ t('search.filter_title') }}</view>
			<up-row gutter="20">
				<up-col span="3" v-for="filter in filterOptions" :key="filter.key">
					<up-button
						:type="selectedFilters[filter.key] === filter.value ? 'primary' : 'default'"
						:plain="selectedFilters[filter.key] !== filter.value"
						size="small"
						shape="round"
						customStyle="width: 100%; margin-bottom: 20rpx;"
						@click="toggleFilter(filter.key, filter.value)"
					>
						{{ filter.label }}
					</up-button>
				</up-col>
			</up-row>
			<view class="clear-filters" v-if="hasActiveFilters">
				<up-button 
					type="warning"
					text
					size="mini"
					@click="clearFilters"
				>
					{{ t('search.clear_filters') }}
				</up-button>
			</view>
		</view>

		<!-- 搜索历史 -->
		<view v-if="!searchKeyword && searchHistory.length > 0" class="search-history">
			<view class="history-header">
				<text class="history-title">{{ t('search.history') }}</text>
				<up-button 
					type="primary" 
					text
					size="mini"
					@click="clearHistory"
				>
					{{ t('search.clear') }}
				</up-button>
			</view>
			<view class="history-tags">
				<up-tag 
					v-for="(item, index) in searchHistory" 
					:key="index"
					:text="item"
					type="info"
					mode="light"
					shape="circle"
					size="default"
					customStyle="margin: 10rpx;"
					@click="selectHistory(item)"
				></up-tag>
			</view>
		</view>

		<!-- 热门搜索 -->
		<view v-if="!searchKeyword" class="hot-search">
			<view class="hot-header">
				<text class="hot-title">🔥 {{ t('search.hot') }}</text>
			</view>
			<view class="hot-tags">
				<up-tag 
					v-for="(item, index) in hotKeywords" 
					:key="index"
					:text="item"
					type="warning"
					mode="light"
					shape="circle"
					size="default"
					customStyle="margin: 10rpx;"
					@click="selectHot(item)"
				></up-tag>
			</view>
		</view>

		<!-- 律师列表 -->
		<view v-if="isLoading" class="loading-container">
			<up-loading-icon :show="true" mode="circle" size="60"></up-loading-icon>
			<text class="loading-text">正在加载...</text>
		</view>
		
		<view v-else-if="displayLawyers.length > 0" class="lawyers-list">
			<view 
				v-for="lawyer in displayLawyers" 
				:key="lawyer.id"
				class="lawyer-card"
				@click="viewLawyer(lawyer)"
			>
				<view class="lawyer-header">
					<image :src="lawyer.avatar" class="lawyer-avatar" mode="aspectFill" />
					<view class="lawyer-basic">
						<view class="lawyer-name">{{ lawyer.name }}</view>
						<view class="lawyer-title">{{ lawyer.title }}</view>
						<view class="lawyer-firm">{{ lawyer.firm }}</view>
					</view>
					<view class="lawyer-rating">
						<up-rate :value="lawyer.rating" :count="5" :size="24" active-color="#FFD700" inactive-color="#e4e4e4" readonly></up-rate>
						<text class="rating-text">{{ lawyer.rating }}/5</text>
					</view>
				</view>
				
				<view class="lawyer-specialties">
					<text class="specialty-label">专业领域：</text>
					<view class="specialty-tags">
						<up-tag 
							v-for="specialty in lawyer.specialties.slice(0, 3)" 
							:key="specialty"
							:text="specialty"
							type="primary"
							mode="light"
							size="mini"
							customStyle="margin-right: 10rpx;"
						></up-tag>
					</view>
				</view>
				
				<view class="lawyer-stats">
					<view class="stat-item">
						<text class="stat-number">{{ lawyer.experience }}</text>
						<text class="stat-label">年经验</text>
					</view>
					<view class="stat-item">
						<text class="stat-number">{{ lawyer.cases }}</text>
						<text class="stat-label">成功案例</text>
					</view>
					<view class="stat-item">
						<text class="stat-number">￥{{ lawyer.hourlyRate }}</text>
						<text class="stat-label">/小时</text>
					</view>
				</view>
				
				<view class="lawyer-description">
					<text class="description-text">{{ lawyer.description }}</text>
				</view>
				
				<view class="lawyer-actions">
					<up-button 
						type="primary"
						plain
						size="small"
						shape="round"
						customStyle="flex: 1; margin-right: 20rpx;"
						@click.stop="consultLawyer(lawyer)"
					>
						在线咨询
					</up-button>
					<up-button 
						type="primary"
						size="small"
						shape="round"
						customStyle="flex: 1;"
						@click.stop="callLawyer(lawyer)"
					>
						立即联系
					</up-button>
				</view>
			</view>
		</view>

		<!-- 空状态 -->
		<view v-if="!isLoading && displayLawyers.length === 0" class="empty-state">
			<up-empty 
				mode="search"
				:text="searchKeyword ? t('search.no_results') : t('search.no_lawyers')"
				textColor="#999"
				textSize="32"
				iconSize="120"
			></up-empty>
		</view>
	</view>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useThemeStore } from '@/store/theme.js'
import { useUserStore } from '@/store/user.js'
import { getLocal, setLocal } from '@/utils/localStorage.js'
import { lawyerAPI } from '@/api/lawyerService.js'

const { t } = useI18n()
const themeStore = useThemeStore()
const userStore = useUserStore()

// 检查登录状态
onMounted(async () => {
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
	
	// 加载初始数据
	await loadInitialData()
})

/**
 * 加载初始数据
 */
const loadInitialData = async () => {
	isLoading.value = true
	try {
		// 并行加载律师数据和筛选选项
		const [lawyersResult, filtersResult] = await Promise.all([
			lawyerAPI.getAllLawyers(),
			lawyerAPI.getFilterOptions()
		])
		
		if (lawyersResult.success) {
			lawyers.value = lawyersResult.data
		} else {
			uni.showToast({
				title: lawyersResult.message || '获取律师数据失败',
				icon: 'error'
			})
		}
		
		if (filtersResult.success) {
			// 合并所有筛选选项
			filterOptions.value = [
				...filtersResult.data.specialtyTypes,
				...filtersResult.data.locations,
				...filtersResult.data.priceRanges
			]
		} else {
			uni.showToast({
				title: filtersResult.message || '获取筛选选项失败',
				icon: 'error'
			})
		}
	} catch (error) {
		console.error('加载数据失败:', error)
		uni.showToast({
			title: '网络错误，请稍后重试',
			icon: 'error'
		})
	} finally {
		isLoading.value = false
	}
}

const searchKeyword = ref('')
const searchHistory = ref(getLocal('searchHistory') || [])
const selectedFilters = ref({})
const isLoading = ref(false)
const lawyers = ref([])
const filterOptions = ref([])

// 热门搜索关键词
const hotKeywords = ref([
	'刑事辩护',
	'婚姻继承',
	'合同纠纷',
	'交通事故',
	'知识产权',
	'劳动争议',
	'房产纠纷'
])

// 筛选选项（现在从API获取）
// const filterOptions = computed(() => [...]) 已经通过ref定义

// 计算属性
const hasActiveFilters = computed(() => 
	Object.keys(selectedFilters.value).length > 0
)

const displayLawyers = computed(() => {
	// 现在筛选和搜索都在API层面处理，直接返回结果
	return lawyers.value
})

// 方法
const toggleFilter = async (key, value) => {
	if (selectedFilters.value[key] === value) {
		// 如果已经选中，则取消选中
		delete selectedFilters.value[key]
	} else {
		// 否则设置新值
		selectedFilters.value[key] = value
	}
	// 筛选条件改变时重新搜索
	await applyFilters()
}

const clearFilters = async () => {
	selectedFilters.value = {}
	// 清除筛选时重新加载所有数据
	await loadAllLawyers()
}

/**
 * 应用筛选条件
 */
const applyFilters = async () => {
	isLoading.value = true
	try {
		const result = await lawyerAPI.searchLawyers({
			keyword: searchKeyword.value,
			filters: selectedFilters.value,
			page: 1,
			pageSize: 50
		})
		
		if (result.success) {
			lawyers.value = result.data.list
		}
	} catch (error) {
		console.error('应用筛选失败:', error)
	} finally {
		isLoading.value = false
	}
}

const viewLawyer = (lawyer) => {
	console.log('查看律师详情:', lawyer)
	uni.showToast({
		title: `查看 ${lawyer.name} 的详细信息`,
		icon: 'none'
	})
}

const consultLawyer = (lawyer) => {
	console.log('在线咨询:', lawyer)
	uni.showToast({
		title: `开始与 ${lawyer.name} 的在线咨询`,
		icon: 'success'
	})
}

const callLawyer = (lawyer) => {
	console.log('立即联系:', lawyer)
	uni.makePhoneCall({
		phoneNumber: '400-123-4567',
		success: () => {
			console.log('拨打电话成功')
		},
		fail: () => {
			uni.showToast({
				title: '无法拨打电话',
				icon: 'error'
			})
		}
	})
}

const handleSearch = async () => {
	if (searchKeyword.value.trim()) {
		addToHistory(searchKeyword.value)
		await searchLawyers()
	}
}

/**
 * 搜索律师
 */
const searchLawyers = async () => {
	isLoading.value = true
	try {
		const result = await lawyerAPI.searchLawyers({
			keyword: searchKeyword.value,
			filters: selectedFilters.value,
			page: 1,
			pageSize: 50 // 暂时不做分页
		})
		
		if (result.success) {
			lawyers.value = result.data.list
		} else {
			uni.showToast({
				title: result.message || '搜索失败',
				icon: 'error'
			})
		}
	} catch (error) {
		console.error('搜索失败:', error)
		uni.showToast({
			title: '网络错误，请稍后重试',
			icon: 'error'
		})
	} finally {
		isLoading.value = false
	}
}

const clearSearch = async () => {
	searchKeyword.value = ''
	// 清除搜索时重新加载所有律师数据
	await loadAllLawyers()
}

/**
 * 加载所有律师数据
 */
const loadAllLawyers = async () => {
	isLoading.value = true
	try {
		const result = await lawyerAPI.getAllLawyers()
		if (result.success) {
			lawyers.value = result.data
		}
	} catch (error) {
		console.error('加载律师数据失败:', error)
	} finally {
		isLoading.value = false
	}
}

const addToHistory = (keyword) => {
	const history = [...searchHistory.value]
	const index = history.indexOf(keyword)
	if (index > -1) {
		history.splice(index, 1)
	}
	history.unshift(keyword)
	if (history.length > 10) {
		history.pop()
	}
	searchHistory.value = history
	setLocal('searchHistory', history)
}

const clearHistory = () => {
	searchHistory.value = []
	setLocal('searchHistory', [])
}

const selectHistory = (item) => {
	searchKeyword.value = item
	handleSearch()
}

const selectHot = (item) => {
	searchKeyword.value = item
	handleSearch()
}
</script>

<style scoped>
/* 浅色主题（默认） */
.search-container {
	min-height: 100vh;
	background: #f8f9fa;
	padding-bottom: 20px;
}

.search-header {
	padding: 20rpx;
	background: #fff;
	border-bottom: 2rpx solid #eee;
}

.filter-section {
	padding: 30rpx;
	background: #fff;
	margin-bottom: 20rpx;
}

/* 暗色主题 */
.theme-dark .search-container {
	background: #1a1a1a;
}

.theme-dark .search-header {
	background: #2d3748;
	border-bottom-color: #4a5568;
}

.theme-dark .filter-section {
	background: #2d3748;
}

.theme-dark .filter-title,
.theme-dark .history-title,
.theme-dark .hot-title {
	color: #e2e8f0;
}

.theme-dark .lawyer-card {
	background: #2d3748;
	box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.3);
}

.theme-dark .lawyer-name {
	color: #e2e8f0;
}

.theme-dark .lawyer-title,
.theme-dark .lawyer-firm,
.theme-dark .specialty-label,
.theme-dark .description-text {
	color: #a0aec0;
}

.theme-dark .lawyer-stats {
	background: #4a5568;
}

.theme-dark .stat-label {
	color: #a0aec0;
}

.theme-dark .empty-text {
	color: #a0aec0;
}

.filter-title {
	font-size: 32rpx;
	font-weight: bold;
	color: #333;
	margin-bottom: 30rpx;
}

.clear-filters {
	text-align: center;
	margin-top: 30rpx;
}

.lawyers-list {
	padding: 0 30rpx;
}

.loading-container {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 120rpx 20rpx;
}

.loading-text {
	font-size: 28rpx;
	color: #999;
	margin-top: 30rpx;
}

.lawyer-card {
	background: #fff;
	border-radius: 20rpx;
	margin-bottom: 30rpx;
	padding: 30rpx;
	box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
}

.lawyer-header {
	display: flex;
	align-items: flex-start;
	margin-bottom: 30rpx;
}

.lawyer-avatar {
	width: 120rpx;
	height: 120rpx;
	border-radius: 60rpx;
	margin-right: 30rpx;
}

.lawyer-basic {
	flex: 1;
}

.lawyer-name {
	font-size: 36rpx;
	font-weight: bold;
	color: #333;
	margin-bottom: 10rpx;
}

.lawyer-title {
	font-size: 28rpx;
	color: #666;
	margin-bottom: 8rpx;
}

.lawyer-firm {
	font-size: 26rpx;
	color: #999;
}

.lawyer-rating {
	display: flex;
	align-items: center;
	flex-direction: column;
}

.rating-text {
	font-size: 24rpx;
	color: #666;
	margin-top: 8rpx;
}

.lawyer-specialties {
	display: flex;
	align-items: center;
	margin-bottom: 30rpx;
}

.specialty-label {
	font-size: 28rpx;
	color: #666;
	margin-right: 20rpx;
}

.specialty-tags {
	display: flex;
	flex-wrap: wrap;
	flex: 1;
}

.lawyer-stats {
	display: flex;
	justify-content: space-around;
	background: #f8f9fa;
	border-radius: 15rpx;
	padding: 30rpx;
	margin-bottom: 30rpx;
}

.stat-item {
	text-align: center;
}

.stat-number {
	display: block;
	font-size: 32rpx;
	font-weight: bold;
	color: #007aff;
	margin-bottom: 8rpx;
}

.stat-label {
	font-size: 24rpx;
	color: #666;
}

.lawyer-description {
	margin-bottom: 30rpx;
}

.description-text {
	font-size: 28rpx;
	color: #666;
	line-height: 1.6;
}

.lawyer-actions {
	display: flex;
	gap: 20rpx;
}

.search-input-wrapper {
	position: relative;
}

.search-input {
	display: flex;
	align-items: center;
	background: #f5f5f5;
	border-radius: 25px;
	padding: 12px 20px;
}

.search-icon {
	font-size: 18px;
	margin-right: 10px;
	color: #999;
}

.search-text {
	flex: 1;
	border: none;
	background: transparent;
	font-size: 16px;
}

.clear-icon {
	font-size: 14px;
	color: #999;
	margin-left: 10px;
}

.search-history,
.hot-search {
	padding: 20px;
}

.history-header,
.hot-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 15px;
}

.history-title,
.hot-title {
	font-size: 16px;
	font-weight: bold;
	color: #333;
}

.clear-history {
	font-size: 14px;
	color: #999;
}

.history-tags,
.hot-tags {
	display: flex;
	flex-wrap: wrap;
	gap: 10px;
}

.history-tag,
.hot-tag {
	padding: 8px 16px;
	background: #f0f0f0;
	border-radius: 20px;
	font-size: 14px;
	color: #666;
}

.search-results {
	padding: 20px;
}

.result-header {
	margin-bottom: 15px;
}

.result-title {
	font-size: 16px;
	font-weight: bold;
	color: #333;
}

.result-list {
	background: #fff;
	border-radius: 10px;
	overflow: hidden;
}

.result-item {
	display: flex;
	align-items: center;
	padding: 15px 20px;
	border-bottom: 1px solid #f0f0f0;
}

.result-item:last-child {
	border-bottom: none;
}

.result-content {
	flex: 1;
}

.result-name {
	display: block;
	font-size: 16px;
	color: #333;
	margin-bottom: 5px;
}

.result-desc {
	font-size: 14px;
	color: #999;
}

.result-arrow {
	font-size: 18px;
	color: #ccc;
}

.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 60px 20px;
}

.empty-icon {
	font-size: 48px;
	margin-bottom: 20px;
	opacity: 0.3;
}

.empty-text {
	font-size: 16px;
	color: #999;
}


</style>