import { apiRequest } from '@/utils/api.js'
import api from '@/utils/axios.js'

/**
 * 用户注册
 * @param {Object} userInfo - 用户注册信息
 * @returns {Promise<Object>} - 注册结果
 */
export const register = async (userInfo) => {
  try {
    const response = await api.post('/auth/register', userInfo)
    return response
  } catch (error) {
    console.error('注册失败:', error)
    throw error
  }
}

/**
 * 用户登录
 * @param {Object} credentials - 用户登录凭证
 * @returns {Promise<Object>} - 登录结果
 */
export const login = async (credentials) => {
  try {
    const response = await api.post('/auth/login', credentials)
    
    // 如果登录成功，保存token和用户信息
    if (response.access_token) {
      // 统一使用access_token作为键名
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('userInfo', JSON.stringify(response.user || {}))
      // 保存用户角色，用于路由守卫的权限控制
      if (response.user && response.user.role) {
        localStorage.setItem('user_role', response.user.role)
      }
      // 返回符合userStore期望格式的响应
      return {
        data: {
          access: response.access_token,
          user: response.user
        }
      }
    }
    
    // 处理登录失败情况
    return {
      code: response.code || 401,
      msg: response.message || '登录失败',
      data: {}
    }
  } catch (error) {
    console.error('登录失败:', error)
    throw error
  }
}

/**
 * 用户注销
 * @returns {Promise<void>}
 */
export const logout = async () => {
  try {
    await api.post('/auth/logout')
  } catch (error) {
    console.error('注销失败:', error)
  } finally {
    // 清除本地存储的token和用户信息，使用统一的键名
    localStorage.removeItem('access_token')
    localStorage.removeItem('userInfo')
    localStorage.removeItem('user_role')
  }
}

/**
 * 获取当前登录用户信息
 * @returns {Object|null} - 用户信息对象或null
 */
export const getCurrentUser = () => {
  try {
    const userInfo = localStorage.getItem('userInfo')
    return userInfo ? JSON.parse(userInfo) : null
  } catch (error) {
    console.error('获取用户信息失败:', error)
    return null
  }
}

/**
 * 获取存储的token
 * @returns {string|null} - token字符串或null
 */
export const getToken = () => {
  try {
    // 统一使用access_token作为键名
    return localStorage.getItem('access_token') || null
  } catch (error) {
    console.error('获取token失败:', error)
    return null
  }
}

/**
 * 验证token是否有效
 * @returns {Promise<boolean>} - token是否有效
 */
export const validateToken = async () => {
  try {
    const token = getToken()
    if (!token) {
      return false
    }
    
    // 使用统一的apiRequest函数
    const response = await apiRequest('/auth/validate-token', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    return response.code === 200
  } catch (error) {
    console.error('验证token失败:', error)
    return false
  }
}

/**
 * 更新用户信息
 * @param {Object} userInfo - 要更新的用户信息
 * @returns {Promise<Object>} - 更新结果
 */
export const updateUserInfo = async (userInfo) => {
  try {
    const response = await api.put('/user/info', userInfo)
    
    // 如果更新成功，更新本地存储的用户信息
    if (response.data.code === 200 && response.data.data) {
      localStorage.setItem('userInfo', JSON.stringify(response.data.data))
    }
    
    return response.data
  } catch (error) {
    console.error('更新用户信息失败:', error)
    throw error
  }
}

/**
 * 修改密码
 * @param {Object} passwordInfo - 密码修改信息
 * @returns {Promise<Object>} - 修改结果
 */
export const changePassword = async (passwordInfo) => {
  try {
    const response = await api.put('/auth/change-password', passwordInfo)
    return response.data
  } catch (error) {
    console.error('修改密码失败:', error)
    throw error
  }
}

/**
 * 忘记密码，发送重置链接
 * @param {string} email - 用户邮箱
 * @returns {Promise<Object>} - 发送结果
 */
export const forgotPassword = async (email) => {
  try {
    const response = await api.post('/auth/forgot-password', { email })
    return response.data
  } catch (error) {
    console.error('发送重置密码链接失败:', error)
    throw error
  }
}