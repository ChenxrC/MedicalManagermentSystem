<template>
  <div class="student-login">
    <div class="login-container">
      <div class="login-header">
        <h2>学员登录</h2>
        <p>请输入您的账号信息</p>
      </div>

                           <el-form 
          ref="loginFormRef" 
          :model="{ username, password }" 
          :rules="loginRules" 
          class="login-form"
          @submit.prevent="handleLogin"
        >
        <el-form-item prop="username">
          <el-input
            v-model="username"
            placeholder="请输入用户名"
            size="large"
            clearable
            @input="onUsernameInput"
            @focus="onUsernameFocus"
            @blur="onUsernameBlur"
            @keydown="onUsernameKeydown"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="password"
            type="password"
            placeholder="请输入密码"
            size="large"
            show-password
            clearable
            @input="onPasswordInput"
            @focus="onPasswordFocus"
            @blur="onPasswordBlur"
            @keydown="onPasswordKeydown"
          />
        </el-form-item>

        <el-form-item>
          <el-button 
            type="primary" 
            size="large" 
            class="login-button"
            :loading="loading"
            @click="handleLogin"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>

        <div class="login-options">
          <el-checkbox v-model="rememberMe">记住我</el-checkbox>
          <a href="#" class="forgot-password">忘记密码？</a>
        </div>
      </el-form>

      <div class="login-footer">
        <p>还没有账号？请联系管理员创建账号</p>
        <el-button type="text" @click="goBack">返回首页</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import axios from 'axios'
import { useUserStore } from '@/stores/userStore'

export default {
  name: 'StudentLogin',
  components: {
    User,
    Lock
  },
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    
    // 使用ref而不是reactive，确保响应式更新
    const username = ref('')
    const password = ref('')
    
    const loading = ref(false)
    const rememberMe = ref(false)
    const loginFormRef = ref(null)

    // 登录验证规则
    const loginRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: ['blur', 'change'] },
        { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: ['blur', 'change'] }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: ['blur', 'change'] },
        { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: ['blur', 'change'] }
      ]
    }

    // 处理登录
    const handleLogin = async () => {
      console.log('开始登录流程...')
      console.log('登录表单数据:', { username: username.value, password: password.value })
      
      loading.value = true
      
      try {
        // 简单的输入验证
        if (!username.value || username.value.length < 3) {
          ElMessage.error('用户名至少需要3个字符')
          return
        }
        
        if (!password.value || password.value.length < 6) {
          ElMessage.error('密码至少需要6个字符')
          return
        }
        
        console.log('输入验证通过')
        
        // 由于没有真实的后端API，直接使用模拟登录
        console.log('使用模拟登录...')
        
        // 模拟登录成功
        const mockUser = {
          id: 1,
          username: username.value,
          email: `${username.value}@example.com`,
          token: 'mock_token_' + Date.now()
        }
        
        console.log('保存用户信息:', mockUser)
        
        // 直接设置用户状态，而不是调用login方法
        userStore.currentUser = mockUser
        userStore.token = mockUser.token
        userStore.isLoggedIn = true
        localStorage.setItem('studentUser', JSON.stringify(mockUser))
        
        ElMessage.success('登录成功')
        console.log('准备跳转到学员考试列表...')
        
        // 跳转到学员考试列表
        await router.push('/student-exams')
        console.log('跳转完成')
        
      } catch (error) {
        console.error('登录过程中发生错误:', error)
        ElMessage.error('登录失败，请稍后重试')
      } finally {
        loading.value = false
      }
    }

    // 返回首页
    const goBack = () => {
      router.push('/')
    }

    // 输入框事件处理函数
    const onUsernameInput = (value) => {
      console.log('用户名输入:', value)
      username.value = value
    }

    const onUsernameFocus = () => {
      console.log('用户名输入框获得焦点')
    }

    const onUsernameBlur = () => {
      console.log('用户名输入框失去焦点')
    }

    const onPasswordInput = (value) => {
      console.log('密码输入:', value)
      password.value = value
    }

    const onPasswordFocus = () => {
      console.log('密码输入框获得焦点')
    }

    const onPasswordBlur = () => {
      console.log('密码输入框失去焦点')
    }

    const onUsernameKeydown = (event) => {
      console.log('用户名键盘事件:', event.key, event.target.value)
    }

    const onPasswordKeydown = (event) => {
      console.log('密码键盘事件:', event.key, event.target.value)
    }

    return {
      username,
      password,
      loginRules,
      loading,
      rememberMe,
      loginFormRef,
      handleLogin,
      goBack,
      onUsernameInput,
      onUsernameFocus,
      onUsernameBlur,
      onPasswordInput,
      onPasswordFocus,
      onPasswordBlur,
      onUsernameKeydown,
      onPasswordKeydown
    }
  }
}
</script>

<style scoped>
.student-login {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  color: #303133;
  margin-bottom: 10px;
  font-size: 28px;
}

.login-header p {
  color: #909399;
  margin: 0;
}

.login-form {
  margin-bottom: 20px;
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  border-radius: 8px;
}

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.forgot-password {
  color: #409eff;
  text-decoration: none;
  font-size: 14px;
}

.forgot-password:hover {
  text-decoration: underline;
}

.login-footer {
  text-align: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.login-footer p {
  color: #909399;
  margin-bottom: 15px;
  font-size: 14px;
}

@media (max-width: 480px) {
  .login-container {
    padding: 30px 20px;
  }
  
  .login-header h2 {
    font-size: 24px;
  }
}
</style>
