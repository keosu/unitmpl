<template>
	<view class="search-refactor-container" :class="`theme-${themeStore.currentTheme}`">
		<!-- 顶部标签栏 -->
		<up-tabs :list="tabsList" @click="tabClick" :current="tabCurrent"></up-tabs>

		<!-- 内容滑动区域 -->
		<swiper class="swiper-box" :current="activeIndex" @change="tabChange">
			<!-- 找律师 标签页 -->
			<swiper-item class="swiper-item">
				<scroll-view scroll-y style="height: 100%;">
					<view class="search-container">
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
				</scroll-view>
			</swiper-item>

			<!-- 看案件 标签页 -->
			<swiper-item class="swiper-item">
				<scroll-view scroll-y style="height: 100%;">
					<view class="case-list-container">
						<!-- 加载状态 -->
						<view v-if="isCasesLoading" class="loading-container">
							<up-loading-icon :show="true" mode="circle" size="60"></up-loading-icon>
						</view>
						<!-- 案件卡片列表 -->
						<view v-else-if="caseList.length > 0">
							<view v-for="item in caseList" :key="item.id" class="case-card">
								<view class="case-card-header">
									<text class="case-card-title">{{ item.title }}</text>
									<up-tag :text="item.status" type="primary" size="mini"></up-tag>
								</view>
								<view class="case-card-body">
									<text class="case-card-number">案件编号: {{ item.case_number }}</text>
									<view class="case-card-tags">
										<up-tag :text="item.case_type" type="info" size="mini" plain></up-tag>
										<up-tag :text="`优先级: ${item.priority}`" type="warning" size="mini" plain></up-tag>
									</view>
								</view>
								<view class="case-card-footer">
									<text class="case-card-date">创建于: {{ new Date(item.created_at).toLocaleDateString() }}</text>
								</view>
							</view>
						</view>
						<!-- 空状态 -->
						<view v-else class="empty-state">
							<up-empty mode="data" :text="t('search.no_cases')"></up-empty>
						</view>
					</view>
				</scroll-view>
			</swiper-item>
		</swiper>

		<!-- 自定义发布按钮 -->
		<view class="custom-fab" @click="navigateToPublish">
			<up-icon name="plus" color="#fff" size="28"></up-icon>
		</view>
	</view>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useThemeStore } from '@/store/theme.js'
import { useUserStore } from '@/store/user.js'
import { getLocal, setLocal } from '@/utils/localStorage.js'
// import { lawyerAPI } from '@/api/lawyerService.js'
// import { caseService } from '@/api/caseService.js'

const { t } = useI18n()
const themeStore = useThemeStore()
const userStore = useUserStore()

// --- Mock Data ---
const mockLawyers = ref([
    {
        id: '1',
        name: '张伟律师',
        title: '高级合伙人',
        firm: '德恒律师事务所',
        avatar: '/static/logo.png',
        rating: 4.9,
        specialties: ['公司法', '合同纠纷', '知识产权'],
        experience: 15,
        cases: 180,
        hourlyRate: 1500,
        description: '张伟律师在公司法和商业诉讼领域拥有超过15年的丰富经验，成功代理了多起重大案件。'
    },
    {
        id: '2',
        name: '李静律师',
        title: '资深律师',
        firm: '金杜律师事务所',
        avatar: '/static/logo.png',
        rating: 4.8,
        specialties: ['婚姻家庭', '劳动争议', '侵权责任'],
        experience: 10,
        cases: 250,
        hourlyRate: 1200,
        description: '李静律师专注于家庭法和劳动法，以其亲和力和专业性赢得了客户的广泛赞誉。'
    },
]);

const mockCases = ref([
    {
        id: 'case1',
        title: '关于XX公司的合同违约案',
        status: 'IN_PROGRESS',
        case_number: 'CASE-2025-001',
        case_type: 'civil',
        priority: 'high',
        created_at: new Date().toISOString()
    },
    {
        id: 'case2',
        title: '劳动仲裁申请 - 王先生诉YY科技',
        status: 'SUBMITTED',
        case_number: 'CASE-2025-002',
        case_type: 'labor',
        priority: 'medium',
        created_at: new Date().toISOString()
    },
    {
        id: 'case3',
        title: '外观设计专利侵权案初步审核',
        status: 'UNDER_REVIEW',
        case_number: 'CASE-2025-003',
        case_type: 'intellectual',
        priority: 'medium',
        created_at: new Date().toISOString()
    },
]);

