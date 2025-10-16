import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as authLogin, logout as authLogout, getCurrentUser, getToken } from '@/services/auth.js'

// 使用统一的认证服务

export const useUserStore = defineStore('user', () => {
  // 用户信息
  const currentUser = ref(null)
  const isLoggedIn = ref(false)

  // 计算属性
  const userInfo = computed(() => currentUser.value)
  const isAuthenticated = computed(() => isLoggedIn.value && getToken())

  // 初始化用户状态
  const initUser = async () => {
    try {
      // 从本地存储获取用户信息
      const userInfo = getCurrentUser()
      const token = getToken()
      
      if (userInfo && token) {
        currentUser.value = userInfo
        isLoggedIn.value = true
        return true
      }
      
      // 尝试从服务器获取用户信息，但处理可能的404错误
      try {
        // 使用统一的认证服务验证token
        const token = getToken()
        if (token) {
          // 如果本地有token，设置为已登录状态
          currentUser.value = userInfo || {}
          isLoggedIn.value = true
          return true
        }
      } catch (apiError) {
        console.warn('从服务器获取用户信息失败:', apiError)
        // 如果是404错误或其他连接错误，我们不要清除本地存储
        // 只返回false表示初始化失败，但保持应用可以继续使用
      }
      
      return false
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
      console.log('开始登录流程，使用统一的auth服务')
      console.log('登录凭据:', credentials)
      
      // 使用统一的authLogin函数
      const response = await authLogin(credentials)
      
      console.log('登录服务响应:', response)
      
      // 更新状态
      if (response.data) {
        // 从localStorage获取最新的用户信息
        const userInfo = getCurrentUser()
        
        console.log('保存用户信息')
        currentUser.value = userInfo
        isLoggedIn.value = true
        
        console.log('当前用户信息:', currentUser.value)
        console.log('当前登录状态:', isLoggedIn.value)
      }
      
      return { success: true, data: response }
    } catch (error) {
      console.error('登录失败:', error)
      return { success: false, error: error.message || '登录失败' }
    }
  }

  // 登出
  const logout = async () => {
    try {
      // 使用统一的authLogout函数
      await authLogout()
      
      // 重置状态
      currentUser.value = null
      isLoggedIn.value = false
      
      return true
    } catch (error) {
      console.error('登出失败:', error)
      return false
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
      const response = await api.get('/auth/me')
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
