<template>
  <div class="debug-container">
    <h1>认证调试工具</h1>
    
    <div class="debug-sections">
      <!-- 登录状态信息 -->
      <div class="debug-section">
        <h2>登录状态</h2>
        <div class="status-info">
          <p><strong>是否已登录:</strong> {{ isAuthenticated ? '是' : '否' }}</p>
          <p><strong>当前用户:</strong> {{ userInfo ? userInfo.username : '无' }}</p>
          <p><strong>用户角色:</strong> {{ userInfo ? userInfo.role : '无' }}</p>
          <p><strong>有访问令牌:</strong> {{ hasAccessToken ? '是' : '否' }}</p>
          <p><strong>token长度:</strong> {{ accessToken ? accessToken.length : 0 }}</p>
          <p><strong>token前20字符:</strong> {{ accessToken ? accessToken.substring(0, 20) + '...' : '无' }}</p>
        </div>
      </div>
      
      <!-- LocalStorage内容 -->
      <div class="debug-section">
        <h2>LocalStorage内容</h2>
        <div class="storage-content">
          <pre>{{ localStorageContent }}</pre>
        </div>
      </div>
      
      <!-- API测试 -->
      <div class="debug-section">
        <h2>API测试</h2>
        <div class="api-test">
          <div class="test-api-buttons">
            <el-button type="primary" @click="testUserListAPI">测试用户列表API</el-button>
            <el-button @click="testAuthMeAPI">测试用户信息API</el-button>
            <el-button type="info" @click="testExamsAPI">测试试卷API</el-button>
          </div>
          <div v-if="apiTestResult" class="api-test-result">
            <h3>API响应结果</h3>
            <p><strong>状态码:</strong> {{ apiTestResult.status }}</p>
          <p><strong>请求头:</strong></p>
          <pre>{{ JSON.stringify(apiTestResult.requestHeaders || {}, null, 2) }}</pre>
          <p><strong>响应数据:</strong></p>
          <pre>{{ JSON.stringify(apiTestResult.data, null, 2) }}</pre>
          </div>
        </div>
      </div>
      
      <!-- 操作按钮 -->
      <div class="debug-section">
        <h2>操作工具</h2>
        <div class="action-buttons">
          <el-button type="primary" @click="openUserManagement">打开人员管理页面</el-button>
          <el-button type="info" @click="openPermissionDebug">打开权限调试</el-button>
          <el-button type="warning" @click="clearLocalStorage">清除LocalStorage</el-button>
          <el-button type="danger" @click="forceLogin">强制登录测试</el-button>
        </div>
      </div>
      
      <!-- 调试日志 -->
      <div class="debug-section">
        <h2>调试日志</h2>
        <div class="debug-logs">
          <div v-for="log in logs" :key="log.id" class="log-item">
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
import { useUserStore } from '@/stores/userStore'
import api from '@/utils/axios'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { setAccessToken, setUserInfo, clearUserInfo, getAccessToken, getUserInfo } from '@/utils/auth'

