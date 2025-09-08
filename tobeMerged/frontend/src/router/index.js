import { createRouter, createWebHistory } from 'vue-router'
import Viewer from '@/views/Viewer.vue'
import { setupRouteGuards } from './guards'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/components/HomePage.vue')
  },
  {
    path: '/viewer',
    name: 'Viewer',
    component: Viewer
  },
  { path: '/exam-editor', component: () => import('@/components/ExamEditor.vue') },
  { path: '/student-login', component: () => import('@/components/StudentLogin.vue') },
  { path: '/student-exams', component: () => import('@/components/StudentExamList.vue') },
  { path: '/student-courses', component: () => import('@/components/StudentCourseList.vue') },
  { path: '/login-test', component: () => import('@/components/StudentLoginTest.vue') },
  { path: '/simple-test', component: () => import('@/components/SimpleLoginTest.vue') },
  { path: '/validation-test', component: () => import('@/components/FormValidationTest.vue') },
  { path: '/login-debug', component: () => import('@/components/LoginTest.vue') },
  { path: '/login-debug-test', component: () => import('@/components/LoginDebugTest.vue') },
  { path: '/answer/:examId', component: () => import('@/components/AnswerInterface.vue') },
  { path: '/grading/:studentId/:examId', component: () => import('@/components/GradingInterface.vue') },
  { path: '/scores', component: () => import('@/components/ScoreView.vue') },
  { path: '/wrong-analysis', component: () => import('@/components/WrongAnalysis.vue') },
  { path: '/account', component: () => import('@/components/AccountManagement.vue') },
  { path: '/evaluate-video/:recordingId', component: () => import('@/components/VideoEvaluation.vue') },
  // 新增管理页面路由
  { path: '/admin', component: () => import('@/components/AdminDashboard.vue') },
  { path: '/admin/students', component: () => import('@/components/StudentManagement.vue') },
  { path: '/admin/exams', component: () => import('@/components/ExamManagement.vue') },
  { path: '/admin/assignments', component: () => import('@/components/AssignmentManagement.vue') },
  { path: '/api-test', component: () => import('@/components/APITest.vue') }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 设置路由守卫
setupRouteGuards(router)

export default router
