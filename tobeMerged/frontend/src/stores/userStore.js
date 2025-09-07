import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import api from '@/utils/axios'

export const useUserStore = defineStore('user', () => {
  // 用户信息
  const currentUser = ref(null)
  const isLoggedIn = ref(false)
  const token = ref(null)

  // 计算属性
  const userInfo = computed(() => currentUser.value)
  const isAuthenticated = computed(() => isLoggedIn.value && token.value)

  // 初始化用户状态
  const initUser = () => {
    try {
      const userData = localStorage.getItem('studentUser')
      if (userData) {
        const user = JSON.parse(userData)
        currentUser.value = user
        token.value = user.token
        isLoggedIn.value = true
        return true
      }
    } catch (error) {
      console.error('初始化用户状态失败:', error)
      logout()
    }
    return false
  }

  // 登录
  const login = async (credentials) => {
    try {
      const response = await api.post('/api/auth/login/', credentials)
      const userData = response.data.user
      
      currentUser.value = userData
      token.value = 'session' // 使用会话认证
      isLoggedIn.value = true
      localStorage.setItem('studentUser', JSON.stringify(userData))
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('登录失败:', error)
      return { success: false, error: error.response?.data?.error || '登录失败' }
    }
  }

  // 登出
  const logout = async () => {
    try {
      await api.post('/api/auth/logout/')
    } catch (error) {
      console.error('登出请求失败:', error)
    } finally {
      currentUser.value = null
      token.value = null
      isLoggedIn.value = false
      localStorage.removeItem('studentUser')
    }
  }

  // 更新用户信息
  const updateUser = (userData) => {
    currentUser.value = { ...currentUser.value, ...userData }
    localStorage.setItem('studentUser', JSON.stringify(currentUser.value))
  }

  // 检查用户权限
  const hasPermission = (permission) => {
    if (!isAuthenticated.value) return false
    // 这里可以添加权限检查逻辑
    return true
  }

  return {
    currentUser,
    isLoggedIn,
    token,
    userInfo,
    isAuthenticated,
    initUser,
    login,
    logout,
    updateUser,
    hasPermission
  }
})
