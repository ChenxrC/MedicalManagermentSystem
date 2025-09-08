import { useUserStore } from '@/stores/userStore'

// 需要登录的路由
const protectedRoutes = [
  '/student-exams',
  '/student-courses',
  '/scores',
  '/wrong-analysis',
  '/account'
]

// 路由守卫
export function setupRouteGuards(router) {
  router.beforeEach((to, from, next) => {
    const userStore = useUserStore()
    
    // 初始化用户状态
    if (!userStore.isAuthenticated) {
      userStore.initUser()
    }
    
    // 检查是否需要登录
    if (protectedRoutes.includes(to.path)) {
      if (!userStore.isAuthenticated) {
        // 未登录，重定向到登录页
        next('/student-login')
        return
      }
    }
    
    // 如果已登录且访问登录页，重定向到学员首页
    if (to.path === '/student-login' && userStore.isAuthenticated) {
      next('/student-exams')
      return
    }
    
    next()
  })
}
