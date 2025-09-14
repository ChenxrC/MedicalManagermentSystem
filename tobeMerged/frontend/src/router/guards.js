import { useUserStore } from '@/stores/userStore'

// 需要登录的路由
const protectedRoutes = [
  '/student-exams',
  '/student-courses',
  '/scores',
  '/wrong-analysis',
  '/account',
  '/admin',
  '/admin/students',
  '/admin/exams',
  '/admin/assignments',
  '/answer/',
  '/grading/',
  '/evaluate-video/'
]

// 管理页面路由 - 管理员专用
const adminOnlyRoutes = [
  '/admin',
  '/admin/users',
  '/admin/students',
  '/admin/exams',
  '/admin/assignments'
]

// 老师权限页面路由
const teacherRoutes = [
  '/admin/exams',
  '/admin/students',
  '/grading/',
  '/scores',
  '/wrong-analysis'
]

// 路由守卫
export function setupRouteGuards(router) {
  router.beforeEach((to, from, next) => {
    const userStore = useUserStore()
    
    // 检查是否是受保护的路由
    const isProtected = protectedRoutes.some(route => 
      to.path === route || to.path.startsWith(route)
    )
    
    // 检查是否是管理员专用路由
    const isAdminOnlyRoute = adminOnlyRoutes.some(route => 
      to.path === route || to.path.startsWith(route)
    )
    
    // 检查是否是老师权限路由
    const isTeacherRoute = teacherRoutes.some(route => 
      to.path === route || to.path.startsWith(route)
    )
    
    // 初始化用户状态
    if (isProtected && !userStore.isAuthenticated) {
      userStore.initUser()
    }
    
    // 如果已登录且访问登录页或注册页，重定向到适当页面
    if ((to.path === '/login' || to.path === '/register') && userStore.isAuthenticated) {
      const userRole = userStore.currentUser?.role
      if (userRole === 'admin') {
        next('/admin')
      } else if (userRole === 'teacher') {
        next('/student-exams')
      } else {
        next('/student-exams')
      }
      return
    }
    
    // 检查是否需要登录
    if (isProtected) {
      if (!userStore.isAuthenticated) {
        // 未登录，重定向到登录页
        next('/login')
        return
      }
      
      // 检查是否是管理员专用路由，需要管理员角色
      if (isAdminOnlyRoute) {
        const userRole = userStore.currentUser?.role
        if (userRole !== 'admin') {
          // 不是管理员，重定向到首页
          next('/')
          return
        }
      } else if (isTeacherRoute) {
        // 检查是否是老师权限路由，需要老师或管理员角色
        const userRole = userStore.currentUser?.role
        if (userRole !== 'admin' && userRole !== 'teacher') {
          // 不是老师或管理员，重定向到首页
          next('/')
          return
        }
      }
    }
    
    next()
  })
}