export default {
  name: 'AuthenticationDebug',
  setup() {
    const userStore = useUserStore()
    const router = useRouter()
    const logs = ref([])
    const apiTestResult = ref(null)
    let logId = 0
    
    // 计算属性
    const isAuthenticated = computed(() => userStore.isAuthenticated)
    const userInfo = computed(() => userStore.userInfo)
    const accessToken = computed(() => getAccessToken())
    const hasAccessToken = computed(() => !!accessToken.value)
    const localStorageContent = computed(() => {
      try {
        const items = {}
        for (let i = 0; i < localStorage.length; i++) {
          const key = localStorage.key(i)
          items[key] = localStorage.getItem(key)
        }
        return JSON.stringify(items, null, 2)
      } catch (error) {
        return `无法读取localStorage: ${error.message}`
      }
    })
    
    // 添加日志
    const addLog = (message) => {
      const time = new Date().toLocaleString()
      logs.value.unshift({
        id: logId++, 
        time, 
        message
      })
      console.log(`[${time}] ${message}`)
    }
    
    // 测试用户列表API
    const testUserListAPI = async () => {
      addLog('开始测试用户列表API: /users/')
      apiTestResult.value = null
      
      try {
        const response = await api.get('/users/')
        apiTestResult.value = {
          status: response.status,
          data: response.data
        }
        
        addLog(`API请求成功，状态码: ${response.status}`)
        addLog(`用户数量: ${response.data.users ? response.data.users.length : 0}`)
        ElMessage.success('用户列表API测试成功')
      } catch (error) {
        apiTestResult.value = {
          status: error.response?.status || 0,
          data: error.response?.data || { error: error.message }
        }
        
        addLog(`API请求失败，状态码: ${error.response?.status || '未知'}`)
        addLog(`错误信息: ${error.message}`)
        ElMessage.error('用户列表API测试失败')
      }
    }
    
    // 测试用户信息API
    const testAuthMeAPI = async () => {
      addLog('开始测试用户信息API: /auth/me')
      apiTestResult.value = null
      
      try {
        const response = await api.get('/auth/me')
        apiTestResult.value = {
          status: response.status,
          data: response.data
        }
        
        addLog(`API请求成功，状态码: ${response.status}`)
        addLog(`获取到用户信息: ${response.data.user?.username}`)
        ElMessage.success('用户信息API测试成功')
      } catch (error) {
        apiTestResult.value = {
          status: error.response?.status || 0,
          data: error.response?.data || { error: error.message }
        }
        
        addLog(`API请求失败，状态码: ${error.response?.status || '未知'}`)
        addLog(`错误信息: ${error.message}`)
        ElMessage.error('用户信息API测试失败')
      }
    }
    
    // 测试试卷API
    const testExamsAPI = async () => {
      addLog('开始测试试卷API: /exams/')
      apiTestResult.value = null
      
      try {
        // 创建请求配置，保存原始请求头
        const config = {}
        
        // 发送请求
        const response = await api.get('/exams/', config)
        
        // 获取实际发送的请求头
        const axiosInstance = api.defaults
        const authToken = localStorage.getItem('access_token')
        const requestHeaders = {
          'Authorization': authToken ? `Bearer ${authToken}` : '未设置',
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
        
        apiTestResult.value = {
          status: response.status,
          data: response.data,
          requestHeaders: requestHeaders
        }
        
        addLog(`API请求成功，状态码: ${response.status}`)
        addLog(`试卷数量: ${response.data.exams ? response.data.exams.length : 0}`)
        ElMessage.success('试卷API测试成功')
      } catch (error) {
        const authToken = localStorage.getItem('access_token')
        const requestHeaders = {
          'Authorization': authToken ? `Bearer ${authToken}` : '未设置',
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
        
        apiTestResult.value = {
          status: error.response?.status || 0,
          data: error.response?.data || { error: error.message },
          requestHeaders: requestHeaders
        }
        
        addLog(`API请求失败，状态码: ${error.response?.status || '未知'}`)
        addLog(`错误信息: ${error.message}`)
        ElMessage.error('试卷API测试失败')
      }
    }
    
    // 清除LocalStorage
    const clearLocalStorage = () => {
      addLog('开始清除LocalStorage')
      clearUserInfo()
      addLog('LocalStorage已清除')
      ElMessage.success('LocalStorage已清除')
      
      // 刷新用户状态
      userStore.currentUser = null
      userStore.isLoggedIn = false
    }
    
    // 强制登录测试
    const forceLogin = async () => {
      addLog('开始强制登录测试')
      
      try {
        // 使用默认管理员凭据
        const credentials = {
          username: 'default_admin',
          password: 'admin123'
        }
        
        addLog(`使用凭据登录: ${credentials.username}`)
        const result = await userStore.login(credentials)
        
        if (result.success) {
          addLog('登录成功')
          addLog(`当前用户: ${userStore.currentUser.username}`)
          addLog(`当前角色: ${userStore.currentUser.role}`)
          ElMessage.success('强制登录成功')
        } else {
          addLog(`登录失败: ${result.error}`)
          ElMessage.error(`登录失败: ${result.error}`)
        }
      } catch (error) {
        addLog(`登录过程异常: ${error.message}`)
        ElMessage.error(`登录异常: ${error.message}`)
      }
    }
    
    // 打开人员管理页面
    const openUserManagement = () => {
      addLog('跳转到人员管理页面')
      router.push('/admin/users')
    }

    // 打开权限调试页面
    const openPermissionDebug = () => {
      addLog('打开权限调试页面')
      router.push('/permission-debug')
    }

    // 初始化
    onMounted(() => {
      addLog('调试工具已初始化')
      addLog(`当前登录状态: ${isAuthenticated.value ? '已登录' : '未登录'}`)
      addLog(`有访问令牌: ${hasAccessToken.value ? '是' : '否'}`)
    })

    return {
      isAuthenticated,
      userInfo,
      accessToken,
      hasAccessToken,
      localStorageContent,
      logs,
      apiTestResult,
      testUserListAPI,
      testAuthMeAPI,
      testExamsAPI,
      clearLocalStorage,
      forceLogin,
      openUserManagement,
      openPermissionDebug
    }
  }
}
</script>

<style scoped>
.debug-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.debug-sections {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
  margin-top: 20px;
}

.debug-section {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.debug-section h2 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 18px;
  color: #303133;
  border-bottom: 1px solid #e4e7ed;
  padding-bottom: 10px;
}

.status-info p,
.storage-content pre,
.api-test-result pre {
  margin: 8px 0;
  word-break: break-all;
  white-space: pre-wrap;
}

.storage-content,
.debug-logs {
  max-height: 300px;
  overflow-y: auto;
  background: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
}

.api-test {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.test-api-buttons {
  display: flex;
  gap: 10px;
}

.action-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.log-item {
  display: flex;
  margin-bottom: 5px;
  font-size: 14px;
}

.log-time {
  color: #909399;
  margin-right: 10px;
  min-width: 150px;
}

.log-message {
  color: #303133;
  flex: 1;
}

@media (min-width: 768px) {
  .debug-sections {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .debug-section:nth-child(3),
  .debug-section:nth-child(4) {
    grid-column: span 2;
  }
}
</style>