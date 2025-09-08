// API工具函数
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'http://localhost:8000' 
  : 'http://localhost:8000'

// 通用请求函数
export const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  }

  const config = {
    ...defaultOptions,
    ...options,
  }

  try {
    const response = await fetch(url, config)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error('API请求失败:', error)
    throw error
  }
}

// 学员相关API
export const studentAPI = {
  // 获取学员列表
  getStudents: () => apiRequest('/api/students/'),
  
  // 创建学员
  createStudent: (data) => apiRequest('/api/students/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  
  // 更新学员
  updateStudent: (id, data) => apiRequest(`/api/students/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  
  // 删除学员
  deleteStudent: (id) => apiRequest(`/api/students/${id}/`, {
    method: 'DELETE',
  }),
}

// 试卷相关API
export const examAPI = {
  // 获取试卷列表
  getExams: () => apiRequest('/api/exams/'),
  
  // 创建试卷
  createExam: (data) => apiRequest('/api/exams/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  
  // 更新试卷
  updateExam: (id, data) => apiRequest(`/api/exams/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  
  // 删除试卷
  deleteExam: (id) => apiRequest(`/api/exams/${id}/`, {
    method: 'DELETE',
  }),
  
  // 更新试卷状态
  updateExamStatus: (id, isActive) => apiRequest(`/api/exams/${id}/`, {
    method: 'PATCH',
    body: JSON.stringify({ is_active: isActive }),
  }),
}

// 试卷分配相关API
export const assignmentAPI = {
  // 获取分配列表
  getAssignments: () => apiRequest('/api/exam-assignments/'),
  
  // 创建分配
  createAssignment: (data) => apiRequest('/api/exam-assignments/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  
  // 移除分配
  removeAssignment: (id) => apiRequest(`/api/exam-assignments/${id}/remove_assignment/`, {
    method: 'POST',
  }),
}
