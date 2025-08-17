<script>
export default {
  onLaunch: function () {
    console.log('App Launch')
  },
  onShow: function () {
    console.log('App Show')
  },
  onHide: function () {
    console.log('App Hide')
    // 当应用隐藏时，触发音频页面暂停事件
    uni.$emit('audioPageHide')
  },
  // 监听主题切换
  onThemeChange: function (res) {
    console.log('主题切换为：', res.theme)
    // 可以在这里添加其他需要在主题切换时执行的逻辑
  }
}
</script>

<style>
/*每个页面公共css */
page {
  background-color: #f8f8f8;
}

/* 暗黑主题全局样式 - 使用媒体查询方式 */
@media (prefers-color-scheme: dark) {
  page {
    background-color: #1a1a1a;
    color: #fff;
  }
  
  .uni-navbar__content {
    background-color: #1a1a1a !important;
  }
}
</style>