/**
 * 律师服务API模块
 * 当前使用模拟数据，将来可以轻松替换为真实API调用
 */

// 模拟律师数据
const mockLawyers = [
	{
		id: 1,
		name: '张维权',
		title: '高级合伙人',
		firm: '大成律师事务所',
		avatar: 'https://picsum.photos/120/120?random=1',
		rating: 4.8,
		experience: 15,
		cases: 128,
		hourlyRate: 800,
		specialties: ['刑事辩护', '合同纠纷', '公司法务'],
		description: '擅长复杂商事诉讼和刑事辩护，具有5年专业经验，年均办案200+件。',
		specialtyType: '刑事',
		location: '北京',
		priceRange: 'high'
	},
	{
		id: 2,
		name: '李明浩',
		title: '主任律师',
		firm: '金杜律师事务所',
		avatar: 'https://picsum.photos/120/120?random=2',
		rating: 4.6,
		experience: 12,
		cases: 95,
		hourlyRate: 600,
		specialties: ['婚姻继承', '房产纠纷', '劳动争议'],
		description: '专注婚姻家庭法律服务，在离婚财产分割、子女抚养等领域经验丰富。',
		specialtyType: '民事',
		location: '上海',
		priceRange: 'medium'
	},
	{
		id: 3,
		name: '王佳慧',
		title: '合伙人律师',
		firm: '华诚律师事务所',
		avatar: 'https://picsum.photos/120/120?random=3',
		rating: 4.9,
		experience: 18,
		cases: 156,
		hourlyRate: 1000,
		specialties: ['知识产权', '投融资', '公司并购'],
		description: '专业知识产权律师，曾代理多起重大专利侵权案件，获得客户一致好评。',
		specialtyType: '知识产权',
		location: '深圳',
		priceRange: 'high'
	},
	{
		id: 4,
		name: '陈宇轩',
		title: '主办律师',
		firm: '鹏华律师事务所',
		avatar: 'https://picsum.photos/120/120?random=4',
		rating: 4.5,
		experience: 8,
		cases: 67,
		hourlyRate: 400,
		specialties: ['交通事故', '人身损害', '保险理赔'],
		description: '专业处理交通事故理赔案件，在人身损害赔偿方面有着丰富经验。',
		specialtyType: '交通事故',
		location: '广州',
		priceRange: 'low'
	},
	{
		id: 5,
		name: '刘妍宇',
		title: '高级律师',
		firm: '德恒律师事务所',
		avatar: 'https://picsum.photos/120/120?random=5',
		rating: 4.7,
		experience: 20,
		cases: 189,
		hourlyRate: 900,
		specialties: ['建设工程', '房地产', '政府采购'],
		description: '在建设工程和房地产法律服务领域有着深入的专业知识和丰富实践。',
		specialtyType: '房地产',
		location: '成都',
		priceRange: 'high'
	},
	{
		id: 6,
		name: '许雅文',
		title: '初级律师',
		firm: '星辉律师事务所',
		avatar: 'https://picsum.photos/120/120?random=6',
		rating: 4.3,
		experience: 5,
		cases: 34,
		hourlyRate: 300,
		specialties: ['劳动争议', '合同纠纷', '消费维权'],
		description: '新锐律师，专注于劳动法和消费者权益保护，服务态度认真负责。',
		specialtyType: '劳动法',
		location: '杭州',
		priceRange: 'low'
	}
]

/**
 * 模拟API延迟
 * @param {number} ms 延迟毫秒数
 * @returns {Promise}
 */
const delay = (ms = 500) => new Promise(resolve => setTimeout(resolve, ms))

/**
 * 模拟API响应格式
 * @param {any} data 响应数据
 * @param {boolean} success 是否成功
 * @param {string} message 响应消息
 * @returns {Object}
 */
const createResponse = (data = null, success = true, message = '') => ({
	success,
	data,
	message,
	timestamp: new Date().toISOString()
})

/**
 * 律师服务API
 */
