<template>
	<view class="page-content">

		<view class="swiper_content">
			<up-swiper :list="bannerList" height="170"> </up-swiper>
		</view>

		<tabsSwiper></tabsSwiper>

		<!-- <view class="scroll-content">
			<view class="top-panel">
				<view class="top-panel-item" v-for="item in topPannel">
					{{item}}
				</view>
			</view>
			<view class="scroll-panel" id="scroll-panel">
				<view class="list-box">
					<view class="left">

						<scroll-view scroll-y="true" :style="{ height: scrollHeight + 'px' }" :scroll-into-view="leftIntoView">
							<view class="item" v-for="(item, index) in leftArray" :key="index" :class="{ active: index == leftIndex }"
								:id="'left-' + index" :data-index="index" @tap="leftTap">
								{{ item }}
							</view>
						</scroll-view>
					</view>
					<view class="main">
						<scroll-view scroll-y="true" :style="{ height: scrollHeight + 'px' }" @scroll="mainScroll"
							:scroll-into-view="scrollInto" scroll-with-animation="true">
							<view class="item main-item" v-for="(item, index) in mainArray" :key="index" :id="'item-' + index">
								<view class="title-tabs">
									<view class="tab-item" v-for="i in item.title">
										{{ i }}
									</view>
								</view>
								<view class="goods" v-for="(item2, index2) in item.list" :key="index2">
									<image src="/static/logo.png" mode=""></image>
									<view>
										<view>第{{ index2 + 1 }}个商品标题</view>
										<view class="describe">第{{ index2 + 1 }}个商品的描述内容</view>
										<view class="money">第{{ index2 + 1 }}个商品的价格</view>
									</view>
								</view>
							</view>
							<view class="fill-last" :style="{ height: fillHeight + 'px' }"></view>
						</scroll-view>
					</view>
				</view>
			</view>

		</view> -->


		<!-- 	<view class="search-input">
			<up-input placeholder="请输入搜索关键字" border="surround" @change="searchMapChange"></up-input>
		</view>
		<view class="page-section page-section-gap">
			<map style="width: 100%; height: 60vh;" :latitude="latitude" :longitude="longitude" :markers="covers"
				@poitap="poitap">
			</map>

		</view>

		<view class="search-list-content">

		</view>
		<view class="" @click="openLocation">
			打开地图
		</view> -->
		
   




	</view>
</template>

