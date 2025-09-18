import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器 - 添加JWT认证头
api.interceptors.request.use(
  (config) => {
    // 获取本地存储的JWT令牌
    const token = localStorage.getItem('access_token')
    
    if (token) {
      // 添加Authorization头
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理认证错误
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // 如果是401未认证错误，清除本地存储并跳转到登录页
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      
      // 跳转到登录页
      if (window && window.location) {
        window.location.href = '/login'
      }
    }
    
    return Promise.reject(error)
  }
)

export default api