export const lawyerAPI = {
	/**
	 * 获取所有律师列表
	 * @returns {Promise<Object>}
	 */
	async getAllLawyers() {
		await delay()
		try {
			return createResponse(mockLawyers, true, '获取律师列表成功')
		} catch (error) {
			return createResponse(null, false, '获取律师列表失败')
		}
	},

	/**
	 * 根据ID获取律师详情
	 * @param {number} id 律师ID
	 * @returns {Promise<Object>}
	 */
	async getLawyerById(id) {
		await delay()
		try {
			const lawyer = mockLawyers.find(l => l.id === parseInt(id))
			if (lawyer) {
				return createResponse(lawyer, true, '获取律师详情成功')
			} else {
				return createResponse(null, false, '律师不存在')
			}
		} catch (error) {
			return createResponse(null, false, '获取律师详情失败')
		}
	},

	/**
	 * 搜索律师
	 * @param {Object} params 搜索参数
	 * @param {string} params.keyword 搜索关键词
	 * @param {Object} params.filters 筛选条件
	 * @param {number} params.page 页码
	 * @param {number} params.pageSize 每页数量
	 * @returns {Promise<Object>}
	 */
	async searchLawyers({ keyword = '', filters = {}, page = 1, pageSize = 10 } = {}) {
		await delay()
		try {
			let filtered = [...mockLawyers]

			// 按筛选条件过滤
			if (Object.keys(filters).length > 0) {
				filtered = filtered.filter(lawyer => {
					return Object.entries(filters).every(([key, value]) => {
						return lawyer[key] === value
					})
				})
			}

			// 按搜索关键词过滤
			if (keyword.trim()) {
				const searchKeyword = keyword.toLowerCase()
				filtered = filtered.filter(lawyer => 
					lawyer.name.toLowerCase().includes(searchKeyword) ||
					lawyer.firm.toLowerCase().includes(searchKeyword) ||
					lawyer.specialties.some(s => s.toLowerCase().includes(searchKeyword)) ||
					lawyer.description.toLowerCase().includes(searchKeyword)
				)
			}

			// 分页处理
			const total = filtered.length
			const startIndex = (page - 1) * pageSize
			const endIndex = startIndex + pageSize
			const pageData = filtered.slice(startIndex, endIndex)

			return createResponse({
				list: pageData,
				total,
				page,
				pageSize,
				totalPages: Math.ceil(total / pageSize)
			}, true, '搜索成功')
		} catch (error) {
			return createResponse(null, false, '搜索失败')
		}
	},

	/**
	 * 获取筛选选项
	 * @returns {Promise<Object>}
	 */
	async getFilterOptions() {
		await delay(200)
		try {
			const options = {
				specialtyTypes: [
					{ key: 'specialtyType', value: '刑事', label: '刑事辩护' },
					{ key: 'specialtyType', value: '民事', label: '民事纠纷' },
					{ key: 'specialtyType', value: '知识产权', label: '知识产权' },
					{ key: 'specialtyType', value: '交通事故', label: '交通事故' },
					{ key: 'specialtyType', value: '房地产', label: '房地产' },
					{ key: 'specialtyType', value: '劳动法', label: '劳动法' }
				],
				locations: [
					{ key: 'location', value: '北京', label: '北京' },
					{ key: 'location', value: '上海', label: '上海' },
					{ key: 'location', value: '深圳', label: '深圳' },
					{ key: 'location', value: '广州', label: '广州' },
					{ key: 'location', value: '成都', label: '成都' },
					{ key: 'location', value: '杭州', label: '杭州' }
				],
				priceRanges: [
					{ key: 'priceRange', value: 'low', label: '低价位' },
					{ key: 'priceRange', value: 'medium', label: '中价位' },
					{ key: 'priceRange', value: 'high', label: '高价位' }
				]
			}
			return createResponse(options, true, '获取筛选选项成功')
		} catch (error) {
			return createResponse(null, false, '获取筛选选项失败')
		}
	}
}

/**
 * 将来替换为真实API时的示例：
 * 
 * import { http } from '@/utils/request'
 * 
 * export const lawyerAPI = {
 *   // 获取所有律师列表
 *   async getAllLawyers() {
 *     return await http.get('/api/lawyers')
 *   },
 *   
 *   // 根据ID获取律师详情
 *   async getLawyerById(id) {
 *     return await http.get(`/api/lawyers/${id}`)
 *   },
 *   
 *   // 搜索律师
 *   async searchLawyers(params) {
 *     return await http.post('/api/lawyers/search', params)
 *   },
 *   
 *   // 获取筛选选项
 *   async getFilterOptions() {
 *     return await http.get('/api/lawyers/filters')
 *   }
 * }
 * 
 * 使用步骤：
 * 1. 在 main.js 中设置 API 基础地址：
 *    import { setBaseURL } from '@/utils/request'
 *    setBaseURL('https://your-api-domain.com')
 * 
 * 2. 替换上述注释代码到 lawyerAPI 对象
 * 
 * 3. 删除模拟数据和延迟函数
 * 
 * 4. 确保后端API返回的数据格式与模拟数据一致
 */

export default lawyerAPI