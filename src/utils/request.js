/**
 * HTTP请求工具模块
 * 为将来切换到真实API做准备
 */

/**
 * 基础请求配置
 */
const BASE_CONFIG = {
	baseURL: '', // 将来设置为实际的API地址
	timeout: 10000,
	header: {
		'Content-Type': 'application/json'
	}
}

/**
 * 请求拦截器 - 添加通用header和处理请求
 */
const requestInterceptor = (config) => {
	// 添加token等认证信息
	const token = uni.getStorageSync('token')
	if (token) {
		config.header.Authorization = `Bearer ${token}`
	}
	
	// 显示加载提示
	if (config.showLoading !== false) {
		uni.showLoading({
			title: '加载中...',
			mask: true
		})
	}
	
	return config
}

/**
 * 响应拦截器 - 统一处理响应和错误
 */
const responseInterceptor = (response) => {
	// 隐藏加载提示
	uni.hideLoading()
	
	const { statusCode, data } = response
	
	// HTTP状态码检查
	if (statusCode >= 200 && statusCode < 300) {
		return data
	} else {
		// 处理HTTP错误
		const error = new Error(`HTTP Error: ${statusCode}`)
		error.statusCode = statusCode
		error.data = data
		throw error
	}
}

/**
 * 错误处理器
 */
const errorHandler = (error) => {
	uni.hideLoading()
	
	console.error('Request Error:', error)
	
	// 根据错误类型显示不同提示
	let message = '网络错误，请稍后重试'
	
	if (error.statusCode) {
		switch (error.statusCode) {
			case 401:
				message = '请先登录'
				// 可以在这里跳转到登录页面
				break
			case 403:
				message = '权限不足'
				break
			case 404:
				message = '接口不存在'
				break
			case 500:
				message = '服务器错误'
				break
			default:
				message = `请求失败 (${error.statusCode})`
		}
	}
	
	uni.showToast({
		title: message,
		icon: 'none'
	})
	
	throw error
}

/**
 * 通用请求方法
 */
const request = (options) => {
	return new Promise((resolve, reject) => {
		// 应用请求拦截器
		const config = requestInterceptor({
			...BASE_CONFIG,
			...options
		})
		
		uni.request({
			...config,
			success: (response) => {
				try {
					const result = responseInterceptor(response)
					resolve(result)
				} catch (error) {
					errorHandler(error)
					reject(error)
				}
			},
			fail: (error) => {
				errorHandler(error)
				reject(error)
			}
		})
	})
}

/**
 * 便捷的HTTP方法
 */
export const http = {
	/**
	 * GET请求
	 */
	get(url, params = {}, options = {}) {
		return request({
			url,
			method: 'GET',
			data: params,
			...options
		})
	},
	
	/**
	 * POST请求
	 */
	post(url, data = {}, options = {}) {
		return request({
			url,
			method: 'POST',
			data,
			...options
		})
	},
	
	/**
	 * PUT请求
	 */
	put(url, data = {}, options = {}) {
		return request({
			url,
			method: 'PUT',
			data,
			...options
		})
	},
	
	/**
	 * DELETE请求
	 */
	delete(url, params = {}, options = {}) {
		return request({
			url,
			method: 'DELETE',
			data: params,
			...options
		})
	},
	
	/**
	 * 上传文件
	 */
	upload(url, filePath, formData = {}, options = {}) {
		return new Promise((resolve, reject) => {
			const config = requestInterceptor({
				...BASE_CONFIG,
				...options
			})
			
			uni.uploadFile({
				url: config.baseURL + url,
				filePath,
				name: 'file',
				formData,
				header: config.header,
				success: (response) => {
					try {
						const result = responseInterceptor(response)
						resolve(result)
					} catch (error) {
						errorHandler(error)
						reject(error)
					}
				},
				fail: (error) => {
					errorHandler(error)
					reject(error)
				}
			})
		})
	}
}

/**
 * 设置基础URL（用于生产环境配置）
 */
export const setBaseURL = (url) => {
	BASE_CONFIG.baseURL = url
}

/**
 * 设置全局header
 */
export const setGlobalHeader = (key, value) => {
	BASE_CONFIG.header[key] = value
}

export default http