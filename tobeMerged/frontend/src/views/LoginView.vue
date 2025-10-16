<template>
  <div class="login-container">
    <el-form
      ref="loginFormRef"
      v-model="loginForm"
      :rules="loginRules"
      class="login-form"
      label-position="left"
    >
      <div class="title-container">
        <h3 class="title">欢迎登录</h3>
      </div>
      <el-form-item prop="username">
        <el-input
          v-model="loginForm.username"
          type="text"
          placeholder="用户名"
          name="username"
          autocomplete="on"
        />
      </el-form-item>
      <el-form-item prop="password">
        <el-input
          v-model="loginForm.password"
          type="password"
          placeholder="密码"
          name="password"
          show-password
          autocomplete="on"
        />
      </el-form-item>
      <el-form-item>
        <el-checkbox
          v-model="loginForm.rememberMe"
          style="margin: 0 auto 20px 0"
        >
          记住密码
        </el-checkbox>
      </el-form-item>
      <el-form-item>
        <el-button
          type="primary"
          style="width: 100%"
          :loading="loading"
          @click="handleLogin"
        >
          登录
        </el-button>
      </el-form-item>
      <div class="register-link">
        <span>还没有账号？</span>
        <el-button
          type="text"
          @click="handleRegister"
        >
          立即注册
        </el-button>
      </div>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore.js'

const router = useRouter()
const loading = ref(false)
const loginFormRef = ref(null)
const userStore = useUserStore()

const loginForm = reactive({
  username: '',
  password: '',
  rememberMe: false
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: ['blur', 'change'] }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: ['blur', 'change'] }
  ]
}

const handleLogin = async () => {
  try {
    await loginFormRef.value.validate()
    loading.value = true
    // 使用userStore进行登录
    const res = await userStore.login(loginForm)
    
    if (res.success) {
      ElMessage.success('登录成功')
      // 登录成功后手动刷新用户状态
      await userStore.initUser()
      // 根据用户角色决定跳转路径
      if (userStore.userRole === 'admin') {
        router.push('/admin')
      } else if (userStore.userRole === 'student') {
        router.push('/student-exams')
      } else {
        router.push('/')
      }
    } else {
      ElMessage.error(res.error || '登录失败')
    }
  } catch (error) {
    ElMessage.error('登录失败，请重试')
    console.error('登录错误:', error)
  } finally {
    loading.value = false
  }
}

const handleRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
}

.login-form {
  width: 400px;
  padding: 40px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.title-container {
  text-align: center;
  margin-bottom: 30px;
}

.title {
  font-size: 24px;
  color: #303133;
}

.svg-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background-color: #f5f7fa;
  border-radius: 50%;
  margin-right: 15px;
  vertical-align: middle;
}

.register-link {
  text-align: center;
  margin-top: 20px;
  color: #606266;
}

.register-link .el-button {
  color: #409eff;
}

.register-link .el-button:hover {
  color: #66b1ff;
}
</style>