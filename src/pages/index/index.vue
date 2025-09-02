<template>
  <view class="content">
    <image class="logo" src="/static/logo.png"></image>
    <view class="text-area">
      <text class="title">{{ title }}</text>
    </view>
    <custom-tab-bar ref="tabBar"></custom-tab-bar>
  </view>
</template>

<script>
import CustomTabBar from '@/components/custom-tab-bar.vue'

export default {
  components: {
    CustomTabBar
  },
  data() {
    return {
      title: 'Hello',
    }
  },
  onLoad() {},
  methods: {},
  onShow() {
    // 当页面显示时，更新tabBar的激活状态
    this.$nextTick(() => {
      if (this.$refs.tabBar) {
        // 获取当前页面路径
        const pages = getCurrentPages()
        const currentPage = pages[pages.length - 1]
        const route = currentPage.route
        this.$refs.tabBar.setActiveTab('/' + route)
      }
    })
  }
}
</script>

<style>
.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.logo {
  height: 200rpx;
  width: 200rpx;
  margin-top: 200rpx;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 50rpx;
}

.text-area {
  display: flex;
  justify-content: center;
}

.title {
  font-size: 36rpx;
  color: #8f8f94;
}
</style>