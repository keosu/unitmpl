import {
	getUser,
	getToken
} from '@/utils/request/auth'

// ===== 系统信息相关 =====

/**
 * 获取状态栏高度
 * @returns {number} 状态栏高度
 * 
 * @example
 * // 获取状态栏高度
 * const statusBarHeight = getStatusBarHeight()
 * console.log('状态栏高度:', statusBarHeight)
 */
export function getStatusBarHeight() {
	return uni.getSystemInfoSync().statusBarHeight
}

/**
 * 获取导航栏高度
 * @returns {number} 导航栏高度
 * 
 * @example
 * // 获取导航栏高度
 * const navBarHeight = getNavBarHeight()
 * console.log('导航栏高度:', navBarHeight)
 */
export function getNavBarHeight() {
	const systemInfo = uni.getSystemInfoSync()
	const menuButtonInfo = uni.getMenuButtonBoundingClientRect()
	return (menuButtonInfo.top - systemInfo.statusBarHeight) * 2 + menuButtonInfo.height
}

/**
 * 获取顶部安全区域高度
 * @returns {number} 顶部安全区域高度
 * 
 * @example
 * // 获取顶部安全区域高度
 * const topHeight = topBarTop()
 * console.log('顶部安全区域高度:', topHeight)
 */
export function topBarTop() {
	let result = 0
	// #ifdef MP-WEIXIN
	result = uni.getMenuButtonBoundingClientRect().top
	// #endif
	// #ifndef MP-WEIXIN
	result = uni.getSystemInfoSync().statusBarHeight
	// #endif
	return result
}

/**
 * 获取系统信息
 * @returns {object} 系统信息对象
 * 
 * @example
 * // 获取系统信息
 * const systemInfo = getSystemInfo()
 * console.log('系统信息:', systemInfo)
 * console.log('平台:', systemInfo.platform)
 * console.log('屏幕宽度:', systemInfo.screenWidth)
 */
export function getSystemInfo() {
	return uni.getSystemInfoSync()
}

// ===== 图片相关 =====

/**
 * 图片预览
 * @param {string|array} urls - 图片链接或链接数组
 * @param {number} current - 当前显示图片的索引
 * @returns {void}
 * 
 * @example
 * // 预览单张图片
 * previewImage('https://example.com/image.jpg')
 * 
 * // 预览多张图片，从第二张开始
 * previewImage(['image1.jpg', 'image2.jpg', 'image3.jpg'], 1)
 * 
 * // 预览逗号分隔的图片字符串
 * previewImage('image1.jpg,image2.jpg,image3.jpg')
 */
export function previewImage(urls, current = 0) {
	if (!urls) return
	
	let imageUrls = []
	if (typeof urls === 'string') {
		imageUrls = urls.split(',')
	} else if (Array.isArray(urls)) {
		imageUrls = urls
	} else {
		console.error('图片预览参数错误')
		return
	}
	
	uni.previewImage({
		urls: imageUrls,
		current: current,
		success: function(res) {
			console.log('图片预览成功', res)
		},
		fail: function(err) {
			console.error('图片预览失败', err)
		}
	})
}

/**
 * 选择图片
 * @param {number} count - 最多可以选择的图片张数，默认9张
 * @param {array} sizeType - 所选的图片的尺寸，['original', 'compressed'] 原图+压缩图
 * @param {array} sourceType - 选择图片的来源，['album', 'camera'] 相册+相机
 * @returns {Promise<array>} 返回选择的图片路径数组
 * 
 * @example
 * // 选择单张图片
 * chooseImage(1).then(paths => {
 *   console.log('选择的图片:', paths[0])
 * }).catch(err => {
 *   console.error('选择图片失败:', err)
 * })
 * 
 * // 选择多张图片，只要原图
 * chooseImage(5, ['original'], ['album']).then(paths => {
 *   console.log('选择的图片:', paths)
 * })
 * 
 * // 使用 async/await
 * async function selectImages() {
 *   try {
 *     const paths = await chooseImage(3)
 *     console.log('选择的图片:', paths)
 *   } catch (err) {
 *     console.error('选择图片失败:', err)
 *   }
 * }
 */
export function chooseImage(count = 9, sizeType = ['original', 'compressed'], sourceType = ['album', 'camera']) {
	return new Promise((resolve, reject) => {
		uni.chooseImage({
			count,
			sizeType,
			sourceType,
			success: (res) => {
				resolve(res.tempFilePaths)
			},
			fail: (err) => {
				reject(err)
			}
		})
	})
}

// ===== 导航相关 =====

