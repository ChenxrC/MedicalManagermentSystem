<template>
  <div class="form-validation-test">
    <div class="test-container">
      <h2>表单验证测试</h2>
      
      <el-form 
        ref="formRef" 
        :model="formData" 
        :rules="rules" 
        label-width="120px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="formData.username" 
            placeholder="请输入用户名"
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="formData.password" 
            type="password"
            placeholder="请输入密码"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="validateForm">验证表单</el-button>
          <el-button @click="clearForm">清空表单</el-button>
        </el-form-item>
      </el-form>

      <div class="debug-info">
        <h3>调试信息</h3>
        <p>用户名: {{ formData.username || '未输入' }}</p>
        <p>密码: {{ formData.password ? '已输入' : '未输入' }}</p>
        <p>用户名长度: {{ formData.username ? formData.username.length : 0 }}</p>
        <p>密码长度: {{ formData.password ? formData.password.length : 0 }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'FormValidationTest',
  setup() {
    const formRef = ref(null)
    
    const formData = reactive({
      username: '',
      password: ''
    })

    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
      ]
    }

    const validateForm = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value.validate()
        ElMessage.success('表单验证通过！')
        console.log('表单数据:', formData)
      } catch (error) {
        ElMessage.error('表单验证失败！')
        console.log('验证错误:', error)
      }
    }

    const clearForm = () => {
      formData.username = ''
      formData.password = ''
      if (formRef.value) {
        formRef.value.clearValidate()
      }
    }

    return {
      formRef,
      formData,
      rules,
      validateForm,
      clearForm
    }
  }
}
</script>

<style scoped>
.form-validation-test {
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
  max-width: 500px;
}

.debug-info {
  margin-top: 30px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.debug-info h3 {
  margin-bottom: 15px;
  color: #303133;
}

.debug-info p {
  margin: 5px 0;
  color: #606266;
  font-size: 14px;
}
</style>
