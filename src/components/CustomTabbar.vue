<template>
	<view class="custom-tabbar" :class="`theme-${currentTheme}`">
		<view 
			v-for="(item, index) in items" 
			:key="index"
			class="tabbar-item"
			:class="{ active: value === index }"
			@click="handleClick(index)"
		>
			<view class="item-icon">
				<text class="icon-emoji">{{ item.emoji }}</text>
			</view>
			<text class="item-text">{{ item.text }}</text>
		</view>
	</view>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
	value: {
		type: Number,
		default: 0
	},
	items: {
		type: Array,
		required: true
	},
	currentTheme: {
		type: String,
		default: 'light'
	}
})

const emit = defineEmits(['change'])

const handleClick = (index) => {
	if (index !== props.value) {
		emit('change', index)
	}
}
</script>

<style scoped>
.custom-tabbar {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	height: 120rpx;
	display: flex;
	align-items: center;
	justify-content: space-around;
	background: #ffffff;
	border-top: 2rpx solid #e4e7ed;
	padding-bottom: constant(safe-area-inset-bottom);
	padding-bottom: env(safe-area-inset-bottom);
	z-index: 1000;
	box-shadow: 0 -4rpx 16rpx rgba(0, 0, 0, 0.1);
}

.theme-dark .custom-tabbar {
	background: #2d3748;
	border-top-color: #4a5568;
	box-shadow: 0 -4rpx 16rpx rgba(0, 0, 0, 0.3);
}

.tabbar-item {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	flex: 1;
	padding: 16rpx 8rpx;
	cursor: pointer;
	transition: all 0.3s ease;
	border-radius: 16rpx;
	margin: 0 8rpx;
}

.item-icon {
	margin-bottom: 8rpx;
	transition: transform 0.3s ease;
}

.icon-emoji {
	font-size: 48rpx;
	opacity: 0.6;
	transition: all 0.3s ease;
}

.tabbar-item.active .icon-emoji {
	opacity: 1;
	transform: scale(1.2);
}

.tabbar-item.active .item-icon {
	transform: translateY(-4rpx);
}

.tabbar-item.active {
	background: rgba(0, 122, 255, 0.1);
}

.theme-dark .tabbar-item.active {
	background: rgba(99, 179, 237, 0.15);
}

.item-text {
	font-size: 24rpx;
	color: #999999;
	transition: all 0.3s ease;
	font-weight: 400;
}

.theme-light .tabbar-item.active .item-text {
	color: #007aff;
	font-weight: 600;
}

.theme-dark .tabbar-item .item-text {
	color: #a0aec0;
}

.theme-dark .tabbar-item.active .item-text {
	color: #63b3ed;
	font-weight: 600;
}

/* 激活状态的emoji样式 */
.theme-light .tabbar-item.active .icon-emoji {
	filter: hue-rotate(200deg) brightness(1.2) saturate(1.3);
}

.theme-dark .tabbar-item.active .icon-emoji {
	filter: hue-rotate(180deg) brightness(1.3) saturate(1.2);
}

/* 悬浮效果 */
.tabbar-item:active {
	transform: scale(0.95);
}
</style>