/**
 * 页面跳转
 * @param {string} url - 跳转路径
 * @param {object} params - 传递参数
 * @returns {void}
 * 
 * @example
 * // 简单跳转
 * navigateTo('/pages/detail/detail')
 * 
 * // 带参数跳转
 * navigateTo('/pages/detail/detail', {
 *   id: 123,
 *   type: 'product'
 * })
 * 
 * // 带中文参数跳转
 * navigateTo('/pages/search/search', {
 *   keyword: '搜索关键词',
 *   category: '分类'
 * })
 */
export function navigateTo(url, params = {}) {
	if (Object.keys(params).length > 0) {
		const query = Object.keys(params)
			.map(key => `${key}=${encodeURIComponent(params[key])}`)
			.join('&')
		url += (url.includes('?') ? '&' : '?') + query
	}
	
	uni.navigateTo({
		url,
		fail: (err) => {
			console.error('页面跳转失败', err)
		}
	})
}

/**
 * 重定向页面
 * @param {string} url - 跳转路径
 * @param {object} params - 传递参数
 * @returns {void}
 * 
 * @example
 * // 重定向到登录页
 * redirectTo('/pages/login/login')
 * 
 * // 重定向带参数
 * redirectTo('/pages/result/result', {
 *   status: 'success',
 *   message: '操作成功'
 * })
 */
export function redirectTo(url, params = {}) {
	if (Object.keys(params).length > 0) {
		const query = Object.keys(params)
			.map(key => `${key}=${encodeURIComponent(params[key])}`)
			.join('&')
		url += (url.includes('?') ? '&' : '?') + query
	}
	
	uni.redirectTo({
		url,
		fail: (err) => {
			console.error('页面重定向失败', err)
		}
	})
}

/**
 * 切换Tab页面
 * @param {string} url - 跳转路径
 * @returns {void}
 * 
 * @example
 * // 切换到首页
 * switchTab('/pages/home/home')
 * 
 * // 切换到我的页面
 * switchTab('/pages/my/my')
 */
export function switchTab(url) {
	uni.switchTab({
		url,
		fail: (err) => {
			console.error('Tab切换失败', err)
		}
	})
}

// ===== 提示相关 =====

/**
 * 显示Toast提示
 * @param {string} title - 提示内容
 * @param {string} icon - 图标类型 ('success', 'error', 'loading', 'none')
 * @param {number} duration - 显示时长(毫秒)
 * @returns {void}
 * 
 * @example
 * // 显示普通提示
 * showToast('操作成功')
 * 
 * // 显示成功提示
 * showToast('保存成功', 'success')
 * 
 * // 显示加载提示
 * showToast('加载中...', 'loading', 3000)
 */
export function showToast(title, icon = 'none', duration = 2000) {
	uni.showToast({
		title,
		icon,
		duration
	})
}

/**
 * 显示成功提示
 * @param {string} title - 提示内容
 * @returns {void}
 * 
 * @example
 * // 显示成功提示
 * showSuccess('操作成功')
 * showSuccess('保存成功')
 */
export function showSuccess(title) {
	showToast(title, 'success')
}

/**
 * 显示错误提示
 * @param {string} title - 提示内容
 * @returns {void}
 * 
 * @example
 * // 显示错误提示
 * showError('操作失败')
 * showError('网络连接失败')
 */
export function showError(title) {
	showToast(title, 'error')
}

/**
 * 显示加载提示
 * @param {string} title - 提示内容
 * @returns {void}
 * 
 * @example
 * // 显示加载提示
 * showLoading('加载中...')
 * showLoading('正在上传...')
 * 
 * // 配合隐藏使用
 * showLoading()
 * setTimeout(() => {
 *   hideLoading()
 * }, 2000)
 */
export function showLoading(title = '加载中...') {
	uni.showLoading({
		title,
		mask: true
	})
}

/**
 * 隐藏加载提示
 * @returns {void}
 * 
 * @example
 * // 隐藏加载提示
 * hideLoading()
 */
export function hideLoading() {
	uni.hideLoading()
}

/**
 * 显示确认对话框
 * @param {string} title - 标题
 * @param {string} content - 内容
 * @param {boolean} showCancel - 是否显示取消按钮
 * @returns {Promise<boolean>} 返回用户是否确认
 * 
 * @example
 * // 显示确认对话框
 * showModal('提示', '确定要删除吗？').then(confirmed => {
 *   if (confirmed) {
 *     console.log('用户点击了确定')
 *     // 执行删除操作
 *   } else {
 *     console.log('用户点击了取消')
 *   }
 * })
 * 
 * // 使用 async/await
 * async function confirmDelete() {
 *   const confirmed = await showModal('提示', '确定要删除吗？')
 *   if (confirmed) {
 *     // 执行删除操作
 *   }
 * }
 * 
 * // 只显示确定按钮
 * showModal('提示', '操作成功', false).then(() => {
 *   console.log('用户点击了确定')
 * })
 */
