import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'LoginView',
    component: () => import('@/views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'RegisterView',
    component: () => import('@/views/RegisterView.vue')
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('@/views/AdminDashboard.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/student-exams',
    name: 'StudentExams',
    component: () => import('@/views/StudentExams.vue'),
    meta: {
      requiresAuth: true,
      requiresStudent: true
    }
  },
  {
    path: '/documents',
    name: 'Documents',
    component: () => import('@/views/DocumentsView.vue'),
    meta: {
      requiresAuth: true
    }
  },
  // 管理系统子路由
  {
    path: '/admin/users',
    name: 'UserManagement',
    component: () => import('@/components/UserManagement.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/admin/exams',
    name: 'ExamManagement',
    component: () => import('@/components/ExamManagement.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {    path: '/admin/assignments',    name: 'ExamAssignment',    component: () => import('@/components/ExamAssignment.vue'),    meta: {      requiresAuth: true,      requiresAdmin: true    }  },  // 考试系统路由
  {
    path: '/student/exams',
    name: 'StudentExamList',
    component: () => import('@/components/StudentExamList.vue'),
    meta: {
      requiresAuth: true,
      requiresStudent: true
    }
  },
  {
    path: '/admin-center',
    name: 'AdminCenter',
    component: () => import('@/components/AdminCenter.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 全局路由守卫
router.beforeEach((to, from, next) => {
  // 检查路由是否需要认证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查是否已登录，使用统一的access_token键名
    const token = localStorage.getItem('access_token')
    if (!token) {
      // 未登录，重定向到登录页
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
      return
    }
    
    // 检查是否需要管理员权限
    if (to.matched.some(record => record.meta.requiresAdmin)) {
      const userRole = localStorage.getItem('user_role')
      if (userRole !== 'admin') {
        next({ path: '/' })
        return
      }
    }
    
    // 检查是否需要学生权限
    if (to.matched.some(record => record.meta.requiresStudent)) {
      const userRole = localStorage.getItem('user_role')
      if (userRole !== 'student') {
        next({ path: '/' })
        return
      }
    }
    
    // 已登录且权限匹配，继续访问
    next()
  } else {
    // 不需要认证的路由，直接访问
    next()
  }
})

export default router
