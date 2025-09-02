<template>
  <view class="audio-container">
    <view class="page-title">
      <text>音频播放</text>
    </view>
    <view class="audio-wrapper">
      <view class="audio-player">
        <!-- 使用uni.createInnerAudioContext API实现音频播放 -->
        <view class="custom-audio-player">
          <view class="audio-info-section">
            <text class="audio-title">测试音频</text>
            <text class="audio-time">{{ currentTime }} / {{ duration }}</text>
          </view>
          <view class="audio-controls">
            <button 
              class="control-button" 
              @click="togglePlay"
              :disabled="!audioReady"
            >
              {{ isPlaying ? '暂停' : '播放' }}
            </button>
            <button 
              class="control-button" 
              @click="stop"
              :disabled="!audioReady"
            >
              停止
            </button>
          </view>
          <view class="progress-container">
            <slider 
              class="progress-slider"
              :value="sliderValue"
              @change="onSliderChange"
              :disabled="!audioReady"
              min="0"
              :max="100"
            />
          </view>
        </view>
      </view>
    </view>
    <view class="audio-info">
      <text class="info-text">使用 uni.createInnerAudioContext() API 实现音频播放</text>
    </view>
    <custom-tab-bar ref="tabBar"></custom-tab-bar>
  </view>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { onShow, onHide } from '@dcloudio/uni-app'
import CustomTabBar from '@/components/custom-tab-bar.vue'

// 音频上下文
let audioContext = null

// 音频状态
const isPlaying = ref(false)
const audioReady = ref(false)
const currentTime = ref('00:00')
const duration = ref('00:00')
const sliderValue = ref(0)

// 页面加载时初始化
onMounted(() => {
  initAudio()
})

// 页面卸载时销毁音频上下文
onUnmounted(() => {
  if (audioContext) {
    audioContext.destroy()
  }
})

// 页面显示时
onShow(() => {
  nextTick(() => {
    // 更新tabBar激活状态
    const pages = getCurrentPages()
    const currentPage = pages[pages.length - 1]
    const route = currentPage.route
    if (tabBar.value) {
      tabBar.value.setActiveTab('/' + route)
    }
    
    console.log('音频页面显示')
  })
})

// 页面隐藏时暂停音频
onHide(() => {
  if (audioContext && isPlaying.value) {
    audioContext.pause()
    isPlaying.value = false
    console.log('音频页面隐藏，暂停播放')
  }
})

// 初始化音频
const initAudio = () => {
  // 创建音频上下文
  audioContext = uni.createInnerAudioContext()
  
  // 设置音频源
  audioContext.src = '/static/audio/test.mp3'
  
  // 监听音频进入可以播放状态
  audioContext.onCanplay(() => {
    console.log('音频准备就绪')
    audioReady.value = true
    
    // 获取音频总时长
    duration.value = formatTime(audioContext.duration)
  })
  
  // 监听音频播放事件
  audioContext.onPlay(() => {
    console.log('音频开始播放')
    isPlaying.value = true
  })
  
  // 监听音频暂停事件
  audioContext.onPause(() => {
    console.log('音频暂停')
    isPlaying.value = false
  })
  
  // 监听音频停止事件
  audioContext.onStop(() => {
    console.log('音频停止')
    isPlaying.value = false
    currentTime.value = '00:00'
    sliderValue.value = 0
  })
  
  // 监听音频播放结束事件
  audioContext.onEnded(() => {
    console.log('音频播放结束')
    isPlaying.value = false
    currentTime.value = '00:00'
    sliderValue.value = 0
  })
  
  // 监听音频播放进度更新事件
  audioContext.onTimeUpdate(() => {
    currentTime.value = formatTime(audioContext.currentTime)
    // 更新进度条
    if (audioContext.duration > 0) {
      sliderValue.value = (audioContext.currentTime / audioContext.duration) * 100
    }
  })
  
  // 监听音频播放错误事件
  audioContext.onError((res) => {
    console.error('音频播放错误:', res.errMsg)
    uni.showToast({
      title: '音频播放错误',
      icon: 'none'
    })
  })
}

// 格式化时间
const formatTime = (time) => {
  if (isNaN(time)) return '00:00'
  
  const minutes = Math.floor(time / 60)
  const seconds = Math.floor(time % 60)
  
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
}

// 切换播放/暂停
const togglePlay = () => {
  if (!audioReady.value) return
  
  if (isPlaying.value) {
    audioContext.pause()
  } else {
    audioContext.play()
  }
}

// 停止播放
const stop = () => {
  if (!audioReady.value) return
  
  audioContext.stop()
}

// 进度条变化
const onSliderChange = (e) => {
  if (!audioReady.value) return
  
  const value = e.detail.value
  const seekTime = (value / 100) * audioContext.duration
  audioContext.seek(seekTime)
}

// tabBar引用
const tabBar = ref(null)
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

.custom-audio-player {
  padding: 30rpx;
  background-color: #f8f8f8;
  border-radius: 10rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.audio-info-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30rpx;
}

.audio-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.audio-time {
  font-size: 28rpx;
  color: #666;
}

.audio-controls {
  display: flex;
  justify-content: center;
  gap: 20rpx;
  margin-bottom: 30rpx;
}

.control-button {
  padding: 15rpx 30rpx;
  font-size: 28rpx;
  background-color: #007AFF;
  color: white;
  border: none;
  border-radius: 10rpx;
}

.control-button[disabled] {
  background-color: #cccccc;
}

.progress-container {
  padding: 0 20rpx;
}

.progress-slider {
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