<template>
	<view class="index" :class="`theme-${themeStore.currentTheme}`">


		<!-- 二级页面 -->
		<view v-if="tabberPageLoadFlag[0]" :style="{
			display: currentTabbarIndex === 0 ? '' : 'none'
		}">
			<scroll-view class="custom-tabbar-page" scroll-y enable-back-to-top @scrolltolower="tabbarPageScrollLower">
				<searchPage></searchPage>
			</scroll-view>
		</view>
		<view v-if="tabberPageLoadFlag[1]" :style="{
			display: currentTabbarIndex === 1 ? '' : 'none'
		}" class="chat-page-wrapper">
			<chatPage ref="chat"></chatPage>
		</view>
		<view v-if="tabberPageLoadFlag[2]" :style="{
			display: currentTabbarIndex === 2 ? '' : 'none'
		}">
			<scroll-view class="custom-tabbar-page" scroll-y enable-back-to-top @scrolltolower="tabbarPageScrollLower">
				<profilePage ref="profile"></profilePage>
			</scroll-view>
		</view>

		<!-- 底部导航栏 -->
		<up-tabbar 
			:value="currentTabbarIndex" 
			@change="changeTabbar" 
			:fixed="true" 
			:placeholder="true"
			:safeAreaInsetBottom="true"
			:bgColor="themeStore.currentTheme === 'dark' ? '#2d3748' : '#ffffff'"
			:activeColor="themeStore.currentTheme === 'dark' ? '#63b3ed' : '#007aff'"
			:inactiveColor="themeStore.currentTheme === 'dark' ? '#a0aec0' : '#999999'"
			borderTop
			:borderColor="themeStore.currentTheme === 'dark' ? '#4a5568' : '#e4e7ed'"
		>
			<up-tabbar-item 
				:text="t('tabbar.search')" 
				icon="search" 
				@click="click1"
			></up-tabbar-item>
			<up-tabbar-item 
				:text="t('tabbar.chat')" 
				icon="chat" 
				@click="click1"
			></up-tabbar-item>
			<up-tabbar-item 
				:text="t('tabbar.profile')" 
				icon="account" 
				@click="click1"
			></up-tabbar-item>
		</up-tabbar>


	</view>
</template>

<script setup>
import searchPage from '@/pages/search/search.vue'
import chatPage from '@/pages/chat/chat.vue'
import profilePage from '@/pages/profile/profile.vue'
import {
	ref,
	computed
} from 'vue'
import {
	onLoad
} from '@dcloudio/uni-app'
import {
	useGlobalOptionStore
} from '@/store/global'
import {
	useUserStore
} from '@/store/user'
import { useI18n } from 'vue-i18n'
import { useThemeStore } from '@/store/theme.js'

const { t } = useI18n()
const themeStore = useThemeStore()
const globalStore = useGlobalOptionStore()
const userStore = useUserStore()
const currentTabbarIndex = ref(1) // 默认选中聊天页面
const tabberPageLoadFlag = ref([])
// 定义tabbar标题列表
const tabbarTitleList = computed(() => [
	t('tabbar.search'),
	t('tabbar.chat'),
	t('tabbar.profile')
])

onLoad((options) => {
	const index = Number(options.index || 1) // 默认显示聊天页面
	// 根据底部tabbar菜单列表设置对应页面的加载情况
	for (let i = 0; i < 3; i++) {
		tabberPageLoadFlag.value.push(i === index)
	}
	changeTabbar(index)
})


// 导航页面滚动到底部
function tabbarPageScrollLower(e) {
	if (currentTabbarIndex.value === 0) {
		// this.$refs.pageA.getRandomData && this.$refs.pageA.getRandomData()
	}
}

// 修改当前选中的tabbar
function changeTabbar(index) {
	// 检查是否需要登录
	if ((index === 0 || index === 2) && !userStore.isLoggedIn) {
		uni.showToast({
			title: t('common.login_required'),
			icon: 'none'
		})
		
		setTimeout(() => {
			uni.navigateTo({
				url: '/pages/login/login'
			})
		}, 1500)
		return
	}
	
	if (currentTabbarIndex.value === index) return
	_switchTabbarPage(index)
	currentTabbarIndex.value = index

	// //切换标题
	uni.setNavigationBarTitle({
		title: tabbarTitleList.value[index]
	})
}

// 切换导航页面
function _switchTabbarPage(index) {
	wx.vibrateShort();
	const selectPageFlag = tabberPageLoadFlag.value[index]
	if (selectPageFlag === undefined) {
		return
	}
	if (selectPageFlag === false) {
		tabberPageLoadFlag.value[index] = true
	}
}

// tabbar 点击事件
function click1() {
	// 可以在这里添加额外的点击处理逻辑
}
</script>

<style lang="scss" scoped>
/* 浅色主题（默认） */
.index {
	width: 100%;
	height: 100vh;
	position: relative;

	.custom-tabbar-page {
		width: 100%;
		height: calc(100vh - 80px); // 给 tabbar 留出空间
		background: #F3F4F6;
		box-sizing: border-box;
		padding-bottom: 20rpx; // 额外的底部间距
		padding-bottom: calc(20rpx + constant(safe-area-inset-bottom));
		padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
	}

	.chat-page-wrapper {
		width: 100%;
		height: calc(100vh - 80px); // 给 tabbar 留出空间
		position: relative; // 为聊天页面的固定输入框提供定位参考
	}

	.color-select {
		color: #FFFFFF;
		background-color: #05C160;
	}

	.color-select-no {
		color: #24272A;
		background-color: #FFFFFF;
	}

	.icon-select {
		color: #05C160;
	}
}

/* 暗色主题 */
.theme-dark .index {
	.custom-tabbar-page {
		background: #1a1a1a;
	}
	
	.color-select-no {
		color: #e2e8f0;
		background-color: #2d3748;
	}
}

/* 为 tabbar 添加额外的主题样式 */
.theme-dark {
	/* 确保 tabbar 在暗色主题下的样式 */
	:deep(.u-tabbar) {
		background-color: #2d3748 !important;
		border-top: 1px solid #4a5568 !important;
		box-shadow: 0 -1px 3px rgba(0, 0, 0, 0.3) !important;
	}
	
	:deep(.u-tabbar-item__text) {
		color: #a0aec0 !important;
	}
	
	:deep(.u-tabbar-item--active .u-tabbar-item__text) {
		color: #63b3ed !important;
	}
	
	:deep(.u-tabbar-item__icon) {
		color: #a0aec0 !important;
	}
	
	:deep(.u-tabbar-item--active .u-tabbar-item__icon) {
		color: #63b3ed !important;
	}
	
	/* 适配uview-plus的新版本类名 */
	:deep(.up-tabbar) {
		background-color: #2d3748 !important;
		border-top: 1px solid #4a5568 !important;
		box-shadow: 0 -1px 3px rgba(0, 0, 0, 0.3) !important;
	}
	
	:deep(.up-tabbar-item__text) {
		color: #a0aec0 !important;
	}
	
	:deep(.up-tabbar-item--active .up-tabbar-item__text) {
		color: #63b3ed !important;
	}
	
	:deep(.up-tabbar-item__icon) {
		color: #a0aec0 !important;
	}
	
	:deep(.up-tabbar-item--active .up-tabbar-item__icon) {
		color: #63b3ed !important;
	}
}
</style>