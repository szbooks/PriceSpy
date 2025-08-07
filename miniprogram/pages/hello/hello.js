// pages/hello/hello.js
Page({
  data: {
    message: 'Hello PriceSpy!'
  },

  onLoad() {
    // 页面加载完成
  },

  onTap() {
    wx.showToast({
      title: 'Hello!',
      icon: 'success'
    })
  }
}) 