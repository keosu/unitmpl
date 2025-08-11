<template>
	<view class="page-content">
		<up-tabs :list="list1" @click="tabClick" :current="tabCurrent"></up-tabs>
		<view class="swiper-box">
			<swiper :current="activeIndex" @change='tabchange' :style="{height:swiperheight}">
				<swiper-item v-for="(item,index) in list1.length" :key="index">
					<view class="swiper-item">{{index}}</view>
				</swiper-item>
			</swiper>
		</view>

	</view>
</template>

<script setup>
	import {
		ref,
		getCurrentInstance
	} from 'vue'
	const tabCurrent = ref(0)
	const activeIndex = ref(0)
	const swiperheight = ref('')
	import {
		onLoad,

	} from '@dcloudio/uni-app';


	const list1 = ref([{
		name: '关注',
	}, {
		name: '推荐',
	}, {
		name: '电影'
	}, {
		name: '科技'
	}, {
		name: '音乐'
	}, {
		name: '美食'
	}, {
		name: '文化'
	}, {
		name: '财经'
	}, {
		name: '手工'
	}])

	const instance = getCurrentInstance(); // 获取组件实例
	onLoad(() => {
		// getSwiperheight()
	})

	function getSwiperheight() {
		uni.getSystemInfo({
			success: (resu) => {
				console.log(resu, '获取高度')
				resu.windowHeight
				swiperheight.value = resu.windowHeight - 50 + 'px'
				console.log(swiperheight.value, 'swiperheight.value')

				// const query = uni.createSelectorQuery().in(instance);
				// query.select(".swiper-box").boundingClientRect((rect) => {
				// 	console.log(rect, 'rect')


				// }).exec();

			},
			fail: (res) => {}
		})

	}

	function tabchange(e) {
		console.log(e)
		tabCurrent.value = e.detail.current
		activeIndex.value = e.detail.current
	}

	function tabClick(e) {
		console.log(e)
		activeIndex.value = e.index
		tabCurrent.value = e.index
	}
</script>

<style scoped lang="scss">
	.page-content {

		height: 100%;

		.swiper-box {

			min-height: 400rpx;

			swiper {
				min-height: 400rpx;

				swiper-item {
					height: 100%;
				}
			}
		}
	}
</style>