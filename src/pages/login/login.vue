<script setup>
import {
	onLoad
} from '@dcloudio/uni-app'
import request from '@/utils/request/index.js'
import {
	getToken
} from '@/utils/request/auth.js'
import {
	useUserStore
} from '@/store/user.js'
import {
	ref
} from 'vue'
const userStore = useUserStore()
onLoad(() => {
	if (getToken()) {
		uni.switchTab({
			url: '/pages/home/home'
		})
	}
})

async function getphonenumber(e) {
	console.log(e, 'eee')
	if (e.detail.code) {
		const res = await userStore.login(e.detail.code)
		console.log(res, '登录信息')
		uni.showToast({
			icon: 'none',
			title: '登录成功'
		})

		uni.hideLoading()
		setTimeout(() => {
			uni.switchTab({
				url: '/pages/home/home'
			})
		}, 500)



	}
}
</script>

<template>
	<view class="page-content">
		<view class="header-info">
			<view class="header-info-logo">
				<!-- <image src="../../static/luhang_logo@2x.jpg" mode=""></image> -->
			</view>
			<view class="header-info-title">
				鹭行咨询在线投票
			</view>
			<view class="header-info-txt">
				您身边的一站式小区管理帮手
			</view>
		</view>
		<view class="bottom-btn">
			<view class="">
				申请获取以下权限
			</view>
			<view class="">
				获取您的公开信息(头像、昵称等)
			</view>
			<view class="">
				<!-- <button open-type="getUserInfo" @getuserinfo="getuserinfo">授权登录</button> -->
				<button open-type="getPhoneNumber" @getphonenumber="getphonenumber">授权登录</button>
			</view>
		</view>
	</view>
</template>



<style lang="scss" scoped>
.page-content {
	background-color: #fff;
	width: 100%;
	height: 100%;
	min-height: 100vh;


	text-align: center;

	.header-info {
		padding-top: 26%;


		.header-info-logo {
			margin-bottom: 10rpx;

			image {
				width: 100px;
				height: 100px;
			}
		}

		.header-info-title {
			padding: 10rpx 0;
			font-size: 34rpx;
			font-weight: 500;
		}

		.header-info-txt {
			padding: 10rpx 0;
			font-size: 14px;
			color: #999;
			letter-spacing: 4rpx;
			font-weight: 500;
		}
	}

	.bottom-btn {
		position: absolute;
		bottom: 10%;
		width: 100%;

		>view:nth-child(1) {
			font-size: 30rpx;
			color: #000;
			margin: 30rpx 0;
		}

		>view:nth-child(2) {
			font-size: 26rpx;
			color: #999;
			margin-bottom: 70rpx;
		}

		>view:nth-child(3) {
			margin-top: 20rpx;


			button {
				width: 80%;
				height: 80rpx;
				line-height: 80rpx;
				background-color: #E69C37;
				color: #fff;
			}
		}
	}
}
</style>