# 主题样式系统使用指南

## 概述

我们创建了一个全局主题样式系统，新页面只需要使用预定义的主题类名，就能自动获得浅色和暗色主题的样式支持，无需重复编写主题相关的CSS。

## 使用方法

### 1. 页面容器

```vue
<template>
  <view class="page-container" :class="`theme-${themeStore.currentTheme}`">
    <!-- 页面内容 -->
  </view>
</template>
```

### 2. 常用主题类名

#### 基础组件
- `.theme-card` - 卡片容器
- `.theme-input` - 输入框
- `.theme-btn` - 按钮
- `.theme-header` - 头部区域
- `.theme-search-bar` - 搜索栏

#### 文字样式
- `.theme-text-primary` - 主要文字
- `.theme-text-secondary` - 次要文字
- `.theme-text-muted` - 弱化文字

#### 布局组件
- `.theme-list-item` - 列表项
- `.theme-divider` - 分割线
- `.theme-icon-container` - 图标容器
- `.theme-product-card` - 商品卡片
- `.theme-service-card` - 服务卡片
- `.theme-option` - 选项项
- `.theme-check` - 勾选标记

## 完整示例

```vue
<template>
  <view class="page-container" :class="`theme-${themeStore.currentTheme}`">
    <!-- 头部 -->
    <view class="theme-header">
      <text class="theme-text-primary">页面标题</text>
    </view>
    
    <!-- 搜索 -->
    <view class="theme-search-bar">
      <input type="text" placeholder="搜索..." class="theme-input" />
    </view>
    
    <!-- 卡片 -->
    <view class="theme-card">
      <text class="theme-text-primary">卡片标题</text>
      <text class="theme-text-secondary">卡片描述</text>
    </view>
    
    <!-- 按钮 -->
    <view class="theme-btn">
      <text class="theme-text-primary">点击按钮</text>
    </view>
    
    <!-- 列表 -->
    <view class="theme-list-item">
      <text class="theme-text-primary">列表项</text>
    </view>
  </view>
</template>

<script setup>
import { useThemeStore } from '@/store/theme.js'
const themeStore = useThemeStore()
</script>

<style scoped>
/* 只需要写布局相关的样式，主题样式自动应用 */
.page-container {
  padding: 20px;
}

.theme-header {
  text-align: center;
  margin-bottom: 20px;
}

.theme-card {
  padding: 25px;
  margin-bottom: 20px;
  text-align: center;
}
</style>
```

## 优势

1. **无需重复编写主题样式** - 新页面直接使用预定义类名
2. **自动响应主题切换** - 当用户切换主题时，所有使用主题类的元素自动更新
3. **统一的视觉风格** - 所有页面使用相同的主题变量，保持一致性
4. **易于维护** - 主题样式集中管理，修改一处即可影响全局
5. **支持自动主题** - 支持系统主题自动检测

## 自定义主题

如果需要自定义主题样式，可以在 `src/styles/theme.css` 中添加新的主题类，或者使用CSS变量：

```css
.my-custom-element {
  background: var(--primary-bg);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}
```

## 注意事项

1. 确保页面根容器使用 `page-container` 类
2. 确保绑定主题类名：`:class="`theme-${themeStore.currentTheme}`"`
3. 优先使用预定义的主题类名，避免重复编写主题样式
4. 如果需要特殊样式，可以结合主题类和自定义样式
