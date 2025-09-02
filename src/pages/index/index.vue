<template>
	<view class="index">


		<!-- 二级页面 -->
		<view v-if="tabberPageLoadFlag[0]" :style="{
			display: currentTabbarIndex === 0 ? '' : 'none'
		}">
			<scroll-view class="custom-tabbar-page" scroll-y enable-back-to-top @scrolltolower="tabbarPageScrollLower">
				<homePage></homePage>
			</scroll-view>
		</view>
		<view v-if="tabberPageLoadFlag[1]" :style="{
			display: currentTabbarIndex === 1 ? '' : 'none'
		}">
			<scroll-view class="custom-tabbar-page" scroll-y enable-back-to-top @scrolltolower="tabbarPageScrollLower">
				<orderPage ref="order"></orderPage>
			</scroll-view>
		</view>
		<view v-if="tabberPageLoadFlag[2]" :style="{
			display: currentTabbarIndex === 2 ? '' : 'none'
		}">
			<scroll-view class="custom-tabbar-page" scroll-y enable-back-to-top @scrolltolower="tabbarPageScrollLower">
				<productPage ref="product"></productPage>
			</scroll-view>
		</view>
		<view v-if="tabberPageLoadFlag[3]" :style="{
			display: currentTabbarIndex === 3 ? '' : 'none'
		}">
			<scroll-view class="custom-tabbar-page" scroll-y enable-back-to-top @scrolltolower="tabbarPageScrollLower">
				<servicePage ref="service"></servicePage>
			</scroll-view>
		</view>
		<view v-if="tabberPageLoadFlag[4]" :style="{
			display: currentTabbarIndex === 4 ? '' : 'none'
		}">
			<scroll-view class="custom-tabbar-page" scroll-y enable-back-to-top @scrolltolower="tabbarPageScrollLower">
				<myPage ref="my"></myPage>
			</scroll-view>
		</view>

		<!-- 底部导航栏 -->
		<view class="tabbar">
			<!-- 图鸟裁剪tabbar-->
			<view class="mask"></view>

			<view class="action" @tap.stop="changeTabbar(0)">
				<view class="bar-icon">
					<image class="" src="https://picsum.photos/55/55?random=1"></image>
				</view>
				<view class="" :class="[currentTabbarIndex === 0 ? 'icon-select' : 'tn-color-gray']">{{ t('tabbar.home')
				}}</view>
			</view>
			<view class="action" @tap.stop="changeTabbar(1)">
				<view class="bar-icon">
					<image class="" src="https://picsum.photos/55/55?random=2"></image>
				</view>
				<view class="" :class="[currentTabbarIndex === 1 ? 'icon-select' : 'tn-color-gray']">{{
					t('tabbar.category') }}</view>
			</view>

			<view class="action bar-center" @tap.stop="changeTabbar(2)">
				<view class="bar-circle nav-index-button">
					<view class="nav-index-button__content">
						<view class="nav-index-button__content--icon tn-flex tn-flex-row-center tn-flex-col-center">
							<view class="bar-circle">
								<image class="" src='https://resource.tuniaokj.com/images/tabbar/planet.png'></image>

							</view>
						</view>
					</view>

					<view class="nav-index-button__meteor">
						<view class="nav-index-button__meteor__wrapper">
							<view v-for="(item, index) in 6" :key="index" class="nav-index-button__meteor__item"
								:style="{ transform: `rotateX(${-60 + (30 * index)}deg) rotateZ(${-60 + (30 * index)}deg)` }">
								<view class="nav-index-button__meteor__item--pic"></view>
							</view>
						</view>
					</view>
				</view>
				<view class="" :class="[currentTabbarIndex === 2 ? 'icon-select' : 'tn-color-gray']">{{
					t('tabbar.publish') }}</view>
			</view>

			<view class="action" @tap.stop="changeTabbar(3)">
				<view class="bar-icon">
					<image class="" src="https://picsum.photos/55/55?random=4"></image>
				</view>
				<view class="" :class="[currentTabbarIndex === 3 ? 'icon-select' : 'tn-color-gray']">{{
					t('tabbar.statistics') }}</view>
			</view>
			<view class="action" @tap.stop="changeTabbar(4)">
				<view class="bar-icon">
					<image class="" src="https://picsum.photos/55/55?random=5"></image>
				</view>
				<view class="" :class="[currentTabbarIndex === 4 ? 'icon-select' : 'tn-color-gray']">{{ t('tabbar.my')
				}}</view>
			</view>
		</view>
	</view>
</template>

<script setup>
import homePage from '@/pages/index/components/home/home.vue'
import orderPage from '@/pages/index/components/order/order.vue'
import productPage from '@/pages/index/components/product/product.vue'
import servicePage from '@/pages/index/components/service/service.vue'
import myPage from '@/pages/index/components/my/my.vue'
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
const globalStore = useGlobalOptionStore()
const currentTabbarIndex = ref(0)
const tabberPageLoadFlag = ref([])
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
// 定义tabbar标题列表
const tabbarTitleList = computed(() => [
	t('tabbar.home'),
	t('tabbar.category'),
	t('tabbar.publish'),
	t('tabbar.statistics'),
	t('tabbar.my')
])

