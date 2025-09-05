<template>
  <view class="env-switcher">
    <!-- 环境切换按钮 -->
    <view 
      class="env-toggle-btn" 
      @click="showEnvModal = true"
      v-if="showButton"
    >
      <text class="env-icon">🔧</text>
      <text class="env-text">{{ currentEnvName }}</text>
    </view>
    
    <!-- 环境选择弹窗 -->
    <up-modal 
      v-model="showEnvModal" 
      title="环境切换"
      :show-confirm-button="false"
      :show-cancel-button="false"
      width="600rpx"
    >
      <view class="env-modal-content">
        <view class="env-description">
          <text class="desc-text">选择运行环境（仅开发调试使用）</text>
        </view>
        
        <view class="env-list">
          <view 
            v-for="env in availableEnvs" 
            :key="env.key"
            class="env-item"
            :class="{ active: env.current }"
            @click="switchEnvironment(env.key)"
          >
            <view class="env-item-content">
              <view class="env-name">{{ env.name }}</view>
              <view class="env-status" v-if="env.current">
                <text class="status-text">当前环境</text>
              </view>
            </view>
            <view class="env-indicator" v-if="env.current">
              <text class="indicator-icon">✓</text>
            </view>
          </view>
        </view>
        
        <view class="env-actions">
          <up-button 
            text="关闭" 
            type="info"
            size="normal"
            @click="showEnvModal = false"
          />
        </view>
      </view>
    </up-modal>
    
    <!-- 环境信息显示 -->
    <view class="env-info" v-if="showInfo">
      <view class="info-row">
        <text class="info-label">当前环境：</text>
        <text class="info-value">{{ currentEnvName }}</text>
      </view>
      <view class="info-row">
        <text class="info-label">API地址：</text>
        <text class="info-value">{{ apiBaseURL || 'Mock数据' }}</text>
      </view>
      <view class="info-row">
        <text class="info-label">Mock模式：</text>
        <text class="info-value">{{ enableMock ? '开启' : '关闭' }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { 
  currentEnv, 
  config, 
  switchEnv, 
  getAvailableEnvs 
} from '@/config/api.js'

// Props
const props = defineProps({
  // 是否显示切换按钮
  showButton: {
    type: Boolean,
    default: true
  },
  // 是否显示环境信息
  showInfo: {
    type: Boolean,
    default: false
  }
})

// 响应式数据
const showEnvModal = ref(false)
const availableEnvs = ref([])

// 计算属性
const currentEnvName = computed(() => config.name)
const apiBaseURL = computed(() => config.baseURL)
const enableMock = computed(() => config.enableMock)

// 方法
const loadAvailableEnvs = () => {
  availableEnvs.value = getAvailableEnvs()
}

const switchEnvironment = async (envKey) => {
  try {
    await switchEnv(envKey)
    showEnvModal.value = false
    
    // 刷新环境列表
    setTimeout(() => {
      loadAvailableEnvs()
    }, 100)
  } catch (error) {
    console.error('环境切换失败:', error)
    uni.showToast({
      title: '环境切换失败',
      icon: 'error'
    })
  }
}

// 生命周期
onMounted(() => {
  loadAvailableEnvs()
  
  // 开发环境显示当前环境信息
  if (currentEnv !== 'production') {
    console.log(`[环境信息] 当前环境: ${config.name}`)
    console.log(`[环境信息] API地址: ${config.baseURL || 'Mock数据'}`)
    console.log(`[环境信息] Mock模式: ${config.enableMock ? '开启' : '关闭'}`)
  }
})
</script>

<style lang="scss" scoped>
.env-switcher {
  position: relative;
}

.env-toggle-btn {
  position: fixed;
  top: 200rpx;
  right: 20rpx;
  z-index: 999;
  display: flex;
  align-items: center;
  padding: 16rpx 20rpx;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 50rpx;
  backdrop-filter: blur(10rpx);
  
  .env-icon {
    font-size: 24rpx;
    margin-right: 8rpx;
  }
  
  .env-text {
    font-size: 20rpx;
    color: #ffffff;
    max-width: 120rpx;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

.env-modal-content {
  padding: 40rpx;
}

.env-description {
  margin-bottom: 40rpx;
  text-align: center;
  
  .desc-text {
    font-size: 28rpx;
    color: #666666;
  }
}

.env-list {
  margin-bottom: 40rpx;
}

.env-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 30rpx 20rpx;
  margin-bottom: 20rpx;
  border: 2rpx solid #e0e0e0;
  border-radius: 16rpx;
  background: #ffffff;
  transition: all 0.3s ease;
  
  &.active {
    border-color: #007aff;
    background: rgba(0, 122, 255, 0.05);
  }
  
  &:last-child {
    margin-bottom: 0;
  }
}

.env-item-content {
  flex: 1;
}

.env-name {
  font-size: 32rpx;
  font-weight: 500;
  color: #333333;
  margin-bottom: 8rpx;
}

.env-status {
  .status-text {
    font-size: 24rpx;
    color: #007aff;
  }
}

.env-indicator {
  .indicator-icon {
    font-size: 32rpx;
    color: #007aff;
  }
}

.env-actions {
  display: flex;
  justify-content: center;
}

.env-info {
  position: fixed;
  bottom: 160rpx;
  left: 20rpx;
  right: 20rpx;
  z-index: 998;
  padding: 20rpx;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 16rpx;
  backdrop-filter: blur(10rpx);
}

.info-row {
  display: flex;
  align-items: center;
  margin-bottom: 8rpx;
  
  &:last-child {
    margin-bottom: 0;
  }
}

.info-label {
  font-size: 24rpx;
  color: #cccccc;
  margin-right: 16rpx;
  min-width: 120rpx;
}

.info-value {
  font-size: 24rpx;
  color: #ffffff;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 暗色主题适配 */
.dark {
  .env-item {
    background: #2d3748;
    border-color: #4a5568;
    
    &.active {
      border-color: #63b3ed;
      background: rgba(99, 179, 237, 0.1);
    }
  }
  
  .env-name {
    color: #ffffff;
  }
  
  .env-status .status-text {
    color: #63b3ed;
  }
  
  .env-indicator .indicator-icon {
    color: #63b3ed;
  }
}
</style>