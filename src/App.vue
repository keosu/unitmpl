<template>
	<view class="app-container" :class="`theme-${themeStore.currentTheme}`">
		<!-- 页面内容 -->
	</view>
</template>

<script setup>
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'
import { onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useThemeStore } from '@/store/theme.js'
import { getLocal } from '@/utils/localStorage.js'
import { getHomeData } from '@/api/home'

const { locale } = useI18n()
const themeStore = useThemeStore()

onLaunch(async () => {
	console.log('onLaunch')
	
	// 初始化语言设置
	try {
		const savedLanguage = getLocal('language')
		if (savedLanguage) {
			locale.value = savedLanguage
		} else {
			// 默认设置为中文
			locale.value = 'zh-cn'
		}
	} catch (error) {
		console.error('语言初始化错误:', error)
		// 默认设置为中文
		locale.value = 'zh-cn'
	}
	
	// const res = await getHomeData()
	// console.log(res,'res')
})

onMounted(async () => {
	// console.log('onMounted')
	// const res = await getHomeData()
	// console.log(res,'res')
})
</script>

<style lang="scss">
@import "uview-plus/index.scss";

/* 全局应用样式 */
.app-container {
	min-height: 100vh;
	width: 100%;
}

/* 浅色主题 */
.theme-light .app-container {
	background: #f8f9fa;
	color: #333;
}

/* 暗色主题 */
.theme-dark .app-container {
	background: #1a1a1a;
	color: #e2e8f0;
}

/* 全局页面样式 */
page {
	background: transparent;
}

.theme-light page {
	background: #f8f9fa;
}

.theme-dark page {
	background: #1a1a1a;
}

/* 全局body样式 */
body {
	background: transparent;
}

.theme-light body {
	background: #f8f9fa;
}

.theme-dark body {
	background: #1a1a1a;
}

/*每个页面公共css */
</style>