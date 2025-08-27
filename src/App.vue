<template>
	<view>
		<!-- 页面内容 -->
	</view>
</template>

<script setup>
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'

import { onMounted } from 'vue'

import { getHomeData } from '@/api/home'



onLaunch(async () => {
	console.log('onLaunch')
	const res = await getHomeData()
	console.log(res,'res')
})


onMounted(async () => {
	// console.log('onMounted')
	// const res = await getHomeData()
	// console.log(res,'res')

})

</script>

<style lang="scss">
@import "uview-plus/index.scss";



/*每个页面公共css */
</style>