export function showModal(title, content, showCancel = true) {
	return new Promise((resolve) => {
		uni.showModal({
			title,
			content,
			showCancel,
			success: (res) => {
				resolve(res.confirm)
			}
		})
	})
}

// ===== 存储相关 =====

/**
 * 设置剪贴板内容
 * @param {string} data - 要复制的内容
 * @returns {Promise<void>} 复制成功或失败的Promise
 * 
 * @example
 * // 复制文本到剪贴板
 * setClipboardData('要复制的文本').then(() => {
 *   console.log('复制成功')
 * }).catch(err => {
 *   console.error('复制失败:', err)
 * })
 * 
 * // 使用 async/await
 * async function copyText() {
 *   try {
 *     await setClipboardData('要复制的文本')
 *     console.log('复制成功')
 *   } catch (err) {
 *     console.error('复制失败:', err)
 *   }
 * }
 */
export function setClipboardData(data) {
	return new Promise((resolve, reject) => {
		uni.setClipboardData({
			data,
			success: () => {
				showSuccess('复制成功')
				resolve()
			},
			fail: (err) => {
				showError('复制失败')
				reject(err)
			}
		})
	})
}

/**
 * 获取剪贴板内容
 * @returns {Promise<string>} 返回剪贴板内容
 * 
 * @example
 * // 获取剪贴板内容
 * getClipboardData().then(data => {
 *   console.log('剪贴板内容:', data)
 * }).catch(err => {
 *   console.error('获取剪贴板失败:', err)
 * })
 * 
 * // 使用 async/await
 * async function getClipboard() {
 *   try {
 *     const data = await getClipboardData()
 *     console.log('剪贴板内容:', data)
 *   } catch (err) {
 *     console.error('获取剪贴板失败:', err)
 *   }
 * }
 */
export function getClipboardData() {
	return new Promise((resolve, reject) => {
		uni.getClipboardData({
			success: (res) => {
				resolve(res.data)
			},
			fail: (err) => {
				reject(err)
			}
		})
	})
}

// ===== 网络相关 =====

/**
 * 获取网络类型
 * @returns {Promise<string>} 返回网络类型 ('wifi', '2g', '3g', '4g', '5g', 'unknown', 'none')
 * 
 * @example
 * // 获取网络类型
 * getNetworkType().then(type => {
 *   console.log('网络类型:', type)
 *   if (type === 'wifi') {
 *     console.log('当前使用WiFi网络')
 *   } else if (type === 'none') {
 *     console.log('无网络连接')
 *   }
 * }).catch(err => {
 *   console.error('获取网络类型失败:', err)
 * })
 * 
 * // 使用 async/await
 * async function checkNetwork() {
 *   try {
 *     const type = await getNetworkType()
 *     console.log('网络类型:', type)
 *   } catch (err) {
 *     console.error('获取网络类型失败:', err)
 *   }
 * }
 */
export function getNetworkType() {
	return new Promise((resolve, reject) => {
		uni.getNetworkType({
			success: (res) => {
				resolve(res.networkType)
			},
			fail: (err) => {
				reject(err)
			}
		})
	})
}

// ===== 设备相关 =====

/**
 * 拨打电话
 * @param {string} phoneNumber - 电话号码
 * @returns {void}
 * 
 * @example
 * // 拨打电话
 * makePhoneCall('10086')
 * makePhoneCall('+86-138-0013-8000')
 * 
 * // 在点击事件中使用
 * function callService() {
 *   makePhoneCall('400-123-4567')
 * }
 */
export function makePhoneCall(phoneNumber) {
	uni.makePhoneCall({
		phoneNumber,
		fail: (err) => {
			console.error('拨打电话失败', err)
		}
	})
}

/**
 * 震动反馈
 * @param {string} type - 震动类型 ('light', 'medium', 'heavy')
 * @returns {void}
 * 
 * @example
 * // 轻微震动
 * vibrateShort('light')
 * 
 * // 中等震动
 * vibrateShort('medium')
 * 
 * // 重震动
 * vibrateShort('heavy')
 * 
 * // 在按钮点击时使用
 * function onButtonClick() {
 *   vibrateShort('light')
 *   // 执行其他操作
 * }
 */
export function vibrateShort(type = 'light') {
	uni.vibrateShort({
		type,
		fail: (err) => {
			console.error('震动失败', err)
		}
	})
}

// ===== 登录相关 =====

