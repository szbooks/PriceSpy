# PriceSpy 图标资源

本文件夹包含了PriceSpy微信小程序中使用的所有图标资源，所有图标都严格按照HTML设计稿制作。

## 图标列表

### 功能图标
- **search.svg** - 搜索框中的放大镜图标 (14x14px)
- **location.svg** - 位置标记图标 (9x12px)
- **action.svg** - 操作按钮图标 (20x20px)
- **heart.svg** - 空心心形图标，表示未收藏状态 (16x16px)
- **heart-filled.svg** - 实心心形图标，表示已收藏状态 (16x16px)
- **check.svg** - 勾选图标，用于复选框选中状态 (12x12px)

### 趋势图标
- **trend-up.svg** - 价格上升趋势箭头 (7.5x10px, 红色)
- **trend-down.svg** - 价格下降趋势箭头 (7.5x10px, 绿色)

### 底部导航图标
- **home.svg** - 首页图标 (22.5x20px, 灰色)
- **home-active.svg** - 首页图标 (22.5x20px, 蓝色，激活状态)
- **follow.svg** - 关注图标 (24x24px, 灰色)
- **follow-active.svg** - 关注图标 (24x24px, 蓝色，激活状态)
- **profile.svg** - 我的图标 (17.5x20px, 灰色)
- **profile-active.svg** - 我的图标 (17.5x20px, 蓝色，激活状态)

### 其他功能图标
- **unfollow.svg** - 取消关注图标 (20.6x20px, 灰色)
- **analysis.svg** - 分析图标 (20x17.5px, 灰色)

## 使用方法

### 在WXML中使用
```xml
<image src="/images/icons/search.svg" mode="aspectFit" />
```

### 在WXSS中使用
```css
.search-icon {
  background-image: url('/images/icons/search.svg');
  background-size: contain;
  background-repeat: no-repeat;
}
```

### 在JavaScript中引用
```javascript
import { ICONS } from '/images/icons/index.js'

// 使用图标路径
const searchIconPath = ICONS.search
```

## 设计规范

- 所有图标都使用SVG格式，确保在不同分辨率下都能清晰显示
- 图标颜色严格按照HTML设计稿的色值设置
- 图标尺寸与设计稿保持一致
- 支持微信小程序的图片组件和CSS背景图片使用

## 维护说明

- 如需添加新图标，请先在HTML设计稿中确认图标样式
- 导出SVG时保持原始尺寸和颜色
- 更新index.js文件中的图标索引
- 在README.md中添加新图标的说明

## 更新日志

- 2024-01-08: 添加底部导航图标（home-active.svg, follow.svg, follow-active.svg, profile-active.svg）
- 2024-01-08: 添加勾选图标（check.svg）
- 2024-01-08: 添加心形图标（heart.svg, heart-filled.svg）
- 2024-01-08: 根据HTML设计稿更新所有图标样式 