<script setup>
	
	import {
		useGlobalOptionStore
	} from '@/store/global'
	import {
		ref,
		nextTick,
		computed
	} from 'vue'
	import {
		onLoad
	} from '@dcloudio/uni-app'

	import tabsSwiper from '../../components/tabs-swiper/tabs-swiper.vue';
	const globalStore = useGlobalOptionStore()
	const list = ref(['未付款', '待评价', '已付款']);
	const bannerList = ref([
		'https://i-blog.csdnimg.cn/blog_migrate/486e1857c3df77284ae6bb3324362b24.png#pic_center',
		'https://i-blog.csdnimg.cn/blog_migrate/486e1857c3df77284ae6bb3324362b24.png#pic_center',
	])
	const QQMapWX = require('../../static/map/qqmap-wx-jssdk1.2/qqmap-wx-jssdk.js');
	const qqmapsdk = ref()
	const latitude = ref() //中心纬度
	const longitude = ref() //中心经度
	const covers = ref([
		// 	{
		// 	id: 1,
		// 	latitude: 39.909,
		// 	longitude: 116.39742,
		// 	width: 20,
		// 	height: 20
		// },
	])



	const tabList = ref([{
			icon: '/static/logo.png',
			text: '首页',
			path: '/pages/home/home',
			selectedIcon: '/static/logo.png',
		},

		{
			icon: '/static/logo.png',
			text: '订单',
			path: '/pages/order/order',
			selectedIcon: '/static/logo.png',
		},
		{
			icon: '/static/logo.png',
			text: '产品',
			path: '/pages/product/product',
			selectedIcon: '/static/logo.png',
		},
		{
			icon: '/static/logo.png',
			text: '服务',
			path: '/pages/service/service',
			selectedIcon: '/static/logo.png',
		},
		{
			icon: '/static/logo.png',
			text: '我的',
			path: '/pages/my/my',
			selectedIcon: '/static/logo.png',
		},
	])

	const topPannel = ref(['综合排序', '销量', '价格'])
	const mainArray = ref([])
	const leftArray = ref([])
	const scrollHeight = ref(400)
	const scrollTopSize = ref(0)
	const fillHeight = ref(0)
	const topArr = ref([])
	const leftIndex = ref(0)
	const scrollInto = ref('')



	onLoad(() => {

		console.log(QQMapWX, 'QQMapWX')
		qqmapsdk.value = new QQMapWX({
			key: 'U55BZ-7IGCD-JPQ4G-H6YIW-HIYB2-OXF43'
		});
		// getAuthorizeInfo()


		// nextTick(() => {
		// 	/* 在非H5平台，nextTick回调后有概率获取到错误的元素高度，则添加200ms的延迟来减少BUG的产生 */
		// 	setTimeout(() => {
		// 		/* 等待滚动区域初始化完成 */
		// 		initScrollView().then(() => {
		// 			/* 获取列表数据，你的代码从此处开始 */
		// 			getListData();
		// 		});
		// 	}, 200);
		// });








	})

	const leftIntoView = computed(() => {
		console.log(leftIndex.value, 999)
		return `left-${leftIndex.value > 3 ? leftIndex.value - 3 : 0}`;
	})



	computed(() => {

	})

	/* 初始化滚动区域 */
	function initScrollView() {
		return new Promise((resolve, reject) => {
			let view = uni.createSelectorQuery().select('#scroll-panel');
			view.boundingClientRect(res => {
				scrollTopSize.value = res.top;
				scrollHeight.value = res.height;
				nextTick(() => {
					resolve();
				});
			}).exec();
		});
	}

	/* 左侧导航点击 */
	function leftTap(e) {
		console.log(e, 'ee')
		let index = e.currentTarget.dataset.index;
		scrollInto.value = `item-${index}`;
	}





	function getListData() {
		// Promise 为 ES6 新增的API ，有疑问的请自行学习该方法的使用。
		new Promise((resolve, reject) => {
			/* 因无真实数据，当前方法模拟数据。正式项目中将此处替换为 数据请求即可 */
			uni.showLoading();
			setTimeout(() => {
				let [left, main] = [
					[],
					[]
				];

				for (let i = 0; i < 25; i++) {
					left.push(`${i + 1}类商品`);

					let list = [];
					let r = Math.floor(Math.random() * 10);
					r = r < 1 ? 3 : r;
					for (let j = 0; j < r; j++) {
						list.push(j);
					}
					let tabs = []
					tabs.push('库思迪', 'KF', '宝马', '奔驰', '大众', '悍马')

					main.push({
						// title: `第${i + 1}类商品标题`,
						title: tabs,
						list
					});
				}

				// 将请求接口返回的数据传递给 Promise 对象的 then 函数。
				resolve({
					left,
					main
				});
			}, 1000);
		}).then(res => {
			console.log('-----------请求接口返回数据示例-------------');
			console.log(res);

			uni.hideLoading();
			leftArray.value = res.left;
			mainArray.value = res.main;

			// DOM 挂载后 再调用 getElementTop 获取高度的方法。
			nextTick(() => {
				getElementTop();
			});
		});
	}

	/* 获取元素顶部信息 */
	function getElementTop() {
		new Promise((resolve, reject) => {
			let view = uni.createSelectorQuery().selectAll('.main-item');
			view.boundingClientRect(data => {
				resolve(data);
			}).exec();
		}).then(res => {
			console.log(res, 'boundingClientRect')
			let arr = res.map(item => {
				return item.top - scrollTopSize.value; /* 减去滚动容器距离顶部的距离 */
			});
			topArr.value = arr;
			console.log(topArr.value, 'topArr')

			/* 获取最后一项的高度，设置填充高度。判断和填充时做了 +-20 的操作，是为了滚动时更好的定位 */
			let last = res[res.length - 1].height;
			if (last - 20 < scrollHeight.value) {
				fillHeight.value = scrollHeight.value - last + 20;
			}
		});
	}

	/* 主区域滚动监听 */
	function mainScroll(e) {
		console.log(topArr.value, 'topArr')
		let top = e.detail.scrollTop;
		let index = 0;
		/* 查找当前滚动距离 */
		for (let i = topArr.value.length - 1; i >= 0; i--) {
			/* 在部分安卓设备上，因手机逻辑分辨率与rpx单位计算不是整数，滚动距离与有误差，增加2px来完善该问题 */
			if (top + 2 >= topArr.value[i]) {
				index = i;
				break;
			}
		}
		leftIndex.value = index < 0 ? 0 : index;
		console.log(leftIndex.value, topArr.value, '	leftIndex.value')
	}




	//获取授权定位信息
	function getAuthorizeInfo() {
		uni.authorize({
			scope: 'scope.userLocation',
			success() { // 允许授权
				getLocation()
			},
			fail() { // 拒绝授权

				console.log("你拒绝了授权，无法获得周边信息")
			}
		})
	}


	function getLocation() {
		uni.getLocation({
			type: 'gcj02',
			isHighAccuracy: true,
			success: function(res) {
				latitude.value = res.latitude
				longitude.value = res.longitude
				covers.value = [{
					id: 1,
					latitude: res.latitude,
					longitude: res.longitude,
					width: 20,
					height: 20
				}]
				console.log('当前位置的经度：' + res.longitude);
				console.log('当前位置的纬度：' + res.latitude);
			}
		})

	}



	function getSearchMapAdd(value) {
		qqmapsdk.value.search({
			keyword: value,
			success: function(res) {
				console.log(res);
			},
			fail: function(res) {
				console.log(res);
			},
			complete: function(res) {
				console.log(res);
			}
		});
	}

	function searchMapChange(e) {
		console.log(e)


		uni.$u.debounce(() => {
			getSearchMapAdd(e)
			console.log('搜索')
		}, 800)
		//防抖

	}

	function poitap(e) {
		console.log(e, 'eee')
		covers.value = [{
			latitude: e.detail.latitude,
			longitude: e.detail.longitude,
			width: 20,
			height: 20,
			callout: {
				content: e.detail.name,
				display: 'ALWAYS',
				padding: 10,
				borderRadius: 10,
				bgColor: '#fff',
				color: '#000',
				fontSize: 12,
				borderWidth: 1,
				borderColor: '#000',
				boxShadow: '0 0 10rpx #000',
				textAlign: 'center',
				lineHeight: 20,
				width: 100,
				height: 30,
				x: 0,
				y: 0,
				zIndex: 999,
			}
		}]
	}
	//打开地图导航
	function openLocation() {
		uni.openLocation({
			latitude: 29.58832234563708,
			longitude: 106.56436432812498,
			scale: 18,
			name: '当前位置',
			success: function(res) {
				console.log('位置名称：' + res.name);
				console.log('位置地址：' + res.address);
				console.log('位置经度：' + res.longitude);
				console.log('位置纬度：' + res.latitude);
			}
		});
	}
