
import CryptoJS from 'crypto-js'
// @ts-ignore
import jsencrypt from './jsencrypt'
// @ts-ignore
import crypto from './crypto'
import { getIsEncrypt, getNoEncryptUrls, getNoDecryptUrls } from "./config";
import { showLoading, hideLoading, showToast, showModal } from '@/utils/utils'
import {
	getToken,
	removeToken,
	removeUser
} from './auth'
import {
	useUserStore
} from '@/store/user'
const VITE_APP_ISENCRYPT = getIsEncrypt()

const VITE_APP_BASE_URL = import.meta.env.VITE_APP_BASE_URL

// 将对象转换为URL编码格式
function objectToUrlEncoded(obj) {
	const params = new URLSearchParams();
	for (const key in obj) {
		if (obj.hasOwnProperty(key)) {
			params.append(key, obj[key]);
		}
	}
	return params.toString();
}

// 将对象转换为JSON字符串
function objectToJson(obj) {
	return JSON.stringify(obj);
}

// 生成随机码
function createCode(strLength) {
	const code = '23456789AaBbCcDdEeFfGgHhJjKkLlMmNnPpOoQqRrSsTtUuVvWwXxYyZz1Ii'
	let tempCode = ''
	const codeLength = strLength
	for (let i = 0; i < codeLength; i++) {
		const tempSize = Math.floor(Math.random() * (code.length - 1))
		tempCode += code.substring(tempSize, tempSize + 1)
	}
	return tempCode
}

// 检查是否包含指定路径
function executeIfNotContains(options) {
	const { array, requestPath, verificationFun, successFun } = options
	const isContains = array.some(item => requestPath.includes(item))
	if (!isContains && verificationFun()) {
		successFun()
		return true
	}
	return false
}

// 公共参数
const commonParams = {

}

// 请求拦截器
function requestInterceptor(config) {
	const token = getToken()

	if (token) {
		config.header = config.header || {}
		config.header.ftoken = token
	}

	// 添加公共参数
	Object.assign(config.data, commonParams)

	// 检测是否为multipart/form-data请求
	const requestPath = config.url || ''

	const isUploadImg = requestPath.includes('common/uploadImg')
	const isMultipartFormData = config.header && config.header['Content-Type'] === 'multipart/form-data'

	// 特殊处理：multipart/form-data请求
	if (isMultipartFormData || isUploadImg) {
		config.header['Content-Type'] = 'multipart/form-data'
		// 对于multipart/form-data，保持原始数据格式，不进行URL编码转换
	}

	// 生成签名参数
	const reqData = config.data
	const nonce = createCode(12)
	const timestamp = Math.round(new Date().getTime() / 1000).toString()
	const str = CryptoJS.SHA1(JSON.stringify(reqData) + nonce) + timestamp
	const signStr = jsencrypt.rsaPublicData(str)
	const signData = {
		nonce,
		timestamp,
		sign: signStr,
	}

	// 添加签名头
	config.header = config.header || {}
	config.header.nonce = signData.nonce
	config.header.timestamp = signData.timestamp
	config.header.sign = signData.sign

	// 数据加密处理
	const urlList = getNoEncryptUrls() // 不加密的接口列表
	const shouldEncrypt = executeIfNotContains({
		array: urlList,
		requestPath: requestPath,
		verificationFun: () => getIsEncrypt(), // 根据配置决定是否加密
		successFun: () => {
			try {
				const encryptedData = crypto.encrypt(reqData)
				config.data = encryptedData
				// 对于multipart/form-data请求，保持原始格式
				if (!isMultipartFormData && !isUploadImg) {
					config.header['Content-Type'] = 'application/json'
				}
			} catch (error) {
				console.error('加密失败:', error)
				// 如果加密失败，使用原始数据
				config.data = reqData
			}
		}
	})

	// 智能处理数据格式
	if (!shouldEncrypt) {
		// 未加密的请求
		if (!config.header['Content-Type'] || (config.header['Content-Type'] !== 'multipart/form-data' && !isMultipartFormData && !isUploadImg)) {
			// 对于multipart/form-data，保持原始格式
			if (config.header['Content-Type'] !== 'multipart/form-data') {
				config.header['Content-Type'] = 'application/x-www-form-urlencoded'
				// 将对象转换为URL编码格式
				config.data = objectToUrlEncoded(reqData)
			}
		}
	} else {
		// 加密的请求，确保使用JSON格式（除了multipart/form-data请求）
		if (!isMultipartFormData && !isUploadImg) {
			config.header['Content-Type'] = 'application/json'
			// 如果加密失败，config.data 仍然是 reqData，需要转换为JSON
			if (config.data === reqData) {
				config.data = objectToJson(reqData)
			}
		}
	}

	return config
}

