<template>
  <div class="login-test">
    <div class="test-container">
      <h2>登录跳转测试</h2>
      
      <div class="test-section">
        <h3>当前用户状态</h3>
        <p>登录状态: {{ isAuthenticated ? '已登录' : '未登录' }}</p>
        <p>用户名: {{ currentUser?.username || '未登录' }}</p>
        <p>Token: {{ token || '无' }}</p>
      </div>

      <div class="test-section">
        <h3>登录测试</h3>
        <el-form :model="loginData" label-width="80px">
          <el-form-item label="用户名">
            <el-input v-model="loginData.username" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="密码">
            <el-input v-model="loginData.password" type="password" placeholder="请输入密码" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="testLogin">测试登录</el-button>
            <el-button @click="testLogout">测试登出</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="test-section">
        <h3>跳转测试</h3>
        <el-button @click="goToStudentExams">跳转到学员考试列表</el-button>
        <el-button @click="goToLogin">跳转到登录页面</el-button>
        <el-button @click="goToHome">跳转到首页</el-button>
      </div>

      <div class="test-section">
        <h3>调试信息</h3>
        <div class="debug-info">
          <p>当前路由: {{ currentRoute }}</p>
          <p>用户信息: {{ JSON.stringify(currentUser, null, 2) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/userStore'

export default {
  name: 'LoginTest',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const userStore = useUserStore()
    
    const loginData = ref({
      username: 'testuser',
      password: '123456'
    })

    const currentUser = computed(() => userStore.userInfo)
    const isAuthenticated = computed(() => userStore.isAuthenticated)
    const token = computed(() => userStore.token)
    const currentRoute = computed(() => route.path)

    const testLogin = async () => {
      try {
        const mockUser = {
          id: 1,
          username: loginData.value.username,
          email: `${loginData.value.username}@example.com`,
          token: 'mock_token_' + Date.now()
        }
        
        userStore.login(mockUser)
        ElMessage.success('登录成功')
        console.log('用户已登录:', mockUser)
      } catch (error) {
        ElMessage.error('登录失败')
        console.error('登录失败:', error)
      }
    }

    const testLogout = () => {
      userStore.logout()
      ElMessage.success('已登出')
      console.log('用户已登出')
    }

    const goToStudentExams = () => {
      router.push('/student-exams')
    }

    const goToLogin = () => {
      router.push('/student-login')
    }

    const goToHome = () => {
      router.push('/')
    }

    onMounted(() => {
      console.log('登录测试页面已加载')
      console.log('当前用户状态:', {
        isAuthenticated: isAuthenticated.value,
        currentUser: currentUser.value,
        token: token.value
      })
    })

    return {
      loginData,
      currentUser,
      isAuthenticated,
      token,
      currentRoute,
      testLogin,
      testLogout,
      goToStudentExams,
      goToLogin,
      goToHome
    }
  }
}
</script>

<style scoped>
.login-test {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.test-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 600px;
}

.test-section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
}

.test-section h3 {
  margin-bottom: 15px;
  color: #303133;
}

.debug-info {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 6px;
  font-family: monospace;
  font-size: 12px;
  white-space: pre-wrap;
  word-break: break-all;
}

.debug-info p {
  margin: 5px 0;
}
</style>