</script>

<style lang="scss" scoped>
	.page-content {

		height: 100%;
		margin: 0 20rpx;
		background-color: #F3F4F6;

		.search-input {
			margin-bottom: 20rpx;

			::v-deep .u-input {
				height: 60rpx;
			}
		}

		.swiper_content {
			margin: 0 30rpx;
		}

		.scroll-content {
			.top-panel {
				display: flex;
				padding-left: 200rpx;
				justify-content: space-evenly;
				padding-right: 40rpx;


				.top-panel-item {}

			}

			.scroll-panel {

				.list-box {
					display: flex;
					flex-direction: row;
					flex-wrap: nowrap;
					justify-content: flex-start;
					align-items: flex-start;
					align-content: flex-start;
					font-size: 28rpx;

					.left {
						width: 200rpx;
						background-color: #f6f6f6;
						line-height: 80rpx;
						box-sizing: border-box;
						font-size: 32rpx;

						.item {
							padding-left: 20rpx;
							position: relative;

							&:not(:first-child) {
								margin-top: 1px;

								&::after {
									content: '';
									display: block;
									height: 0;
									border-top: #d6d6d6 solid 1px;
									width: 620upx;
									position: absolute;
									top: -1px;
									right: 0;
									transform: scaleY(0.5);
									/* 1px像素 */
								}
							}

							&.active {
								color: #42b983;
								background-color: #fff;
							}
						}

						.fill-last {
							height: 0;
							width: 100%;
							background: none;
						}
					}

					.main {
						background-color: #fff;
						padding-left: 20rpx;
						width: 0;
						flex-grow: 1;
						box-sizing: border-box;

						.title-tabs {
							width: 100%;
							overflow-x: auto;
							display: flex;

							padding: 20rpx 0;
							font-size: 24rpx;
							font-weight: bold;
							color: #666;
							background-color: #fff;
							position: sticky;
							top: -1px;
							z-index: 19;

							white-space: nowrap;

							.tab-item {
								// width: 240rpx;
								padding: 10rpx 30rpx;
								border-radius: 10rpx;

								margin-right: 30rpx;
								background-color: #fff;
								border: 1px solid #ccc;

							}

						}

						.item {
							padding-bottom: 10rpx;
							border-bottom: #eee solid 1px;
						}

						.goods {
							display: flex;
							flex-direction: row;
							flex-wrap: nowrap;
							justify-content: flex-start;
							align-items: center;
							align-content: center;
							margin-bottom: 10rpx;

							&>image {
								width: 120rpx;
								height: 120rpx;
								margin-right: 16rpx;
								margin-left: 2px;
							}

							.describe {
								font-size: 24rpx;
								color: #999;
							}

							.money {
								font-size: 24rpx;
								color: #efba21;
							}
						}
					}
				}

			}

		}




	}
</style>