// 响应拦截器
function responseInterceptor(response, config) {
	// 数据解密处理
	const requestPath = config.url || ''
	const urlList = getNoDecryptUrls() // 不解密的接口列表
	const shouldDecrypt = executeIfNotContains({
		array: urlList,
		requestPath: requestPath,
		verificationFun: () => getIsEncrypt(), // 根据配置决定是否解密
		successFun: () => {
			try {
				if (response.data?.data) {
					// 验证是否需要解密
					if (validateResponseData(response.data)) {
						const decryptedData = crypto.decrypt(response.data.data)
						response.data.data = decryptedData
					}
				}
			} catch (error) {
				console.error('解密失败:', error)
				// 如果解密失败，保持原始数据
			}
		}
	})

	return response
}

// 验证响应数据是否需要解密
function validateResponseData(response) {
	try {
		// 检查响应结构
		if (!response || typeof response !== 'object') {
			return false
		}

		// 检查是否有data字段
		if (!response.hasOwnProperty('data')) {
			return false
		}

		// 检查data字段的类型
		if (typeof response.data === 'string') {
			// 可能是加密的字符串
			return true
		} else if (typeof response.data === 'object') {
			// 可能是已解密的对象
			return false
		}

		return false
	} catch (error) {
		console.error('验证响应数据失败:', error)
		return false
	}
}

// 主请求函数
const request = (config) => {
	let defaultUrl = config.url

	// 拼接完整的接口路径
	config.url = VITE_APP_BASE_URL + config.url

	// 判断是否携带参数
	if (!config.data) {
		config.data = {}
	}

	const token = getToken()

	let loadingTime = config.loadingTime || 600 // 配置loading关闭时间

	// 应用请求拦截器
	config = requestInterceptor(config)

	// 包含的路径接口不做loading处理
	const homePathList = []
	const requestPath = config.url // 获取接口请求地址

	function executeIfNotContains(array, requestPath) {
		const basePath = requestPath.split('/api/')[1]
		if (!basePath) {
			console.error('No base path found. Make sure the request path contains /api/.')
			return
		}
		const isSubstringExists = array.some(element => element.includes(basePath))
		if (!isSubstringExists) {
			// 只在路径不包含于列表中时显示加载提示
			showLoading('Loading...')
		} else {

		}
	}
	executeIfNotContains(homePathList, requestPath)

	let promise = new Promise(function (resolve, reject) {
		uni
			.request(config)
			.then((responses) => {
				// 异常处理
				if (responses[0]) {
					reject({
						message: '网络超时'
					})
				} else if (responses.data.code == 20000) {
					const userStore = useUserStore()
					userStore.logout()
					// 登录过期


					showModal('登录', '登录已失效，重新登录').then(confirmed => {
						if (confirmed) {
							uni.navigateTo({
								url: '/pages/login/index'
							})
						} else {
							console.log('用户点击了取消')
						}
					})


				} else {
					if (responses.data.code !== 200) {
						showToast(responses?.data?.msg || '请联系管理员')

						reject(responses.data)
					} else {
					

						// 应用响应拦截器
						const processedResponse = responseInterceptor(responses, config)
				

						if (VITE_APP_ISENCRYPT) {
							// const exportData = processedResponse.data?.data ?
							// 	crypto.decrypt(processedResponse.data.data) :
							// 	processedResponse.data
							// console.log(exportData, 'exportData')
							// resolve(exportData)
							resolve(processedResponse.data.data)
						} else {
							resolve(processedResponse.data.data)
						}
					}
				}
			})
			.catch((error) => {
				console.log(error, 'errrr')
				reject(error)
			})
			.finally(() => {
				setTimeout(() => {
					hideLoading()
				}, loadingTime)
			})
	})
	return promise
}

// POST请求方法
export function post(url, data = {}, config = {}) {
	return request({
		url: url,
		method: 'POST',
		data: data,
		...config
	})
}

// 上传方法
export function upload(url, data = {}, config = {}) {
	// 设置multipart/form-data，但让请求拦截器处理加密
	const configResult = Object.assign(config, {
		header: { "Content-Type": "multipart/form-data" }
	})

	return request({
		url: url,
		method: 'POST',
		data: data,
		...configResult
	})
}

export default request



