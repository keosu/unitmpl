/**
 * 聊天服务API
 * 支持Mock和后端API的自动切换
 */

import { config, API_ENDPOINTS } from '@/config/api.js'
import { http } from '@/api/http.js'

// Mock聊天回复数据
const MOCK_REPLIES = [
  "感谢您的咨询。根据您描述的情况，这确实是一个需要仔细分析的法律问题。",
  "从法律角度来看，您遇到的问题涉及多个法律条文。建议我们先梳理一下相关证据。",
  "这类案件在实践中比较常见，通常有以下几种处理方式...",
  "您提到的合同条款确实存在一些问题，我建议从以下几个方面来分析..."
]

const MARKDOWN_REPLIES = [
  `# 法律建议总结

## 您的问题分析

根据您提供的信息，我建议从以下几个方面来处理：

### 1. 合同条款审查
- **核心条款**：仔细检查争议条款的具体内容
- **违约责任**：明确双方的违约责任和赔偿标准
- **履行期限**：确认合同履行的时间要求

### 2. 证据收集
\`\`\`
重要文件清单：
✓ 原始合同文件
✓ 往来邮件记录  
✓ 付款凭证
✓ 交付证明
\`\`\`

### 3. 法律依据

> 根据《合同法》第107条规定："当事人一方不履行合同义务或者履行合同义务不符合约定的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。"

| 处理方式 | 适用情况 | 预期效果 |
|---------|---------|----------|
| 协商解决 | 争议较小 | 快速、成本低 |
| 调解 | 双方有合作意愿 | 维护关系 |
| 仲裁 | 合同有仲裁条款 | 专业、效率高 |
| 诉讼 | 其他方式无效 | 强制执行 |

**下一步建议**：
1. 整理完整的证据材料
2. 评估各种解决方案的可行性
3. 制定具体的维权策略

如需进一步咨询，请随时联系我。`,
  
  `## 🏛️ 诉讼流程指南

### 民事诉讼的基本步骤

#### 第一阶段：起诉准备
1. **起诉条件确认**
   - 原告是与本案有直接利害关系的公民、法人
   - 有明确的被告
   - 有具体的诉讼请求和事实、理由
   - 属于人民法院受理民事诉讼的范围

2. **材料准备**
   \`\`\`markdown
   必备材料：
   - 起诉状（一式两份）
   - 身份证明文件
   - 证据材料清单
   - 代理人委托书（如有）
   \`\`\`

#### 第二阶段：法院受理
- **时间**：法院应在7日内决定是否受理
- **费用**：根据诉讼标的额缴纳案件受理费
- **流程**：
  1. 提交材料
  2. 法院审查
  3. 缴费通知
  4. 正式立案

#### 第三阶段：庭审程序

> **注意**：简易程序审理期限为3个月，普通程序为6个月

**庭审要点**：
- 📋 充分准备答辩材料
- 🎯 突出核心争议焦点
- 📝 注意法庭纪律
- 💼 配合法官调查

有什么具体问题需要我详细解答吗？`
]

/**
 * 模拟延迟
 */
const delay = (ms = 1500) => new Promise(resolve => setTimeout(resolve, ms))

/**
 * 聊天服务API
 */
