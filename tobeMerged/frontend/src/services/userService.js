// 用户和权限管理API服务
import api from '../utils/axios.js'

/**
 * 获取用户列表
 * @returns {Promise} 用户列表数据
 */
export const getUsers = async () => {
  try {
    const response = await api.get('/users')
    return response.data.users || response.data
  } catch (error) {
    console.error('获取用户列表失败:', error)
    throw error
  }
}

/**
 * 更新用户权限
 * @param {number} userId - 用户ID
 * @param {Object} userData - 用户数据，包含权限信息
 * @returns {Promise} 更新后的用户数据
 */
export const updateUserPermissions = async (userId, userData) => {
  try {
    const response = await api.patch(`/users/${userId}`, userData)
    return response.data
  } catch (error) {
    console.error('更新用户权限失败:', error)
    throw error
  }
}

/**
 * 创建新用户
 * @param {Object} userData - 新用户数据
 * @returns {Promise} 创建的用户数据
 */
export const createUser = async (userData) => {
  try {
    const response = await api.post('/users', userData)
    return response.data
  } catch (error) {
    console.error('创建用户失败:', error)
    throw error
  }
}

/**
 * 删除用户
 * @param {number} userId - 用户ID
 * @returns {Promise} 删除结果
 */
export const deleteUser = async (userId) => {
  try {
    const response = await api.delete(`/users/${userId}`)
    return response.data
  } catch (error) {
    console.error('删除用户失败:', error)
    throw error
  }
}

/**
 * 获取角色默认权限配置
 * @returns {Object} 角色默认权限配置
 */
export const getRoleDefaultPermissions = () => {
  return {
    admin: [
      'view_users', 'create_users', 'update_users', 'delete_users',
      'view_courses', 'create_courses', 'update_courses', 'delete_courses',
      'view_documents', 'create_documents', 'update_documents', 'delete_documents',
      'view_exams', 'create_exams', 'update_exams', 'delete_exams',
      'view_results', 'manage_system'
    ],
    teacher: [
      'view_users', 'view_courses', 'create_courses', 'update_courses', 'delete_courses',
      'view_documents', 'create_documents', 'update_documents', 'delete_documents',
      'view_exams', 'create_exams', 'update_exams', 'delete_exams',
      'view_results'
    ],
    student: [
      'view_courses', 'view_documents', 'view_exams', 'take_exams', 'view_results'
    ]
  }
}

export default {
  getUsers,
  updateUserPermissions,
  createUser,
  deleteUser,
  getRoleDefaultPermissions
}