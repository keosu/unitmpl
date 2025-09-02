<template>
  <view class="custom-tab-bar">
    <uv-tabbar
      :value="activeIndex"
      @change="changeTab"
      :fixed="true"
      :placeholder="true"
      :safeAreaInsetBottom="true"
    >
      <uv-tabbar-item
        v-for="(item, index) in tabList"
        :key="index"
        :text="item.text"
      >
        <template #active-icon>
          <uv-icon 
            :name="item.activeIcon" 
            size="24"
            :color="tabBarStyle.selectedColor"
          ></uv-icon>
        </template>
        <template #inactive-icon>
          <uv-icon 
            :name="item.inactiveIcon" 
            size="24"
            :color="tabBarStyle.color"
          ></uv-icon>
        </template>
      </uv-tabbar-item>
    </uv-tabbar>
  </view>
</template>

<script>
export default {
  name: 'CustomTabBar',
  data() {
    return {
      activeIndex: 0,
      tabList: [
        {
          pagePath: '/pages/index/index',
          text: '首页',
          inactiveIcon: 'home',
          activeIcon: 'home-fill'
        },
        {
          pagePath: '/pages/video/video',
          text: '视频',
          inactiveIcon: 'play-left',
          activeIcon: 'play-left-fill'
        },
        {
          pagePath: '/pages/audio/audio',
          text: '音频',
          inactiveIcon: 'music',
          activeIcon: 'music-fill'
        },
        {
          pagePath: '/pages/profile/profile',
          text: '我的',
          inactiveIcon: 'account',
          activeIcon: 'account-fill'
        }
      ],
      tabBarStyle: {
        color: '#7A7E83',
        selectedColor: '#007AFF',
        backgroundColor: '#F8F8F8',
        borderStyle: 'black'
      }
    }
  },
  methods: {
    changeTab(index) {
      this.activeIndex = index
      const pagePath = this.tabList[index].pagePath
      uni.switchTab({
        url: pagePath
      })
    },
    
    // 设置当前激活的tab
    setActiveTab(url) {
      const index = this.tabList.findIndex(item => url.includes(item.pagePath))
      if (index !== -1) {
        this.activeIndex = index
      }
    }
  }
}
</script>

<style scoped>
.custom-tab-bar {
  /* 自定义样式 */
}
</style>