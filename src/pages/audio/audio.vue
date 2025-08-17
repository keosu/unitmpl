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
  </view>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { onShow, onHide } from '@dcloudio/uni-app'

// 音频上下文
const innerAudioContext = ref(null)

// 音频状态
const isPlaying = ref(false)
const audioReady = ref(false)
const currentTime = ref('00:00')
const duration = ref('00:00')
const sliderValue = ref(0)

// 音频源
const audioSrc = ref('/static/audio/test.mp3')

// 格式化时间显示
const formatTime = (time) => {
  if (isNaN(time) || time <= 0) return '00:00'
  const minutes = Math.floor(time)
  const seconds = Math.floor((time - minutes) * 60)
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
}

// 创建音频上下文
const initAudioContext = () => {
  innerAudioContext.value = uni.createInnerAudioContext()
  innerAudioContext.value.src = audioSrc.value
  
  // 监听音频进入可以播放状态
  innerAudioContext.value.onCanplay(() => {
    audioReady.value = true
    const dur = innerAudioContext.value.duration || 0
    duration.value = formatTime(dur)
  })
  
  // 监听播放事件
  innerAudioContext.value.onPlay(() => {
    isPlaying.value = true
    console.log('开始播放')
  })
  
  // 监听暂停事件
  innerAudioContext.value.onPause(() => {
    isPlaying.value = false
    console.log('暂停播放')
  })
  
  // 监听停止事件
  innerAudioContext.value.onStop(() => {
    isPlaying.value = false
    currentTime.value = '00:00'
    sliderValue.value = 0
    console.log('停止播放')
  })
  
  // 监听播放进度更新事件
  innerAudioContext.value.onTimeUpdate(() => {
    const current = innerAudioContext.value.currentTime
    const dur = innerAudioContext.value.duration || 0
    // 更新时间显示
    currentTime.value = formatTime(current)
    duration.value = formatTime(dur)
    // 更新进度条
    if (dur > 0) {
      sliderValue.value = (current / dur) * 100
    }
  })
  
  // 监听自然播放结束事件
  innerAudioContext.value.onEnded(() => {
    isPlaying.value = false
    currentTime.value = '00:00'
    sliderValue.value = 0
    console.log('播放结束')
  })
  
  // 监听播放错误事件
  innerAudioContext.value.onError((res) => {
    console.error('音频播放错误:', res.errMsg)
    console.error('错误码:', res.errCode)
  })
}

// 播放/暂停切换
const togglePlay = () => {
  if (!audioReady.value) return
  
  if (isPlaying.value) {
    innerAudioContext.value.pause()
  } else {
    innerAudioContext.value.play()
  }
}

// 停止播放
const stop = () => {
  if (!audioReady.value) return
  
  innerAudioContext.value.stop()
}

// 进度条变化
const onSliderChange = (e) => {
  if (!audioReady.value || !innerAudioContext.value.duration) return
  
  const value = e.detail.value
  const time = (value / 100) * innerAudioContext.value.duration
  innerAudioContext.value.seek(time)
}

// 暂停播放
const pausePlayback = () => {
  console.log('暂停播放函数被调用')
  if (innerAudioContext.value && isPlaying.value) {
    innerAudioContext.value.pause()
  }
}

// 页面显示时的处理函数
onShow(() => {
  console.log('音频页面显示')
})


// 页面隐藏时的处理函数
onHide(() => {
  console.log('音频页面隐藏，暂停播放')
  pausePlayback()
})

// 组件挂载时初始化音频上下文
onMounted(() => {
  console.log('音频页面挂载')
  initAudioContext()
})

// 组件卸载时销毁音频上下文
onUnmounted(() => {
  console.log('音频页面卸载')
  if (innerAudioContext.value) {
    innerAudioContext.value.destroy()
  }
})
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

.custom-audio-player {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.audio-info-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.audio-title {
  font-size: 32rpx;
  font-weight: bold;
}

.audio-time {
  font-size: 24rpx;
  color: #666;
}

.audio-controls {
  display: flex;
  justify-content: center;
  gap: 20rpx;
}

.control-button {
  padding: 10rpx 20rpx;
  background-color: #007aff;
  color: white;
  border: none;
  border-radius: 6rpx;
  font-size: 28rpx;
}

.control-button[disabled] {
  background-color: #ccc;
}

.progress-container {
  width: 100%;
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
  font-size: 24rpx;
  color: #666;
}
</style>