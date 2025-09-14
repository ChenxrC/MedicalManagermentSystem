// 用户认证工具函数
import api from './axios';

// 用户注册
export const register = async (userData) => {
  const response = await api.post('/api/auth/register', userData);
  return response.data;
};

// 用户登录
export const login = async (credentials) => {
  const response = await api.post('/api/auth/login', credentials);
  
  // 保存令牌和用户信息到本地存储
  if (response.data && response.data.data) {
    setAccessToken(response.data.data.access);
    setUserInfo(response.data.data.user);
  }
  
  return response.data;
};

// 保存用户信息到本地存储
export const setUserInfo = (userInfo) => {
  localStorage.setItem('user', JSON.stringify(userInfo));
};

// 保存访问令牌到本地存储
export const setAccessToken = (token) => {
  localStorage.setItem('access_token', token);
};

// 获取本地存储的用户信息
export const getUserInfo = () => {
  const user = localStorage.getItem('user');
  return user ? JSON.parse(user) : null;
};

// 获取本地存储的访问令牌
export const getAccessToken = () => {
  return localStorage.getItem('access_token');
};

// 清除本地存储的用户信息
export const clearUserInfo = () => {
  localStorage.removeItem('user');
  localStorage.removeItem('access_token');
};

// 检查用户是否已登录
export const isAuthenticated = () => {
  return !!getAccessToken();
};

// 获取用户角色
export const getUserRole = () => {
  const user = getUserInfo();
  return user ? user.role : null;
};