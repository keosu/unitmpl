import CryptoJS from 'crypto-js'
import crypto from './crypto'

const VITE_APP_ISENCRYPT = JSON.parse(import.meta.env.VITE_APP_ISENCRYPT)
const VITE_APP_BASE_URL = import.meta.env.VITE_APP_BASE_URL

import {
	getToken,
	removeToken,
	removeUser
} from './auth'

// import {
// 	useUserStore
// } from '@/store/user'

function createCode(strLength) {
	let code = '23456789AaBbCcDdEeFfGgHhJjKkLlMmNnPpOoQqRrSsTtUuVvWwXxYyZz1Ii'
	let tempCode = ''
	// 设置长度，这里看需求，我这里设置了4
	let codeLength = strLength
	// 循环codeLength 我设置的4就是循环4次
	for (let i = 0; i < codeLength; i++) {
		// 设置随机数范围,这设置为0 ~ 36
		let tempSize = Math.floor(getRandomArbitrary(0, code.length - 1))
		tempCode += code.substring(tempSize, tempSize + 1)
	}
	return tempCode
}

function getRandomArbitrary(min, max) {
	// 生成随机数
	return Math.random() * (max - min) + min
}

const request = (config) => {
	let defaultUrl = config.url

	// 拼接完整的接口路径
	config.url = VITE_APP_BASE_URL + config.url

	//判断是都携带参数
	if (!config.data) {
		config.data = {}
	}

	const token = getToken()

	let loadingTime = config.loadingTime || 600 //配置loading关闭时间

	let reqData = config.data
	let nonce = createCode(12)
	let timestamp = Math.round(new Date().getTime() / 1000).toString()

	let str =crypto.sm3Encrypt(JSON.stringify(reqData) + nonce) + timestamp
	
	let signStr = crypto.sm2Encrypt(str)
	let signData = {
		nonce,
		timestamp,
		sign: signStr,
	}
	//包含的路径不做加密处理
	// const urlList = ['/upload/uploadImg']
	const urlList = []

	function executeIfNotContains(urlList, defaultUrl) {
		const isSubstringExists = urlList.some(element => element.includes(defaultUrl));
		
		if (!isSubstringExists && VITE_APP_ISENCRYPT) {
			config.data = crypto.sm4encrypt(reqData)
		}
	}
	executeIfNotContains(urlList, defaultUrl);

	let promise = new Promise(function(resolve, reject) {
		let data = Object.assign({}, config, {
			header: {
				nonce: signData.nonce,
				timestamp: signData.timestamp,
				sign: signData.sign,
				ftoken: token,
			},
		})


		//	//包含的路径接口不做loading处理
		const homePathList = [];
		const requestPath = config.url; //获取接口请求地址
		function executeIfNotContains(array, requestPath) {
			const basePath = requestPath.split('/api/')[1];
			if (!basePath) {
				console.error('No base path found. Make sure the request path contains /api/.');
				return;
			}
			const isSubstringExists = array.some(element => element.includes(basePath));
			if (!isSubstringExists) {
				// 只在路径不包含于列表中时显示加载提示
				uni.showLoading({
					title: 'Loading...',
				});
			} else {
				// 可选：如果路径已经被包含，可以做其他的处理，比如记录日志或直接继续操作
				console.log('Required base path already exists.');
			}
		}
		executeIfNotContains(homePathList, requestPath);




		uni
			.request(data)
			.then((responses) => {
				// 异常
				if (responses[0]) {
					reject({
						message: '网络超时'
					})
				} else if (responses.data.code == 20000) {
					const userStore = useUserStore()
					userStore.logout()
					//登录过期
					uni.showModal({
						title: '登录',
						content: '登录已失效，重新登录',
						showCancel: true,
						success: function(res) {
							if (res.confirm) {
								uni.navigateTo({
									url: '/pages/login/index'
								})
							} else if (res.cancel) {
								console.log('用户点击取消');
							}
						}
					})
				} else {

					if (responses.data.code !== 200) {
						uni.showToast({
							title: responses?.data?.msg || '请联系管理员',
							icon: 'none',
							duration: 2000,
						})
						console.log(responses.data, 'reject响应结果')
						reject(responses.data)
					} else {
						console.log(responses,'responses')
						if (VITE_APP_ISENCRYPT) {
							const exportData = responses.data?.data ?
								crypto.sm4decrypt(responses.data.data) :
								responses.data

							
							resolve(exportData)
						} else {
							
							resolve(responses.data.data)
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
					uni.hideLoading()
				}, loadingTime)
			})
	})
	return promise
}

export default request