export const chatAPI = {
  /**
   * 发送聊天消息
   * @param {string} message 用户消息
   * @param {Object} context 上下文信息
   * @returns {Promise<Object>}
   */
  async sendMessage(message, context = {}) {
    if (config.enableMock) {
      // 使用Mock数据
      await delay()
      
      try {
        // 基于消息内容选择回复类型
        const messageLower = message.toLowerCase()
        const markdownKeywords = ['详细', '分析', '流程', '步骤', '总结', '建议', '指南', '如何', '怎么']
        const useMarkdown = markdownKeywords.some(keyword => messageLower.includes(keyword))
        
        const content = useMarkdown 
          ? MARKDOWN_REPLIES[Math.floor(Math.random() * MARKDOWN_REPLIES.length)]
          : MOCK_REPLIES[Math.floor(Math.random() * MOCK_REPLIES.length)]
        
        const responseData = {
          content,
          timestamp: new Date().toISOString(),
          format: useMarkdown ? 'markdown' : 'text',
          metadata: {
            ai_model: 'legal-assistant-v1',
            confidence: Math.round((Math.random() * 0.13 + 0.85) * 100) / 100,
            theme: context.theme || 'light',
            processing_time_ms: Math.floor(Math.random() * 700 + 800)
          }
        }
        
        return {
          success: true,
          data: responseData,
          message: '发送成功'
        }
      } catch (error) {
        return {
          success: false,
          data: {
            content: '抱歉，我现在遇到了一些技术问题，请稍后再试。',
            timestamp: new Date().toISOString(),
            format: 'text',
            metadata: {
              error: true,
              error_type: 'service_unavailable'
            }
          },
          message: '发送失败'
        }
      }
    } else {
      // 使用后端API
      try {
        const response = await http.post(API_ENDPOINTS.CHAT.SEND_MESSAGE, {
          message,
          context
        })
        
        return {
          success: response.success || true,
          data: response.data || response,
          message: '发送成功'
        }
      } catch (error) {
        return {
          success: false,
          data: {
            content: '抱歉，服务暂时不可用，请稍后重试。',
            timestamp: new Date().toISOString(),
            format: 'text',
            metadata: {
              error: true,
              error_type: 'api_error'
            }
          },
          message: error.message || '发送失败'
        }
      }
    }
  },

  /**
   * 获取聊天室列表
   * @param {Object} params 查询参数
   * @returns {Promise<Object>}
   */
  async getChatRooms(params = {}) {
    if (config.enableMock) {
      await delay(500)
      
      // Mock聊天室数据
      const mockRooms = [
        {
          id: '1',
          name: '法律咨询',
          description: 'AI法律助手',
          room_type: 'ai_chat',
          last_message_at: new Date().toISOString(),
          created_at: new Date().toISOString()
        }
      ]
      
      return {
        success: true,
        data: {
          list: mockRooms,
          total: mockRooms.length,
          page: params.page || 1,
          pageSize: params.size || 20
        },
        message: '获取成功'
      }
    } else {
      try {
        const response = await http.get(API_ENDPOINTS.CHAT.ROOMS, params)
        return {
          success: true,
          data: response,
          message: '获取成功'
        }
      } catch (error) {
        return {
          success: false,
          message: error.message || '获取聊天室列表失败'
        }
      }
    }
  },

  /**
   * 获取聊天记录
   * @param {string} roomId 聊天室ID
   * @param {Object} params 查询参数
   * @returns {Promise<Object>}
   */
  async getChatMessages(roomId, params = {}) {
    if (config.enableMock) {
      await delay(300)
      
      // Mock聊天记录
      const mockMessages = []
      
      return {
        success: true,
        data: {
          list: mockMessages,
          total: mockMessages.length,
          page: params.page || 1,
          pageSize: params.size || 50
        },
        message: '获取成功'
      }
    } else {
      try {
        const url = API_ENDPOINTS.CHAT.MESSAGES.replace('{roomId}', roomId)
        const response = await http.get(url, params)
        return {
          success: true,
          data: response,
          message: '获取成功'
        }
      } catch (error) {
        return {
          success: false,
          message: error.message || '获取聊天记录失败'
        }
      }
    }
  },

  /**
   * 创建AI对话
   * @param {Object} conversationData 对话数据
   * @returns {Promise<Object>}
   */
  async createAIConversation(conversationData) {
    if (config.enableMock) {
      await delay(800)
      
      const mockConversation = {
        id: 'conv_' + Date.now(),
        session_id: 'session_' + Date.now(),
        title: conversationData.title || '新对话',
        created_at: new Date().toISOString()
      }
      
      return {
        success: true,
        data: mockConversation,
        message: '创建成功'
      }
    } else {
      try {
        const response = await http.post(API_ENDPOINTS.CHAT.AI_CONVERSATION, conversationData)
        return {
          success: response.success || true,
          data: response.data || response,
          message: '创建成功'
        }
      } catch (error) {
        return {
          success: false,
          message: error.message || '创建AI对话失败'
        }
      }
    }
  }
}

export default chatAPI