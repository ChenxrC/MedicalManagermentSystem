<template>
  <div class="permission-debug-container">
    <h1>权限调试工具</h1>
    
    <div class="debug-sections">
      <!-- 认证状态信息 -->
      <div class="debug-section">
        <h2>认证状态详情</h2>
        <div class="status-info">
          <p><strong>是否已登录:</strong> {{ isAuthenticated ? '是' : '否' }}</p>
          <p><strong>当前用户:</strong> {{ userInfo ? userInfo.username : '无' }}</p>
          <p><strong>用户角色:</strong> {{ userInfo ? userInfo.role : '无' }}</p>
          <p><strong>用户ID:</strong> {{ userInfo ? userInfo.id : '无' }}</p>
          <p><strong>有访问令牌:</strong> {{ hasAccessToken ? '是' : '否' }}</p>
          <p><strong>token长度:</strong> {{ accessToken ? accessToken.length : 0 }}</p>
          <p><strong>token前20字符:</strong> {{ accessToken ? accessToken.substring(0, 20) + '...' : '无' }}</p>
        </div>
      </div>
      
      <!-- 权限信息 -->
      <div class="debug-section" v-if="userInfo">
        <h2>权限列表</h2>
        <div class="permissions-list">
          <div class="permission-group">
          <h3>考试管理权限</h3>
          <div class="permission-item">
            <span class="permission-name">查看试卷</span>
            <span class="permission-key">{{ PERMISSIONS.VIEW_EXAMS }}</span>
            <span class="permission-status" :class="hasPermission(PERMISSIONS.VIEW_EXAMS) ? 'granted' : 'denied'">
              {{ hasPermission(PERMISSIONS.VIEW_EXAMS) ? '已授权' : '未授权' }}
            </span>
          </div>
          <div class="permission-item">
            <span class="permission-name">创建试卷</span>
            <span class="permission-key">{{ PERMISSIONS.CREATE_EXAMS }}</span>
            <span class="permission-status" :class="hasPermission(PERMISSIONS.CREATE_EXAMS) ? 'granted' : 'denied'">
              {{ hasPermission(PERMISSIONS.CREATE_EXAMS) ? '已授权' : '未授权' }}
            </span>
          </div>
          <div class="permission-item">
            <span class="permission-name">更新试卷</span>
            <span class="permission-key">{{ PERMISSIONS.UPDATE_EXAMS }}</span>
            <span class="permission-status" :class="hasPermission(PERMISSIONS.UPDATE_EXAMS) ? 'granted' : 'denied'">
              {{ hasPermission(PERMISSIONS.UPDATE_EXAMS) ? '已授权' : '未授权' }}
            </span>
          </div>
          <div class="permission-item">
            <span class="permission-name">删除试卷</span>
            <span class="permission-key">{{ PERMISSIONS.DELETE_EXAMS }}</span>
            <span class="permission-status" :class="hasPermission(PERMISSIONS.DELETE_EXAMS) ? 'granted' : 'denied'">
              {{ hasPermission(PERMISSIONS.DELETE_EXAMS) ? '已授权' : '未授权' }}
            </span>
          </div>
        </div>
        
        <div class="permission-group">
          <h3>角色信息</h3>
          <div class="permission-item">
            <span class="permission-name">当前角色</span>
            <span class="permission-value">{{ userInfo?.role || '未登录' }}</span>
          </div>
          <div class="permission-item">
            <span class="permission-name">是否管理员</span>
            <span class="permission-status" :class="userStore.hasRole('admin') ? 'granted' : 'denied'">
              {{ userStore.hasRole('admin') ? '是' : '否' }}
            </span>
          </div>
          <div class="permission-item">
            <span class="permission-name">是否教师</span>
            <span class="permission-status" :class="userStore.hasRole('teacher') ? 'granted' : 'denied'">
              {{ userStore.hasRole('teacher') ? '是' : '否' }}
            </span>
          </div>
          <div class="permission-item">
            <span class="permission-name">是否学生</span>
            <span class="permission-status" :class="userStore.hasRole('student') ? 'granted' : 'denied'">
              {{ userStore.hasRole('student') ? '是' : '否' }}
            </span>
          </div>
        </div>
        </div>
      </div>
      
      <!-- API测试 -->
      <div class="debug-section">
        <h2>API权限测试</h2>
        <div class="api-test">
          <div class="test-api-buttons">
            <el-button type="primary" @click="testAllAPIs">测试所有API</el-button>
            <el-button type="info" @click="testAPI('/api/exams/', 'GET')">测试试卷API</el-button>
            <el-button type="info" @click="testAPI('/api/exams/?student=true', 'GET')">测试我的试卷</el-button>
            <el-button type="info" @click="testAPI('/api/students/', 'GET')">测试学员API</el-button>
            <el-button type="info" @click="testAPI('/api/exam-assignments/', 'GET')">测试考试分配API</el-button>
            <el-button type="info" @click="testAPI('/auth/me', 'GET')">测试用户信息API</el-button>
            <el-button type="info" @click="testAPI('/api/exam-sessions/', 'GET')">测试考试会话API</el-button>
            <el-button type="info" @click="testExamAssignmentValidation">测试考试分配验证</el-button>
          </div>
          <div class="api-test-results">
            <div v-for="result in apiTestResults" :key="result.id" class="api-test-result" :class="{ 'success': result.status === 200, 'error': result.status >= 400 }">
              <h3>{{ result.api }} - {{ result.method }}</h3>
              <p><strong>状态码:</strong> {{ result.status }}</p>
              <p><strong>请求头:</strong></p>
              <pre>{{ JSON.stringify(result.requestHeaders || {}, null, 2) }}</pre>
              <p><strong>响应数据:</strong></p>
              <pre>{{ JSON.stringify(result.data, null, 2) }}</pre>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 操作按钮 -->
      <div class="debug-section">
        <h2>操作工具</h2>
        <div class="action-buttons">
          <el-button type="primary" @click="openExamManagement">打开试卷管理</el-button>
          <el-button type="warning" @click="clearLocalStorage">清除LocalStorage</el-button>
          <el-button type="danger" @click="forceLogin">强制登录测试</el-button>
          <el-button @click="refreshPermissions">刷新权限信息</el-button>
        </div>
      </div>
      
      <!-- 调试日志 -->
      <div class="debug-section">
        <h2>调试日志</h2>
        <div class="debug-logs">
          <div v-for="log in logs" :key="log.id" class="log-item" :class="log.type">
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
import { PERMISSIONS, ROLES, PERMISSION_GROUPS } from '@/utils/permission'

