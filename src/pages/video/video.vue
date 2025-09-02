<template>
  <view class="video-container">
    <view class="page-title">
      <text>视频播放</text>
    </view>
    <view class="video-wrapper">
      <video 
        id="videoPlayer"
        class="video-player"
        :src="videoSrc"
        controls
        @play="onPlay"
        @pause="onPause"
        @ended="onEnded"
      ></video>
    </view>
    <view class="video-info">
      <text class="info-text">这是一个视频播放页面</text>
    </view>
    <custom-tab-bar ref="tabBar"></custom-tab-bar>
  </view>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import CustomTabBar from '@/components/custom-tab-bar.vue'

const videoSrc = ref('/static/video/test.mp4')

const onPlay = () => {
  console.log('视频开始播放')
}

const onPause = () => {
  console.log('视频暂停')
}

const onEnded = () => {
  console.log('视频播放结束')
}

// 在页面显示时更新tabBar激活状态
const tabBar = ref(null)

onShow(() => {
  nextTick(() => {
    if (tabBar.value) {
      // 获取当前页面路径
      const pages = getCurrentPages()
      const currentPage = pages[pages.length - 1]
      const route = currentPage.route
      tabBar.value.setActiveTab('/' + route)
    }
  })
})
</script>

<style scoped>
.video-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20rpx;
}

.page-title {
  font-size: 36rpx;
  font-weight: bold;
  margin-bottom: 40rpx;
}

.video-wrapper {
  width: 100%;
  max-width: 750rpx;
  margin-bottom: 40rpx;
}

.video-player {
  width: 100%;
  height: 420rpx;
}

.video-info {
  padding: 20rpx;
  background-color: #f0f0f0;
  border-radius: 10rpx;
}

.info-text {
  font-size: 28rpx;
  color: #666;
}
</style>