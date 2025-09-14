import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import api from '@/utils/axios'

// 导入认证工具函数
import {
  setUserInfo,
  setAccessToken,
  getUserInfo,
  getAccessToken,
  clearUserInfo
} from '@/utils/auth'

export const useUserStore = defineStore('user', () => {
  // 用户信息
  const currentUser = ref(null)
  const isLoggedIn = ref(false)

  // 计算属性
  const userInfo = computed(() => currentUser.value)
  const isAuthenticated = computed(() => isLoggedIn.value && getAccessToken())

  // 初始化用户状态
  const initUser = async () => {
    try {
      // 从本地存储获取用户信息
      const userInfo = getUserInfo()
      const token = getAccessToken()
      
      if (userInfo && token) {
        currentUser.value = userInfo
        isLoggedIn.value = true
        return true
      }
      
      // 尝试从服务器获取用户信息，但处理可能的404错误
      try {
        const response = await api.get('/api/auth/me')
        currentUser.value = response.data.user
        isLoggedIn.value = true
        
        // 保存用户信息到本地存储
        setUserInfo(response.data.user)
        
        return true
      } catch (apiError) {
        console.warn('从服务器获取用户信息失败（可能是因为端点不存在）:', apiError)
        // 如果是404错误或其他连接错误，我们不要清除本地存储
        // 只返回false表示初始化失败，但保持应用可以继续使用
        return false
      }
    } catch (error) {
      console.error('初始化用户失败:', error)
      // 这里不清除本地存储，因为可能只是API调用问题
      currentUser.value = null
      isLoggedIn.value = false
      return false
    }
  }

  // 登录
  const login = async (credentials) => {
    try {
      const response = await api.post('/api/auth/login', credentials)
      
      // 保存JWT令牌和用户信息
      if (response.data && response.data.data && response.data.data.access) {
        setAccessToken(response.data.data.access)
      }
      
      if (response.data && response.data.data && response.data.data.user) {
        currentUser.value = response.data.data.user
        setUserInfo(response.data.data.user)
      }
      
      isLoggedIn.value = true
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('登录失败:', error)
      return { success: false, error: error.response?.data?.error || '登录失败' }
    }
  }

  // 登出
  const logout = async () => {
    try {
      // 清除本地存储
      clearUserInfo()
      
      // 重置状态
      currentUser.value = null
      isLoggedIn.value = false
      
      // 可选：发送登出请求到服务器
      try {
        await api.post('/api/logout/')
      } catch (logoutError) {
        console.error('登出请求失败，但仍然清除了本地状态:', logoutError)
      }
    } catch (error) {
      console.error('登出过程失败:', error)
      // 无论如何都重置状态
      currentUser.value = null
      isLoggedIn.value = false
      clearUserInfo()
    }
  }

  // 更新用户信息
  const updateUser = async (userData) => {
    try {
      const response = await api.put('/api/update/', userData)
      currentUser.value = response.data
      setUserInfo(response.data)
      return response.data
    } catch (error) {
      console.error('更新用户信息失败:', error)
      throw error
    }
  }

  // 检查用户权限
  const hasPermission = (permission) => {
    if (!isAuthenticated.value || !currentUser.value?.permissions) {
      return false
    }
    // 如果是管理员，拥有所有权限
    if (currentUser.value.role === 'admin') {
      return true
    }
    return currentUser.value.permissions.includes(permission)
  }

  // 检查用户角色
  const hasRole = (role) => {
    if (!isAuthenticated.value || !currentUser.value?.role) {
      return false
    }
    // 如果是管理员，也拥有老师角色的权限
    if (role === 'teacher' && currentUser.value.role === 'admin') {
      return true
    }
    return currentUser.value.role === role
  }

  // 刷新用户权限
  const refreshUserPermissions = async () => {
    try {
      const response = await api.get('/api/auth/me')
      if (response.data && response.data.user) {
        currentUser.value = response.data.user
        setUserInfo(response.data.user)
        return true
      }
    } catch (error) {
      console.error('刷新用户权限失败:', error)
    }
    return false
  }

  return {
    currentUser,
    isLoggedIn,
    userInfo,
    isAuthenticated,
    initUser,
    login,
    logout,
    updateUser,
    hasPermission,
    hasRole,
    refreshUserPermissions
  }
})
