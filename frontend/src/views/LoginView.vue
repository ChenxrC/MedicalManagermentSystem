<template>
  <div class="login page-container">
    <el-card class="login-card enhanced-card">
      <div slot="header" class="clearfix">
        <span>用户登录</span>
      </div>
      <el-form :model="loginForm" :rules="rules" ref="loginForm" label-width="80px" class="enhanced-form">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin" :loading="loading" class="enhanced-button">登录</el-button>
          <el-button @click="handleRegister" class="enhanced-button">注册</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { login, setUserInfo, setAccessToken } from '@/services/auth'

export default {
  name: 'LoginView',
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      },
      loading: false
    }
  },
  methods: {
    async handleLogin() {
      this.$refs.loginForm.validate(async (valid) => {
        if (valid) {
          this.loading = true
          try {
            const response = await login(this.loginForm)
            const { access_token, user } = response.data
            
            // 保存访问令牌和用户信息
            setAccessToken(access_token)
            setUserInfo(user)
            
            // 显示成功消息
            this.$message.success('登录成功')
            
            // 发送自定义事件通知认证状态变化
            window.dispatchEvent(new Event('auth-status-changed'))
            
            // 登录成功后跳转到首页
            this.$router.push('/');
          } catch (error) {
            // 显示错误消息
            this.$message.error(error.response?.data?.message || '登录失败')
          } finally {
            this.loading = false
          }
        } else {
          console.log('表单验证失败')
          return false
        }
      })
    },
    handleRegister() {
      this.$router.push('/register')
    }
  }
}
</script>

<style scoped>
.login {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.login-card {
  width: 400px;
}
</style>