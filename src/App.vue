<script>
export default {
  onLaunch: function () {
    console.log('App Launch')
    
    // 应用启动时设置主题
    const themeMode = uni.getStorageSync('themeMode') || 'light'
    this.applyTheme(themeMode)
  },
  onShow: function () {
    console.log('App Show')
  },
  onHide: function () {
    console.log('App Hide')
    // 当应用隐藏时，触发音频页面暂停事件
    uni.$emit('audioPageHide')
  },
  // 监听底部标签页切换
  onPageHide: function() {
    console.log('Page Hide')
    // 当页面隐藏时，触发音频页面暂停事件
    uni.$emit('audioPageHide')
  },
  methods: {
    applyTheme(themeMode) {
      // 应用主题
      if (themeMode === 'dark') {
        uni.setNavigationBarColor({
          frontColor: '#ffffff',
          backgroundColor: '#1a1a1a'
        })
      } else {
        uni.setNavigationBarColor({
          frontColor: '#000000',
          backgroundColor: '#ffffff'
        })
      }
    }
  }
}
</script>

<style>
/*每个页面公共css */
page {
  background-color: #f8f8f8;
}

/* 暗黑主题全局样式 */
.dark page {
  background-color: #1a1a1a;
  color: #fff;
}

.dark .uni-navbar__content {
  background-color: #1a1a1a !important;
}
</style>