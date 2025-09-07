<template>
  <div class="login-debug-test">
    <div class="test-container">
      <h2>登录跳转调试测试</h2>
      
      <div class="test-section">
        <h3>当前用户状态</h3>
        <p>登录状态: {{ isAuthenticated ? '已登录' : '未登录' }}</p>
        <p>用户名: {{ currentUser?.username || '未登录' }}</p>
        <p>Token: {{ token || '无' }}</p>
        <p>用户ID: {{ currentUser?.id || '无' }}</p>
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
            <el-button @click="clearStorage">清除存储</el-button>
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
          <p>localStorage内容: {{ localStorageContent }}</p>
          <p>用户信息: {{ JSON.stringify(currentUser, null, 2) }}</p>
        </div>
      </div>

      <div class="test-section">
        <h3>操作日志</h3>
        <div class="log-container">
          <div v-for="(log, index) in logs" :key="index" class="log-item">
            <span class="log-time">{{ log.time }}</span>
            <span class="log-message">{{ log.message }}</span>
          </div>
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
  name: 'LoginDebugTest',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const userStore = useUserStore()
    
    const loginData = ref({
      username: 'testuser',
      password: '123456'
    })

    const logs = ref([])

    const currentUser = computed(() => userStore.userInfo)
    const isAuthenticated = computed(() => userStore.isAuthenticated)
    const token = computed(() => userStore.token)
    const currentRoute = computed(() => route.path)
    const localStorageContent = computed(() => {
      try {
        return localStorage.getItem('studentUser') || '无数据'
      } catch (error) {
        return '无法读取localStorage'
      }
    })

    const addLog = (message) => {
      const time = new Date().toLocaleTimeString()
      logs.value.unshift({ time, message })
      console.log(`[${time}] ${message}`)
    }

    const testLogin = async () => {
      try {
        addLog('开始测试登录...')
        
        const mockUser = {
          id: 1,
          username: loginData.value.username,
          email: `${loginData.value.username}@example.com`,
          token: 'mock_token_' + Date.now()
        }
        
        addLog(`创建模拟用户: ${mockUser.username}`)
        
        // 直接设置用户状态
        userStore.currentUser = mockUser
        userStore.token = mockUser.token
        userStore.isLoggedIn = true
        localStorage.setItem('studentUser', JSON.stringify(mockUser))
        
        addLog('用户状态已设置')
        addLog('localStorage已更新')
        
        ElMessage.success('登录成功')
        addLog('登录成功消息已显示')
        
        // 等待一下再跳转
        setTimeout(async () => {
          addLog('准备跳转到学员考试列表...')
          await router.push('/student-exams')
          addLog('跳转完成')
        }, 500)
        
      } catch (error) {
        addLog(`登录失败: ${error.message}`)
        ElMessage.error('登录失败')
        console.error('登录失败:', error)
      }
    }

    const testLogout = () => {
      addLog('开始测试登出...')
      userStore.logout()
      addLog('用户状态已清除')
      ElMessage.success('已登出')
    }

    const clearStorage = () => {
      addLog('清除localStorage...')
      localStorage.removeItem('studentUser')
      addLog('localStorage已清除')
      ElMessage.success('存储已清除')
    }

    const goToStudentExams = () => {
      addLog('手动跳转到学员考试列表...')
      router.push('/student-exams')
    }

    const goToLogin = () => {
      addLog('手动跳转到登录页面...')
      router.push('/student-login')
    }

    const goToHome = () => {
      addLog('手动跳转到首页...')
      router.push('/')
    }

    onMounted(() => {
      addLog('登录调试测试页面已加载')
      addLog(`当前用户状态: ${isAuthenticated.value ? '已登录' : '未登录'}`)
      addLog(`当前路由: ${route.path}`)
    })

    return {
      loginData,
      currentUser,
      isAuthenticated,
      token,
      currentRoute,
      localStorageContent,
      logs,
      testLogin,
      testLogout,
      clearStorage,
      goToStudentExams,
      goToLogin,
      goToHome
    }
  }
}
</script>

<style scoped>
.login-debug-test {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.test-container {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.test-container h2 {
  text-align: center;
  color: #303133;
  margin-bottom: 30px;
}

.test-section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  background: #fafafa;
}

.test-section h3 {
  color: #303133;
  margin-bottom: 15px;
  border-bottom: 2px solid #409eff;
  padding-bottom: 8px;
}

.debug-info {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  font-family: monospace;
  font-size: 12px;
  max-height: 200px;
  overflow-y: auto;
}

.log-container {
  background: #1e1e1e;
  color: #fff;
  padding: 15px;
  border-radius: 6px;
  max-height: 300px;
  overflow-y: auto;
  font-family: monospace;
  font-size: 12px;
}

.log-item {
  margin-bottom: 5px;
  padding: 2px 0;
}

.log-time {
  color: #4fc08d;
  margin-right: 10px;
}

.log-message {
  color: #fff;
}

.el-button {
  margin-right: 10px;
  margin-bottom: 10px;
}
</style>