/**
 * 检查登录状态
 * @returns {boolean} 是否已登录
 * 
 * @example
 * // 检查登录状态
 * if (isLogin()) {
 *   console.log('用户已登录')
 *   // 执行需要登录的操作
 * } else {
 *   console.log('用户未登录')
 *   // 会自动弹出登录提示
 * }
 * 
 * // 在需要登录的操作前检查
 * function submitOrder() {
 *   if (!isLogin()) {
 *     return // 未登录会自动处理
 *   }
 *   // 执行下单操作
 * }
 */
export function isLogin() {
	if (!getToken()) {
		uni.showModal({
			title: '提示',
			content: '请先登录',
			showCancel: true,
			success: function(res) {
				if (res.confirm) {
					uni.navigateTo({
						url: '/pages/login/index'
					})
				}
			},
			complete: function() {
				uni.hideLoading()
			}
		})
		return false
	}
	return true
}

// ===== 工具方法 =====

/**
 * 防抖函数
 * @param {function} func - 要防抖的函数
 * @param {number} wait - 等待时间(毫秒)
 * @returns {function} 防抖后的函数
 * 
 * @example
 * // 搜索输入防抖
 * const debouncedSearch = debounce((keyword) => {
 *   console.log('搜索关键词:', keyword)
 *   // 执行搜索请求
 * }, 500)
 * 
 * // 在输入事件中使用
 * function onInput(e) {
 *   debouncedSearch(e.target.value)
 * }
 * 
 * // 按钮点击防抖
 * const debouncedSubmit = debounce(() => {
 *   console.log('提交表单')
 *   // 执行提交操作
 * }, 1000)
 */
export function debounce(func, wait = 300) {
	let timeout
	return function executedFunction(...args) {
		const later = () => {
			clearTimeout(timeout)
			func(...args)
		}
		clearTimeout(timeout)
		timeout = setTimeout(later, wait)
	}
}

/**
 * 节流函数
 * @param {function} func - 要节流的函数
 * @param {number} limit - 限制时间(毫秒)
 * @returns {function} 节流后的函数
 * 
 * @example
 * // 滚动事件节流
 * const throttledScroll = throttle(() => {
 *   console.log('滚动事件')
 *   // 执行滚动相关操作
 * }, 200)
 * 
 * // 在滚动事件中使用
 * function onScroll() {
 *   throttledScroll()
 * }
 * 
 * // 按钮点击节流
 * const throttledClick = throttle(() => {
 *   console.log('按钮点击')
 *   // 执行点击操作
 * }, 500)
 */
export function throttle(func, limit = 300) {
	let inThrottle
	return function() {
		const args = arguments
		const context = this
		if (!inThrottle) {
			func.apply(context, args)
			inThrottle = true
			setTimeout(() => inThrottle = false, limit)
		}
	}
}

/**
 * 格式化时间
 * @param {Date|string|number} date - 日期
 * @param {string} format - 格式字符串
 * @returns {string} 格式化后的时间字符串
 * 
 * @example
 * // 格式化当前时间
 * formatDate(new Date()) // '2024-01-15 14:30:25'
 * 
 * // 自定义格式
 * formatDate(new Date(), 'YYYY年MM月DD日') // '2024年01月15日'
 * formatDate(new Date(), 'MM/DD HH:mm') // '01/15 14:30'
 * 
 * // 格式化时间戳
 * formatDate(1705305025000) // '2024-01-15 14:30:25'
 * 
 * // 格式化日期字符串
 * formatDate('2024-01-15T14:30:25.000Z') // '2024-01-15 14:30:25'
 */
export function formatDate(date, format = 'YYYY-MM-DD HH:mm:ss') {
	const d = new Date(date)
	const year = d.getFullYear()
	const month = String(d.getMonth() + 1).padStart(2, '0')
	const day = String(d.getDate()).padStart(2, '0')
	const hours = String(d.getHours()).padStart(2, '0')
	const minutes = String(d.getMinutes()).padStart(2, '0')
	const seconds = String(d.getSeconds()).padStart(2, '0')
	
	return format
		.replace('YYYY', year)
		.replace('MM', month)
		.replace('DD', day)
		.replace('HH', hours)
		.replace('mm', minutes)
		.replace('ss', seconds)
}

/**
 * 生成随机字符串
 * @param {number} length - 字符串长度
 * @returns {string} 随机字符串
 * 
 * @example
 * // 生成8位随机字符串
 * randomString() // 'aB3cD9eF'
 * 
 * // 生成指定长度的随机字符串
 * randomString(16) // 'aB3cD9eFgH2iJ4kL'
 * randomString(4) // 'aB3c'
 * 
 * // 用于生成临时ID
 * const tempId = randomString(12)
 * console.log('临时ID:', tempId)
 */
export function randomString(length = 8) {
	const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
	let result = ''
	for (let i = 0; i < length; i++) {
		result += chars.charAt(Math.floor(Math.random() * chars.length))
	}
	return result
}