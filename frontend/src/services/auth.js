import api from './api'

// 用户注册
export const register = (userData) => {
  return api.post('/auth/register', userData)
}

// 用户登录
export const login = (credentials) => {
  return api.post('/auth/login', credentials)
}

// 保存用户信息到本地存储
export const setUserInfo = (userInfo) => {
  localStorage.setItem('user', JSON.stringify(userInfo))
}

// 保存访问令牌到本地存储
export const setAccessToken = (token) => {
  localStorage.setItem('access_token', token)
}

// 获取本地存储的用户信息
export const getUserInfo = () => {
  const user = localStorage.getItem('user')
  return user ? JSON.parse(user) : null
}

// 获取本地存储的访问令牌
export const getAccessToken = () => {
  return localStorage.getItem('access_token')
}

// 清除本地存储的用户信息
export const clearUserInfo = () => {
  localStorage.removeItem('user')
  localStorage.removeItem('access_token')
}

// 检查用户是否已登录
export const isAuthenticated = () => {
  return !!getAccessToken()
}

// 获取用户角色
export const getUserRole = () => {
  const user = getUserInfo()
  return user ? user.role : null
}