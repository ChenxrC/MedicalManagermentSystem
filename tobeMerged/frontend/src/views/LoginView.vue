<template>
  <div class="login-container">
    <div class="login-form-wrapper">
      <h2>用户登录</h2>
      <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin" :loading="loading" style="width: 100%">登录</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="default" @click="goToHome" style="width: 100%">返回主页</el-button>
        </el-form-item>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      </el-form>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '@/stores/userStore'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { defineComponent, ref, reactive } from 'vue'

export default defineComponent({
  name: 'LoginView',
  setup() {
    const userStore = useUserStore()
    const router = useRouter()
    const loginForm = reactive({
      username: '',
      password: ''
    })
    const loading = ref(false)
    const errorMessage = ref('')
    const loginFormRef = ref(null)
    
    const loginRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
      ]
    }
    
    const handleLogin = async () => {
      if (!loginFormRef.value) {
        console.error('表单引用未找到')
        return
      }
      
      loginFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          errorMessage.value = ''
          
          try {
            const result = await userStore.login(loginForm)
            if (result.success) {
              ElMessage.success('登录成功')
              
              // 根据用户角色重定向到不同页面
          const userRole = userStore.currentUser?.role
          if (userRole === 'admin') {
            router.push('/admin')
          } else if (userRole === 'teacher') {
            router.push('/student-exams')
          } else if (userRole === 'student') {
            router.push('/student-exams')
          } else {
            router.push('/')
          }
            } else {
              errorMessage.value = result.error || '登录失败'
            }
          } catch (error) {
            errorMessage.value = '登录失败，请检查用户名和密码'
            console.error('登录错误:', error)
          } finally {
            loading.value = false
          }
        }
      })
    }
    
    const goToHome = () => {
      router.push('/')
    }

    return {
      loginForm,
      loading,
      errorMessage,
      loginRules,
      handleLogin,
      loginFormRef,
      goToHome
    }
  }
})
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.login-form-wrapper {
  width: 400px;
  padding: 30px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.login-form-wrapper h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #303133;
}

.error-message {
  color: #f56c6c;
  font-size: 14px;
  text-align: center;
  margin-top: 10px;
}
</style>