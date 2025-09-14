import { useUserStore } from '@/stores/userStore'

// 权限指令：根据用户权限显示或隐藏元素
export const setupPermissionDirective = (app) => {
  // 检查单个权限
  app.directive('permission', {
    mounted(el, binding) {
      const userStore = useUserStore()
      const requiredPermission = binding.value
      
      // 确保有用户信息
      if (!userStore.isAuthenticated || !userStore.currentUser) {
        el.style.display = 'none'
        return
      }
      
      // 检查用户是否有权限
      const hasPermission = userStore.hasPermission(requiredPermission)
      
      if (!hasPermission) {
        el.style.display = 'none'
      }
    },
    updated(el, binding) {
      // 组件更新时重新检查权限
      const userStore = useUserStore()
      const requiredPermission = binding.value
      
      // 确保有用户信息
      if (!userStore.isAuthenticated || !userStore.currentUser) {
        el.style.display = 'none'
        return
      }
      
      // 检查用户是否有权限
      const hasPermission = userStore.hasPermission(requiredPermission)
      
      if (!hasPermission) {
        el.style.display = 'none'
      } else {
        // 如果之前被隐藏但现在有权限了，恢复显示
        el.style.display = ''
      }
    }
  })
  
  // 检查用户角色
  app.directive('role', {
    mounted(el, binding) {
      const userStore = useUserStore()
      const requiredRole = binding.value
      
      // 确保有用户信息
      if (!userStore.isAuthenticated || !userStore.currentUser) {
        el.style.display = 'none'
        return
      }
      
      // 检查用户角色
      const hasRole = userStore.hasRole(requiredRole)
      
      if (!hasRole) {
        el.style.display = 'none'
      }
    },
    updated(el, binding) {
      // 组件更新时重新检查角色
      const userStore = useUserStore()
      const requiredRole = binding.value
      
      // 确保有用户信息
      if (!userStore.isAuthenticated || !userStore.currentUser) {
        el.style.display = 'none'
        return
      }
      
      // 检查用户角色
      const hasRole = userStore.hasRole(requiredRole)
      
      if (!hasRole) {
        el.style.display = 'none'
      } else {
        // 如果之前被隐藏但现在有角色了，恢复显示
        el.style.display = ''
      }
    }
  })
  
  // 检查多个权限（任一权限满足即可）
  app.directive('any-permission', {
    mounted(el, binding) {
      const userStore = useUserStore()
      const requiredPermissions = Array.isArray(binding.value) ? binding.value : [binding.value]
      
      // 确保有用户信息
      if (!userStore.isAuthenticated || !userStore.currentUser) {
        el.style.display = 'none'
        return
      }
      
      // 检查是否有任一权限
      const hasAnyPermission = requiredPermissions.some(permission => 
        userStore.hasPermission(permission)
      )
      
      if (!hasAnyPermission) {
        el.style.display = 'none'
      }
    }
  })
  
  // 检查多个角色（任一角色满足即可）
  app.directive('any-role', {
    mounted(el, binding) {
      const userStore = useUserStore()
      const requiredRoles = Array.isArray(binding.value) ? binding.value : [binding.value]
      
      // 确保有用户信息
      if (!userStore.isAuthenticated || !userStore.currentUser) {
        el.style.display = 'none'
        return
      }
      
      // 检查是否有任一角色
      const hasAnyRole = requiredRoles.some(role => 
        userStore.hasRole(role)
      )
      
      if (!hasAnyRole) {
        el.style.display = 'none'
      }
    }
  })
}

// 权限检查辅助函数
export const checkPermission = (permission) => {
  const userStore = useUserStore()
  return userStore.hasPermission(permission)
}

export const checkRole = (role) => {
  const userStore = useUserStore()
  return userStore.hasRole(role)
}

export const checkAnyPermission = (...permissions) => {
  const userStore = useUserStore()
  return permissions.some(permission => userStore.hasPermission(permission))
}

export const checkAnyRole = (...roles) => {
  const userStore = useUserStore()
  return roles.some(role => userStore.hasRole(role))
}

// 权限过滤器：在模板中可以使用的权限过滤函数
export const permissionFilters = {
  hasPermission: checkPermission,
  hasRole: checkRole,
  hasAnyPermission: checkAnyPermission,
  hasAnyRole: checkAnyRole
}

// 权限常量，用于统一管理权限名称
export const PERMISSIONS = {
  // 用户管理权限
  VIEW_USERS: 'view_users',
  CREATE_USERS: 'create_users',
  UPDATE_USERS: 'update_users',
  DELETE_USERS: 'delete_users',
  
  // 课程管理权限
  VIEW_COURSES: 'view_courses',
  CREATE_COURSES: 'create_courses',
  UPDATE_COURSES: 'update_courses',
  DELETE_COURSES: 'delete_courses',
  
  // 文档管理权限
  VIEW_DOCUMENTS: 'view_documents',
  CREATE_DOCUMENTS: 'create_documents',
  UPDATE_DOCUMENTS: 'update_documents',
  DELETE_DOCUMENTS: 'delete_documents',
  
  // 考试管理权限
  VIEW_EXAMS: 'view_exams',
  CREATE_EXAMS: 'create_exams',
  UPDATE_EXAMS: 'update_exams',
  DELETE_EXAMS: 'delete_exams',
  
  // 结果管理权限
  VIEW_RESULTS: 'view_results',
  
  // 学生权限
  TAKE_EXAMS: 'take_exams',
  
  // 系统管理权限
  MANAGE_SYSTEM: 'manage_system'
}

// 角色常量
export const ROLES = {
  ADMIN: 'admin',
  TEACHER: 'teacher',
  STUDENT: 'student'
}

// 权限组，用于简化权限检查
export const PERMISSION_GROUPS = {
  // 用户管理相关权限组
  USER_MANAGEMENT: [
    PERMISSIONS.VIEW_USERS,
    PERMISSIONS.CREATE_USERS,
    PERMISSIONS.UPDATE_USERS,
    PERMISSIONS.DELETE_USERS
  ],
  
  // 课程管理相关权限组
  COURSE_MANAGEMENT: [
    PERMISSIONS.VIEW_COURSES,
    PERMISSIONS.CREATE_COURSES,
    PERMISSIONS.UPDATE_COURSES,
    PERMISSIONS.DELETE_COURSES
  ],
  
  // 文档管理相关权限组
  DOCUMENT_MANAGEMENT: [
    PERMISSIONS.VIEW_DOCUMENTS,
    PERMISSIONS.CREATE_DOCUMENTS,
    PERMISSIONS.UPDATE_DOCUMENTS,
    PERMISSIONS.DELETE_DOCUMENTS
  ],
  
  // 考试管理相关权限组
  EXAM_MANAGEMENT: [
    PERMISSIONS.VIEW_EXAMS,
    PERMISSIONS.CREATE_EXAMS,
    PERMISSIONS.UPDATE_EXAMS,
    PERMISSIONS.DELETE_EXAMS
  ]
}