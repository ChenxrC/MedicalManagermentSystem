<template>
  <div class="register-container">
    <div class="register-form-wrapper">
      <h2>用户注册</h2>
      <el-form ref="registerForm" :model="registerForm" :rules="registerRules" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="registerForm.email" placeholder="请输入邮箱"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="registerForm.password" type="password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="registerForm.confirmPassword" type="password" placeholder="请确认密码"></el-input>
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="registerForm.role" placeholder="请选择角色">
            <el-option label="学生" value="STUDENT"></el-option>
            <el-option label="教师" value="TEACHER"></el-option>
            <el-option label="管理员" value="ADMIN"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleRegister" :loading="loading">注册</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { defineComponent } from 'vue'
import { register } from '@/utils/auth'

export default defineComponent({
  name: 'RegisterView',
  setup() {
    const router = useRouter()
    const registerForm = {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      role: 'STUDENT' // 默认角色为学生
    }
    const loading = false
    const errorMessage = ''
    
    const registerRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度至少为 6 个字符', trigger: 'blur' }
      ],
      confirmPassword: [
        { required: true, message: '请确认密码', trigger: 'blur' },
        {
          validator: (rule, value, callback) => {
            if (value !== this.registerForm.password) {
              callback(new Error('两次输入的密码不一致'))
            } else {
              callback()
            }
          },
          trigger: 'blur'
        }
      ],
      role: [
        { required: true, message: '请选择角色', trigger: 'change' }
      ]
    }
    
    const handleRegister = async () => {
      const registerFormRef = this.$refs.registerForm
      registerFormRef.validate(async (valid) => {
        if (valid) {
          this.loading = true
          this.errorMessage = ''
          
          try {
            const userData = {
              username: this.registerForm.username,
              email: this.registerForm.email,
              password: this.registerForm.password,
              role: this.registerForm.role
            }
            
            const response = await register(userData)
            
            ElMessage.success('注册成功，请登录')
            // 注册成功后跳转到登录页
            router.push('/login')
          } catch (error) {
            console.error('注册失败:', error)
            this.errorMessage = '注册失败，请稍后重试'
          } finally {
            this.loading = false
          }
        }
      })
    }
    
    const resetForm = () => {
      this.$refs.registerForm.resetFields()
      this.errorMessage = ''
    }
    
    return {
      registerForm,
      loading,
      errorMessage,
      registerRules,
      handleRegister,
      resetForm
    }
  }
})
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.register-form-wrapper {
  width: 500px;
  padding: 30px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.register-form-wrapper h2 {
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