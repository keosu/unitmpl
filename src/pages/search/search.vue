<template>
	<view class="search-container" :class="`theme-${themeStore.currentTheme}`">
		<!-- 搜索栏 -->
		<view class="search-header">
			<view class="search-input-wrapper">
				<view class="search-input">
					<text class="search-icon">🔍</text>
					<input 
						type="text" 
						:placeholder="t('search.placeholder')" 
						class="search-text"
						v-model="searchKeyword"
						@input="onSearchInput"
						@confirm="handleSearch"
					/>
					<text v-if="searchKeyword" class="clear-icon" @click="clearSearch">✕</text>
				</view>
			</view>
		</view>

		<!-- 搜索历史 -->
		<view v-if="!searchKeyword && searchHistory.length > 0" class="search-history">
			<view class="history-header">
				<text class="history-title">{{ t('search.history') }}</text>
				<text class="clear-history" @click="clearHistory">{{ t('search.clear') }}</text>
			</view>
			<view class="history-tags">
				<view 
					v-for="(item, index) in searchHistory" 
					:key="index"
					class="history-tag"
					@click="selectHistory(item)"
				>
					{{ item }}
				</view>
			</view>
		</view>

		<!-- 热门搜索 -->
		<view v-if="!searchKeyword" class="hot-search">
			<view class="hot-header">
				<text class="hot-title">🔥 {{ t('search.hot') }}</text>
			</view>
			<view class="hot-tags">
				<view 
					v-for="(item, index) in hotKeywords" 
					:key="index"
					class="hot-tag"
					@click="selectHot(item)"
				>
					{{ item }}
				</view>
			</view>
		</view>

		<!-- 搜索结果 -->
		<view v-if="searchKeyword && searchResults.length > 0" class="search-results">
			<view class="result-header">
				<text class="result-title">{{ t('search.results') }} ({{ searchResults.length }})</text>
			</view>
			<view class="result-list">
				<view 
					v-for="(item, index) in searchResults" 
					:key="index"
					class="result-item"
					@click="selectResult(item)"
				>
					<view class="result-content">
						<text class="result-name">{{ item.name }}</text>
						<text class="result-desc">{{ item.description }}</text>
					</view>
					<text class="result-arrow">→</text>
				</view>
			</view>
		</view>

		<!-- 空状态 -->
		<view v-if="searchKeyword && searchResults.length === 0" class="empty-state">
			<text class="empty-icon">🔍</text>
			<text class="empty-text">{{ t('search.no_results') }}</text>
		</view>
	</view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
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
const searchResults = ref([])

const hotKeywords = computed(() => [
	t('search.hot_1'),
	t('search.hot_2'),
	t('search.hot_3'),
	t('search.hot_4'),
	t('search.hot_5')
])

// 模拟搜索结果
const mockResults = [
	{ name: 'Search Result 1', description: 'Description for result 1' },
	{ name: 'Search Result 2', description: 'Description for result 2' },
	{ name: 'Search Result 3', description: 'Description for result 3' }
]

const onSearchInput = () => {
	if (searchKeyword.value.trim()) {
		// 模拟搜索
		searchResults.value = mockResults.filter(item => 
			item.name.toLowerCase().includes(searchKeyword.value.toLowerCase())
		)
	} else {
		searchResults.value = []
	}
}

const handleSearch = () => {
	if (searchKeyword.value.trim()) {
		addToHistory(searchKeyword.value)
		onSearchInput()
	}
}

const selectHistory = (keyword) => {
	searchKeyword.value = keyword
	handleSearch()
}

const selectHot = (keyword) => {
	searchKeyword.value = keyword
	handleSearch()
}

const selectResult = (result) => {
	console.log('Selected result:', result)
	// 处理结果选择
}

const clearSearch = () => {
	searchKeyword.value = ''
	searchResults.value = []
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
</script>

<style scoped>
.search-container {
	min-height: 100vh;
	background: #f8f9fa;
	transition: all 0.3s ease;
}

.search-header {
	padding: 20px;
	background: #fff;
	border-bottom: 1px solid #eee;
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