/**
 * 案例管理API服务
 * 提供案例创建、查询、更新等功能
 */

import http from './http.js'

/**
 * 案例相关API
 */
export const caseService = {
  /**
   * 创建新案例
   * @param {Object} caseData - 案例数据
   * @returns {Promise} 案例创建结果
   */
  createCase(caseData) {
    return http.post('/api/v1/cases/', caseData)
  },

  /**
   * 获取案例列表
   * @param {Object} params - 查询参数
   * @returns {Promise} 案例列表
   */
  getCases(params = {}) {
    return http.get('/api/v1/cases/', params)
  },

  /**
   * 获取案例详情
   * @param {string} caseId - 案例ID
   * @returns {Promise} 案例详情
   */
  getCase(caseId) {
    return http.get(`/api/v1/cases/${caseId}`)
  },

  /**
   * 更新案例
   * @param {string} caseId - 案例ID
   * @param {Object} caseData - 更新数据
   * @returns {Promise} 更新结果
   */
  updateCase(caseId, caseData) {
    return http.put(`/api/v1/cases/${caseId}`, caseData)
  },

  /**
   * 删除案例
   * @param {string} caseId - 案例ID
   * @returns {Promise} 删除结果
   */
  deleteCase(caseId) {
    return http.delete(`/api/v1/cases/${caseId}`)
  },

  /**
   * 搜索案例
   * @param {Object} searchParams - 搜索参数
   * @returns {Promise} 搜索结果
   */
  searchCases(searchParams) {
    return http.get('/api/v1/cases/search', searchParams)
  }
}

export default caseService