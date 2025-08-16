<template>
  <view class="audio-container">
    <view class="page-title">
      <text>音频播放</text>
    </view>
    <view class="audio-wrapper">
      <view class="audio-player">
        <audio 
          id="audioPlayer"
          class="audio-element"
          :src="audioSrc"
          controls
          @play="onPlay"
          @pause="onPause"
          @ended="onEnded"
        ></audio>
      </view>
    </view>
    <view class="audio-info">
      <text class="info-text">这是一个音频播放页面</text>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

const audioSrc = ref('/static/audio/test.mp3')

const onPlay = () => {
  console.log('音频开始播放')
}

const onPause = () => {
  console.log('音频暂停')
}

const onEnded = () => {
  console.log('音频播放结束')
}
</script>

<style scoped>
.audio-container {
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

.audio-wrapper {
  width: 100%;
  max-width: 750rpx;
  margin-bottom: 40rpx;
}

.audio-player {
  width: 100%;
  padding: 30rpx;
  background-color: #f8f8f8;
  border-radius: 10rpx;
  box-sizing: border-box;
}

.audio-element {
  width: 100%;
}

.audio-info {
  padding: 20rpx;
  background-color: #f0f0f0;
  border-radius: 10rpx;
}

.info-text {
  font-size: 28rpx;
  color: #666;
}
</style>