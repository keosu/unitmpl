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
		<view v-if="displayLawyers.length > 0" class="lawyers-list">
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
		<view v-if="displayLawyers.length === 0" class="empty-state">
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

const { t } = useI18n()
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

const searchKeyword = ref('')
const searchHistory = ref(getLocal('searchHistory') || [])
const selectedFilters = ref({})

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

// 模拟律师数据
const mockLawyers = ref([
	{
		id: 1,
		name: '张维权',
		title: '高级合伙人',
		firm: '大成律师事务所',
		avatar: 'https://picsum.photos/120/120?random=1',
		rating: 4.8,
		experience: 15,
		cases: 128,
		hourlyRate: 800,
		specialties: ['刑事辩护', '合同纠纷', '公司法务'],
		description: '擅长复杂商事诉讼和刑事辩护，具有5年专业经验，年均办案200+件。',
		specialtyType: '刑事',
		location: '北京',
		priceRange: 'high'
	},
	{
		id: 2,
		name: '李明浩',
		title: '主任律师',
		firm: '金杜律师事务所',
		avatar: 'https://picsum.photos/120/120?random=2',
		rating: 4.6,
		experience: 12,
		cases: 95,
		hourlyRate: 600,
		specialties: ['婚姻继承', '房产纠纷', '劳动争议'],
		description: '专注婚姻家庭法律服务，在离婚财产分割、子女抚养等领域经验丰富。',
		specialtyType: '民事',
		location: '上海',
		priceRange: 'medium'
	},
	{
		id: 3,
		name: '王佳慧',
		title: '合伙人律师',
		firm: '华诚律师事务所',
		avatar: 'https://picsum.photos/120/120?random=3',
		rating: 4.9,
		experience: 18,
		cases: 156,
		hourlyRate: 1000,
		specialties: ['知识产权', '投融资', '公司并购'],
		description: '专业知识产权律师，曾代理多起重大专利侵权案件，获得客户一致好评。',
		specialtyType: '知识产权',
		location: '深圳',
		priceRange: 'high'
	},
	{
		id: 4,
		name: '陈宇轩',
		title: '主办律师',
		firm: '鹏华律师事务所',
		avatar: 'https://picsum.photos/120/120?random=4',
		rating: 4.5,
		experience: 8,
		cases: 67,
		hourlyRate: 400,
		specialties: ['交通事故', '人身损害', '保险理赔'],
		description: '专业处理交通事故理赔案件，在人身损害赔偿方面有着丰富经验。',
		specialtyType: '交通事故',
		location: '广州',
		priceRange: 'low'
	},
	{
		id: 5,
		name: '刘妍宇',
		title: '高级律师',
		firm: '德恒律师事务所',
		avatar: 'https://picsum.photos/120/120?random=5',
		rating: 4.7,
		experience: 20,
		cases: 189,
		hourlyRate: 900,
		specialties: ['建设工程', '房地产', '政府采购'],
		description: '在建设工程和房地产法律服务领域有着深入的专业知识和丰富实践。',
		specialtyType: '房地产',
		location: '成都',
		priceRange: 'high'
	},
	{
		id: 6,
		name: '许雅文',
		title: '初级律师',
		firm: '星辉律师事务所',
		avatar: 'https://picsum.photos/120/120?random=6',
		rating: 4.3,
		experience: 5,
		cases: 34,
		hourlyRate: 300,
		specialties: ['劳动争议', '合同纠纷', '消费维权'],
		description: '新锐律师，专注于劳动法和消费者权益保护，服务态度认真负责。',
		specialtyType: '劳动法',
		location: '杭州',
		priceRange: 'low'
	}
])

// 筛选选项
const filterOptions = computed(() => [
	{ key: 'specialtyType', value: '刑事', label: '刑事辩护' },
	{ key: 'specialtyType', value: '民事', label: '民事纠纷' },
	{ key: 'specialtyType', value: '知识产权', label: '知识产权' },
	{ key: 'specialtyType', value: '交通事故', label: '交通事故' },
	{ key: 'location', value: '北京', label: '北京' },
	{ key: 'location', value: '上海', label: '上海' },
	{ key: 'location', value: '深圳', label: '深圳' },
	{ key: 'location', value: '广州', label: '广州' },
	{ key: 'priceRange', value: 'low', label: '低价位' },
	{ key: 'priceRange', value: 'medium', label: '中价位' },
	{ key: 'priceRange', value: 'high', label: '高价位' }
])

// 计算属性
const hasActiveFilters = computed(() => 
	Object.keys(selectedFilters.value).length > 0
)

const displayLawyers = computed(() => {
	let filtered = mockLawyers.value
	
	// 按筛选条件过滤
	if (hasActiveFilters.value) {
		filtered = filtered.filter(lawyer => {
			return Object.entries(selectedFilters.value).every(([key, value]) => {
				return lawyer[key] === value
			})
		})
	}
	
	// 按搜索关键词过滤
	if (searchKeyword.value.trim()) {
		const keyword = searchKeyword.value.toLowerCase()
		filtered = filtered.filter(lawyer => 
			lawyer.name.toLowerCase().includes(keyword) ||
			lawyer.firm.toLowerCase().includes(keyword) ||
			lawyer.specialties.some(s => s.toLowerCase().includes(keyword)) ||
			lawyer.description.toLowerCase().includes(keyword)
		)
	}
	
	return filtered
})

// 方法
const toggleFilter = (key, value) => {
	if (selectedFilters.value[key] === value) {
		// 如果已经选中，则取消选中
		delete selectedFilters.value[key]
	} else {
		// 否则设置新值
		selectedFilters.value[key] = value
	}
}

const clearFilters = () => {
	selectedFilters.value = {}
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

const handleSearch = () => {
	if (searchKeyword.value.trim()) {
		addToHistory(searchKeyword.value)
	}
}

const clearSearch = () => {
	searchKeyword.value = ''
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

/* 主题样式 */
.theme-dark .search-container {
	background: #1a1a1a;
}

.theme-dark .search-header {
	background: #2a2a2a;
	border-bottom-color: #333;
}

.theme-dark .search-input {
	background: #333;
}

.theme-dark .search-text {
	color: #fff;
}

.theme-dark .history-title,
.theme-dark .hot-title,
.theme-dark .result-title {
	color: #fff;
}

.theme-dark .result-list {
	background: #2a2a2a;
}

.theme-dark .result-item {
	border-bottom-color: #333;
}

.theme-dark .result-name {
	color: #fff;
}
</style>