onLoad((options) => {
	const index = Number(options.index || 0)
	// 根据底部tabbar菜单列表设置对应页面的加载情况
	for (let i = 0; i < 5; i++) {
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
</script>

<style lang="scss" scoped>
.index {
	width: 100%;
	height: 100vh;
	position: relative;

	.custom-tabbar-page {
		width: 100%;

		height: 100vh;
		background: #F3F4F6;

		box-sizing: border-box;
		padding-bottom: 0rpx;
		padding-bottom: calc(0rpx + constant(safe-area-inset-bottom));
		padding-bottom: calc(0rpx + env(safe-area-inset-bottom));
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

	/* 底部导航 statr */
	.tabbar {
		width: 100%;
		height: 120rpx;
		height: calc(120rpx + constant(safe-area-inset-bottom));
		height: calc(120rpx + env(safe-area-inset-bottom));
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		background-color: transparent;
		z-index: 998;
		padding-bottom: calc(constant(safe-area-inset-bottom));
		padding-bottom: calc(env(safe-area-inset-bottom));
		display: flex;
		align-items: center;
		justify-content: space-between;
		// box-shadow: 0rpx 0rpx 30rpx 0rpx rgba(0, 0, 0, 0.07);
		/* 图鸟温馨提醒，裁剪式也生效的阴影样式，不用box-shadow*/
		filter: drop-shadow(0rpx 0rpx 20rpx rgba(0, 0, 0, 0.05));

		.mask {
			position: absolute;
			width: 100%;
			height: 100%;
			bottom: 0;
			left: 0;
			background-color: #FFFFFF;
			/* 图鸟温馨提醒，两边低的效果，不要这个效果的话，删掉即可*/
			// -webkit-clip-path: polygon(37% 0%,63% 0%,100% 9%,100% 100%,0% 100%,0% 9%);
			// clip-path: polygon(37% 0%,63% 0%,100% 9%,100% 100%,0% 100%,0% 9%);
			/* 图鸟裁剪中间凹陷*/
			-webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 58.7'%3E%3Cpath d='M142,40c-10.7,11.5-26,18.7-43,18.7s-32.2-7.2-43-18.7c-1.1-1.2-2.2-2.3-3.3-3.5C37.9,20.4,21,2.1,0,0.2V0h200 v0c-21.9,1-39.3,19.9-54.7,36.5C144.2,37.7,143.1,38.9,142,40z'/%3E%3C/svg%3E"), linear-gradient(#000, #000);
			-webkit-mask-size: auto 56rpx, cover;
			-webkit-mask-position: center -1rpx;
			-webkit-mask-repeat: no-repeat;
			-webkit-mask-composite: xor;
			/*只显示不重合的地方， chorem 、safari 支持*/
			z-index: -1;
			transition: 0.5s;
		}

		.action {
			font-size: 22rpx;
			position: relative;
			flex: 1;
			text-align: center;
			padding: 0;
			display: block;
			height: auto;
			line-height: 1;
			margin: 0;
			overflow: initial;

			.bar-icon {
				width: 100rpx;
				position: relative;
				display: block;
				height: auto;
				margin: 10rpx auto 8rpx;
				text-align: center;
				font-size: 46rpx;

				image {
					width: 55rpx;
					height: 55rpx;
					display: inline-block;
				}
			}

			.bar-circle {
				position: relative;
				display: block;
				margin: 0rpx auto 0rpx;
				text-align: center;
				font-size: 52rpx;
				line-height: 90rpx;
				width: 120rpx !important;
				height: 120rpx !important;
				overflow: hidden;

				image {
					width: 120rpx;
					height: 120rpx;
					display: inline-block;
					margin: 0rpx auto 0rpx;
				}
			}
		}

		.bar-center {

			.nav-index-button {
				animation: suspension 3s ease-in-out infinite;
				z-index: 999999;
				margin-top: -60rpx;
				margin-bottom: 6rpx;


				&__content {
					position: absolute;
					width: 120rpx;
					height: 120rpx;
					top: 50%;
					left: 50%;
					transform: translate(-50%, -50%);

					&--icon {
						width: 120rpx;
						height: 120rpx;
						font-size: 62rpx;
						border-radius: 50%;
						margin-bottom: 18rpx;
						position: relative;
						z-index: 1;
						transform: scale(0.76);

						&::after {
							content: " ";
							position: absolute;
							z-index: -1;
							width: 100%;
							height: 100%;
							left: 0;
							bottom: 0;
							border-radius: inherit;
							opacity: 1;
							transform: scale(1, 1);
							background-size: 100% 100%;
							// background-image: url(https://resource.tuniaokj.com/images/cool_bg_image/icon_bg6.png);
						}
					}
				}

				&__meteor {
					position: absolute;
					top: 50%;
					left: 50%;
					width: 120rpx;
					height: 120rpx;
					transform-style: preserve-3d;
					transform: translate(-50%, -50%) rotateY(75deg) rotateZ(10deg);

					&__wrapper {
						width: 120rpx;
						height: 120rpx;
						transform-style: preserve-3d;
						animation: spin 20s linear infinite;
					}

					&__item {
						position: absolute;
						width: 120rpx;
						height: 120rpx;
						border-radius: 1000rpx;
						left: 0;
						top: 0;

						&--pic {
							display: block;
							width: 100%;
							height: 100%;
							background: url(https://resource.tuniaokj.com/images/cool_bg_image/arc3.png) no-repeat center center;
							background-size: 100% 100%;
							animation: arc 4s linear infinite;
						}
					}
				}
			}
		}
	}

	/* 底部导航 end */
}

@keyframes suspension {

	0%,
	100% {
		transform: translateY(-0.45rem);
	}

	50% {
		transform: translateY(-0.60rem);
	}
}

@keyframes spin {
	0% {
		transform: rotateX(0deg);
	}

	100% {
		transform: rotateX(-360deg);
	}
}

@keyframes arc {
	to {
		transform: rotate(360deg);
	}
}
</style>