import request from '@/utils/request/index'

export function getHomeData(data) {
	return request({
		url: '/set/getCommonSetting',
		method: 'post',
		data
	})
}

