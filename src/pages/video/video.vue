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
  </view>
</template>

<script>
export default {
  data() {
    return {
      videoSrc: '/static/video/test.mp4' // 设置默认视频地址
    }
  },
  methods: {
    onPlay() {
      console.log('视频开始播放')
    },
    onPause() {
      console.log('视频暂停')
    },
    onEnded() {
      console.log('视频播放结束')
    }
  }
}
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