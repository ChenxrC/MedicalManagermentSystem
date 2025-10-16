// API服务
import api from '../utils/axios.js'

/**
 * 获取已发布的文档列表
 * @returns {Promise} 文档列表数据
 */
export async function getPublishedDocuments() {
  try {
    const response = await api.get('/documents/published')
    return response
  } catch (error) {
    console.error('获取已发布文档失败:', error)
    // 如果API调用失败，返回模拟数据作为备用
    return {
      data: {
        documents: [
          {
            id: 1,
            title: '系统使用指南',
            content: '<p>欢迎使用本系统！本指南将帮助您快速了解系统的各项功能和操作方法。</p><p>系统主要包括课件/知识库管理、考试系统和人员管理三大模块。</p><p>如需更多帮助，请联系系统管理员。</p>',
            published_at: '2023-01-15T08:00:00Z'
          },
          {
            id: 2,
            title: '考试系统操作手册',
            content: '<p>本手册详细介绍了考试系统的使用方法，包括如何创建试卷、分配考试和查看成绩。</p><p>系统支持多种题型，包括选择题、填空题、简答题等。</p>',
            published_at: '2023-01-10T10:30:00Z'
          }
        ]
      }
    }
  }
}

/**
 * 发布文档到主页
 * @param {number} documentId - 文档ID
 * @returns {Promise} 操作结果
 */
export async function publishDocumentToHomepage(documentId) {
  try {
    const response = await api.post(`/documents/${documentId}/publish`)
    return response.data
  } catch (error) {
    console.error('发布文档到主页失败:', error)
    throw error
  }
}

/**
 * 上传文档
 * @param {Object} documentData - 文档数据
 * @returns {Promise} 上传结果
 */
export async function uploadDocument(documentData) {
  try {
    const response = await api.post('/documents', documentData)
    return response.data
  } catch (error) {
    console.error('上传文档失败:', error)
    throw error
  }
}