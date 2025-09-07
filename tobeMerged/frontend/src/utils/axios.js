import axios from 'axios'
import { useUserStore } from '@/stores/userStore'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器 - 添加认证头
api.interceptors.request.use(
  (config) => {
    // 使用会话认证，不需要额外的认证头
    // Django会自动处理会话认证
    
    // 添加CSRF token（如果需要）
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content')
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken
    }
    
    // 确保包含凭证
    config.withCredentials = true
    
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
    const userStore = useUserStore()
    
    // 如果是401未认证错误，清除用户状态并跳转到登录页
    if (error.response?.status === 401) {
      userStore.logout()
      // 可以在这里添加跳转到登录页的逻辑
      console.log('用户未认证，请重新登录')
    }
    
    return Promise.reject(error)
  }
)

export default api
