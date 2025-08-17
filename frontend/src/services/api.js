import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 在发送请求之前做些什么
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    // 对请求错误做些什么
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    // 对响应数据做些什么
    return response
  },
  error => {
    // 对响应错误做些什么
    if (error.response && error.response.status === 401) {
      // token过期或无效，清除本地存储并跳转到登录页
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      // 这里可以添加跳转到登录页的逻辑
      // window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// 课程相关API
export const getCourses = () => api.get('/courses')
export const createCourse = (courseData) => api.post('/courses', courseData)

// 文档相关API
export const getDocuments = () => api.get('/documents')
export const uploadDocument = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/documents', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 考试相关API
export const getExams = () => api.get('/exams')
export const getQuestions = () => api.get('/questions')
export const createExam = (examData) => api.post('/exams', examData)

export default api