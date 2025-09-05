/**
 * 聊天服务API模块
 * 提供统一的聊天相关API接口
 * 当前使用mock数据，未来可无缝切换到真实后端API
 */

import { 
	getRandomMarkdownReply, 
	getReplyByKeyword, 
	getThemeReply,
	getErrorReply,
	mockApiResponse 
} from '@/mock/chatReplies.js'

/**
 * 发送消息并获取AI回复
 * @param {string} message - 用户发送的消息
 * @param {Object} options - 可选参数
 * @param {string} options.theme - 当前主题 (light/dark)
 * @param {number} options.delay - 模拟延迟时间(ms)
 * @returns {Promise<Object>} API响应对象
 */
export async function sendMessage(message, options = {}) {
	const { theme = 'light', delay = 1500 } = options
	
	try {
		// 分析用户消息，选择合适的回复
		let replyContent = getRandomMarkdownReply()
		
		// 简单的关键词匹配
		const lowerMessage = message.toLowerCase()
		if (lowerMessage.includes('代码') || lowerMessage.includes('code')) {
			replyContent = getReplyByKeyword('代码')
		} else if (lowerMessage.includes('列表') || lowerMessage.includes('list')) {
			replyContent = getReplyByKeyword('列表')
		} else if (lowerMessage.includes('表格') || lowerMessage.includes('table')) {
			replyContent = getReplyByKeyword('表格')
		} else if (lowerMessage.includes('主题') || lowerMessage.includes('theme')) {
			replyContent = getThemeReply(theme)
		}
		
		// 使用mock API响应
		const response = await mockApiResponse(replyContent, delay)
		
		return {
			success: true,
			data: {
				...response.data,
				userMessage: message,
				messageId: generateMessageId()
			}
		}
	} catch (error) {
		console.error('发送消息失败:', error)
		return {
			success: false,
			error: error.message,
			data: {
				content: getErrorReply(),
				timestamp: new Date().toISOString(),
				type: 'error',
				format: 'text'
			}
		}
	}
}

/**
 * 获取聊天历史记录
 * @param {number} limit - 获取条数限制
 * @param {number} offset - 偏移量
 * @returns {Promise<Object>} 聊天历史数据
 */
export async function getChatHistory(limit = 20, offset = 0) {
	// 模拟API调用
	return new Promise((resolve) => {
		setTimeout(() => {
			resolve({
				success: true,
				data: {
					messages: [], // 在实际应用中这里会是历史消息列表
					total: 0,
					hasMore: false
				}
			})
		}, 300)
	})
}

/**
 * 删除聊天记录
 * @param {string} messageId - 消息ID
 * @returns {Promise<Object>} 删除结果
 */
export async function deleteMessage(messageId) {
	return new Promise((resolve) => {
		setTimeout(() => {
			resolve({
				success: true,
				message: '消息删除成功'
			})
		}, 200)
	})
}

/**
 * 清空聊天记录
 * @returns {Promise<Object>} 清空结果
 */
export async function clearChatHistory() {
	return new Promise((resolve) => {
		setTimeout(() => {
			resolve({
				success: true,
				message: '聊天记录已清空'
			})
		}, 500)
	})
}

/**
 * 生成消息ID
 * @returns {string} 唯一消息ID
 */
function generateMessageId() {
	return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

/**
 * 格式化消息数据
 * @param {Object} rawMessage - 原始消息数据
 * @returns {Object} 格式化后的消息对象
 */
export function formatMessage(rawMessage) {
	return {
		id: rawMessage.id || generateMessageId(),
		type: rawMessage.type || 'received',
		content: rawMessage.content || '',
		timestamp: rawMessage.timestamp ? new Date(rawMessage.timestamp) : new Date(),
		format: rawMessage.format || 'text',
		status: rawMessage.status || 'sent'
	}
}

/**
 * 验证消息内容
 * @param {string} content - 消息内容
 * @returns {Object} 验证结果
 */
export function validateMessage(content) {
	if (!content || content.trim().length === 0) {
		return {
			valid: false,
			error: '消息内容不能为空'
		}
	}
	
	if (content.length > 500) {
		return {
			valid: false,
			error: '消息内容过长，请控制在500字符以内'
		}
	}
	
	return {
		valid: true
	}
}

// 导出默认配置
export default {
	sendMessage,
	getChatHistory,
	deleteMessage,
	clearChatHistory,
	formatMessage,
	validateMessage
}