// Tab控制
const tabCurrent = ref(0)
const activeIndex = ref(0)
const tabsList = ref([
	{ name: '找律师' },
	{ name: '看案件' }
])

const tabClick = (item) => {
	activeIndex.value = item.index
}

const tabChange = (e) => {
	tabCurrent.value = e.detail.current
	if (tabCurrent.value === 1 && caseList.value.length === 0) {
		fetchUnfinishedCases()
	}
}

// 案件列表
const caseList = ref([])
const isCasesLoading = ref(false)

const fetchUnfinishedCases = async () => {
	isCasesLoading.value = true
	// 使用Mock数据
	setTimeout(() => {
		caseList.value = mockCases.value;
		isCasesLoading.value = false;
	}, 1000); // 模拟1秒延迟
}

const navigateToPublish = () => {
	uni.navigateTo({ url: '/pages/publish/publish' })
}

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
 * 加载初始数据 (Mock)
 */
const loadInitialData = async () => {
	isLoading.value = true
	// 使用Mock数据
	setTimeout(() => {
		lawyers.value = mockLawyers.value;
		filterOptions.value = [
			{ key: 'specialty', value: '公司法', label: '公司法' },
			{ key: 'specialty', value: '婚姻家庭', label: '婚姻家庭' },
			{ key: 'location', value: '北京', label: '北京' },
			{ key: 'price', value: '1000-2000', label: '1k-2k' },
		];
		isLoading.value = false;
	}, 500); // 模拟0.5秒延迟
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

// 计算属性
const hasActiveFilters = computed(() => 
	Object.keys(selectedFilters.value).length > 0
)

const displayLawyers = computed(() => {
    if (!searchKeyword.value && !hasActiveFilters.value) {
        return lawyers.value;
    }
    let filtered = [...lawyers.value];
    // 关键词搜索
    if (searchKeyword.value) {
        filtered = filtered.filter(l => 
            l.name.includes(searchKeyword.value) || 
            l.description.includes(searchKeyword.value) ||
            l.specialties.some(s => s.includes(searchKeyword.value))
        );
    }
    // 筛选器
    if (hasActiveFilters.value) {
        // Mock筛选逻辑, 实际应在API层面处理
    }
	return filtered
})

// 方法
const toggleFilter = (key, value) => {
	if (selectedFilters.value[key] === value) {
		delete selectedFilters.value[key]
	} else {
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
.search-refactor-container {
	display: flex;
	flex-direction: column;
	height: 100vh;
}
.swiper-box {
	flex: 1;
	overflow: hidden;
}
.swiper-item {
	height: 100%;
}

.case-list-container {
	padding: 20rpx;
}

.case-card {
	background: #fff;
	border-radius: 16rpx;
	padding: 24rpx;
	margin-bottom: 20rpx;
	box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.08);
}

.theme-dark .case-card {
	background: #2d3748;
}

.case-card-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 16rpx;
}

.case-card-title {
	font-size: 32rpx;
	font-weight: bold;
}

.case-card-body {
	margin-bottom: 16rpx;
}

.case-card-number {
	font-size: 24rpx;
	color: #999;
	margin-bottom: 10rpx;
}

.case-card-tags {
	display: flex;
	gap: 10rpx;
}

.case-card-footer {
	font-size: 24rpx;
	color: #999;
}

/* 浅色主题（默认） */
.search-container {
	min-height: 100%;
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


.custom-fab {
	position: fixed;
	right: 40rpx;
	bottom: 120rpx;
	width: 100rpx;
	height: 100rpx;
	border-radius: 50%;
	background-color: #007aff;
	display: flex;
	justify-content: center;
	align-items: center;
	box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.2);
	z-index: 10;
}


</style>