export default {
  name: 'PermissionDebug',
  setup() {
    const userStore = useUserStore()
    const router = useRouter()
    const logs = ref([])
    const apiTestResults = ref([])
    const userPermissions = ref({})
    let logId = 0
    let resultId = 0
    
    // 计算属性
    const isAuthenticated = computed(() => userStore.isAuthenticated)
    const userInfo = computed(() => userStore.userInfo)
    const accessToken = computed(() => getAccessToken())
    const hasAccessToken = computed(() => !!accessToken.value)
    
    // 添加日志
    const addLog = (message, type = 'info') => {
      const time = new Date().toLocaleString()
      logs.value.unshift({
        id: logId++,
        time,
        message,
        type
      })
      console.log(`[${type.toUpperCase()}] [${time}] ${message}`)
    }
    
    // 刷新权限信息
    const refreshPermissions = () => {
      addLog('刷新用户权限信息')
      
      if (!userStore.isAuthenticated) {
        userPermissions.value = {}
        addLog('用户未登录，无法获取权限信息', 'warning')
        return
      }
      
      // 检查所有权限
      const permissions = {}
      Object.keys(PERMISSIONS).forEach(key => {
        permissions[key] = userStore.hasPermission(PERMISSIONS[key])
      })
      
      // 添加特殊API权限检查
      permissions['can_access_exams_api'] = userStore.hasPermission(PERMISSIONS.VIEW_EXAMS)
      permissions['can_access_students_api'] = userStore.hasPermission(PERMISSIONS.VIEW_STUDENTS)
      permissions['is_admin'] = userStore.hasRole('admin')
      permissions['is_teacher'] = userStore.hasRole('teacher')
      permissions['is_student'] = userStore.hasRole('student')
      
      userPermissions.value = permissions
      addLog('权限信息刷新完成')
    }
    
    // 测试单个API
    const testAPI = async (apiPath, method = 'GET') => {
      const apiName = apiPath
      addLog(`开始测试API: ${method} ${apiName}`)
      
      try {
        // 获取实际的token和请求头
        const authToken = localStorage.getItem('access_token')
        const requestHeaders = {
          'Authorization': authToken ? `Bearer ${authToken}` : '未设置',
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
        
        // 发送请求
        let response
        switch (method.toUpperCase()) {
          case 'GET':
            response = await api.get(apiName)
            break
          case 'POST':
            response = await api.post(apiName, {})
            break
          case 'PUT':
            response = await api.put(apiName, {})
            break
          case 'DELETE':
            response = await api.delete(apiName)
            break
          default:
            response = await api.get(apiName)
        }
        
        // 记录结果
        const result = {
          id: resultId++,
          api: apiName,
          method: method,
          status: response.status,
          data: response.data,
          requestHeaders: requestHeaders
        }
        
        apiTestResults.value.unshift(result)
        addLog(`API请求成功: ${method} ${apiName}, 状态码: ${response.status}`, 'success')
        ElMessage.success(`${apiName} 测试成功`)
        
      } catch (error) {
        // 记录错误结果
        const authToken = localStorage.getItem('access_token')
        const requestHeaders = {
          'Authorization': authToken ? `Bearer ${authToken}` : '未设置',
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
        
        const result = {
          id: resultId++,
          api: apiName,
          method: method,
          status: error.response?.status || 0,
          data: error.response?.data || { error: error.message },
          requestHeaders: requestHeaders
        }
        
        apiTestResults.value.unshift(result)
        addLog(`API请求失败: ${method} ${apiName}, 状态码: ${error.response?.status || '未知'}`, 'error')
        addLog(`错误信息: ${error.message}`, 'error')
        ElMessage.error(`${apiName} 测试失败: ${error.response?.status || '未知错误'}`)
      }
    }
    
    // 测试考试分配验证
    const testExamAssignmentValidation = async () => {
      addLog('开始测试考试分配验证流程', 'info')
      
      try {
        // 1. 首先获取当前用户信息
        const userInfoResponse = await api.get('/auth/me')
        addLog(`获取用户信息成功: ${userInfoResponse.data.username} (角色: ${userInfoResponse.data.role})`, 'success')
        
        // 2. 获取用户的考试分配
        const assignmentsResponse = await api.get('/api/exam-assignments/')
        addLog(`获取考试分配成功，共 ${assignmentsResponse.data.length || 0} 个分配`, 'success')
        
        // 3. 检查是否有激活的考试分配
        const activeAssignments = assignmentsResponse.data.filter(assignment => assignment.is_active)
        addLog(`找到 ${activeAssignments.length} 个激活的考试分配`, 'info')
        
        // 4. 测试获取我的试卷
        const myExamsResponse = await api.get('/api/exams/?student=true')
        addLog(`获取我的试卷成功，共 ${myExamsResponse.data.length || 0} 份试卷`, 'success')
        
        // 5. 测试考试会话
        const sessionsResponse = await api.get('/api/exam-sessions/')
        addLog(`获取考试会话成功，共 ${sessionsResponse.data.length || 0} 个会话`, 'success')
        
        // 6. 总结
        let summary = '考试分配验证总结：\n'
        summary += `- 用户角色: ${userInfoResponse.data.role}\n`
        summary += `- 总分配数: ${assignmentsResponse.data.length || 0}\n`
        summary += `- 激活分配数: ${activeAssignments.length}\n`
        summary += `- 可用试卷数: ${myExamsResponse.data.length || 0}\n`
        summary += `- 会话数: ${sessionsResponse.data.length || 0}\n`
        
        if (activeAssignments.length === 0) {
          summary += '\n⚠️ 警告: 没有找到激活的考试分配，这可能是导致403错误的原因。'
          addLog(summary, 'warning')
          ElMessage.warning('未找到激活的考试分配，请联系管理员获取访问权限')
        } else {
          summary += '\n✅ 考试分配验证通过，您有激活的考试权限。'
          addLog(summary, 'success')
          ElMessage.success('考试分配验证通过')
        }
        
        // 将详细结果添加到API测试结果中
        const validationResult = {
          id: resultId++,
          api: '考试分配验证',
          method: 'VALIDATE',
          status: 200,
          data: {
            userInfo: userInfoResponse.data,
            assignments: assignmentsResponse.data,
            activeAssignments: activeAssignments,
            myExams: myExamsResponse.data,
            sessions: sessionsResponse.data,
            summary: summary
          },
          requestHeaders: {
            'Authorization': `Bearer ${localStorage.getItem('access_token') || '未设置'}`
          }
        }
        
        apiTestResults.value.unshift(validationResult)
        
      } catch (error) {
        addLog(`考试分配验证失败: ${error.message}`, 'error')
        addLog(`错误详情: ${JSON.stringify(error.response?.data || {}, null, 2)}`, 'error')
        ElMessage.error('考试分配验证失败，请查看日志获取详细信息')
        
        // 记录错误结果
        const errorResult = {
          id: resultId++,
          api: '考试分配验证',
          method: 'VALIDATE',
          status: error.response?.status || 0,
          data: {
            error: error.message,
            details: error.response?.data
          },
          requestHeaders: {
            'Authorization': `Bearer ${localStorage.getItem('access_token') || '未设置'}`
          }
        }
        
        apiTestResults.value.unshift(errorResult)
      }
    }
    
    // 测试所有API
    const testAllAPIs = async () => {
      addLog('开始测试所有API', 'info')
      
      const apisToTest = [
        { path: '/api/exams/', method: 'GET' },
        { path: '/api/exams/?student=true', method: 'GET' },
        { path: '/api/students/', method: 'GET' },
        { path: '/api/exam-assignments/', method: 'GET' },
        { path: '/auth/me', method: 'GET' },
        { path: '/api/users/', method: 'GET' },
        { path: '/api/exam-sessions/', method: 'GET' }
      ]
      
      for (const apiInfo of apisToTest) {
        await testAPI(apiInfo.path, apiInfo.method)
        // 延迟100ms，避免请求过快
        await new Promise(resolve => setTimeout(resolve, 100))
      }
      
      addLog('所有API测试完成', 'info')
    }
    
    // 清除LocalStorage
    const clearLocalStorage = () => {
      addLog('清除LocalStorage内容')
      localStorage.clear()
      userStore.logout()
      addLog('LocalStorage已清除，用户已登出', 'warning')
      ElMessage.warning('LocalStorage已清除')
    }
    
    // 强制登录测试
    const forceLogin = () => {
      addLog('执行强制登录测试')
      
      // 模拟用户信息
      const mockUser = {
        id: 1,
        username: 'admin_test',
        role: 'admin',
        email: 'admin@example.com'
      }
      
      // 模拟token
      const mockToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEsInVzZXJuYW1lIjoiYWRtaW4iLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MzA3NjQ4MDB9.mock_signature'
      
      // 设置本地存储
      localStorage.setItem('user', JSON.stringify(mockUser))
      localStorage.setItem('access_token', mockToken)
      
      // 更新用户状态
      setUserInfo(mockUser)
      setAccessToken(mockToken)
      userStore.initUser()
      
      addLog('强制登录成功，使用模拟管理员账户', 'success')
      ElMessage.success('强制登录成功')
      
      // 刷新权限信息
      refreshPermissions()
    }
    
    // 打开试卷管理页面
    const openExamManagement = () => {
      addLog('打开试卷管理页面')
      router.push('/exam-management')
    }
    
    // 初始化
    onMounted(() => {
      addLog('权限调试工具已加载')
      refreshPermissions()
    })
    
    return {
      isAuthenticated,
      userInfo,
      accessToken,
      hasAccessToken,
      logs,
      apiTestResults,
      userPermissions,
      addLog,
      testAPI,
      testAllAPIs,
      testExamAssignmentValidation,
      clearLocalStorage,
      forceLogin,
      openExamManagement,
      refreshPermissions
    }
  }
}
</script>

<style scoped>
.permission-debug-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  color: #1890ff;
  margin-bottom: 20px;
}

.debug-sections {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.debug-section {
  background: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.debug-section h2 {
  color: #333;
  font-size: 18px;
  margin-bottom: 16px;
  border-bottom: 1px solid #eee;
  padding-bottom: 8px;
}

.status-info p,
.permissions-list .permission-item {
  margin: 8px 0;
  padding: 4px 0;
}

.permissions-list {
  max-height: 300px;
  overflow-y: auto;
}

.permission-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.permission-name {
  font-weight: 500;
}

.permission-value {
  font-weight: bold;
}

.permission-value.has-permission {
  color: #52c41a;
}

.permission-value:not(.has-permission) {
  color: #ff4d4f;
}

.test-api-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 16px;
}

.api-test-results {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 500px;
  overflow-y: auto;
}

.api-test-result {
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  padding: 12px;
  transition: all 0.3s;
}

.api-test-result.success {
  border-color: #52c41a;
  background-color: #f6ffed;
}

.api-test-result.error {
  border-color: #ff4d4f;
  background-color: #fff2f0;
}

.api-test-result h3 {
  font-size: 16px;
  margin-bottom: 8px;
  color: #333;
}

.api-test-result pre {
  background: #f5f5f5;
  padding: 8px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 14px;
  margin: 4px 0;
}

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.debug-logs {
  max-height: 300px;
  overflow-y: auto;
  background: #f5f5f5;
  padding: 12px;
  border-radius: 4px;
}

.log-item {
  display: flex;
  gap: 10px;
  padding: 4px 0;
  border-bottom: 1px solid #e8e8e8;
}

.log-item:last-child {
  border-bottom: none;
}

.log-time {
  color: #8c8c8c;
  font-size: 12px;
  min-width: 120px;
}

.log-item.error .log-message {
  color: #ff4d4f;
}

.log-item.success .log-message {
  color: #52c41a;
}

.log-item.warning .log-message {
  color: #faad14;
}
</style>