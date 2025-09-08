<template>
  <div class="simple-login-test">
    <div class="test-container">
      <h2>简单登录测试</h2>
      
      <!-- 直接使用v-model，不添加额外事件 -->
      <div class="input-group">
        <label>用户名 (v-model only):</label>
        <el-input 
          v-model="username" 
          placeholder="请输入用户名"
        />
        <p>当前值: {{ username }}</p>
      </div>

      <div class="input-group">
        <label>密码 (v-model only):</label>
        <el-input 
          v-model="password" 
          type="password"
          placeholder="请输入密码"
        />
        <p>当前值: {{ password ? '已输入' : '未输入' }}</p>
      </div>

      <!-- 使用事件处理 -->
      <div class="input-group">
        <label>用户名 (with events):</label>
        <el-input 
          v-model="username2" 
          placeholder="请输入用户名"
          @input="onInput"
          @focus="onFocus"
          @blur="onBlur"
        />
        <p>当前值: {{ username2 }}</p>
      </div>

      <div class="input-group">
        <label>密码 (with events):</label>
        <el-input 
          v-model="password2" 
          type="password"
          placeholder="请输入密码"
          @input="onInput"
          @focus="onFocus"
          @blur="onBlur"
        />
        <p>当前值: {{ password2 ? '已输入' : '未输入' }}</p>
      </div>

      <el-button @click="clearAll">清空所有</el-button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'SimpleLoginTest',
  setup() {
    const username = ref('')
    const password = ref('')
    const username2 = ref('')
    const password2 = ref('')

    const onInput = (value) => {
      console.log('输入事件:', value)
    }

    const onFocus = () => {
      console.log('获得焦点')
    }

    const onBlur = () => {
      console.log('失去焦点')
    }

    const clearAll = () => {
      username.value = ''
      password.value = ''
      username2.value = ''
      password2.value = ''
    }

    return {
      username,
      password,
      username2,
      password2,
      onInput,
      onFocus,
      onBlur,
      clearAll
    }
  }
}
</script>

<style scoped>
.simple-login-test {
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

.input-group {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
}

.input-group label {
  display: block;
  margin-bottom: 10px;
  color: #303133;
  font-weight: bold;
}

.input-group .el-input {
  margin-bottom: 10px;
}

.input-group p {
  margin: 5px 0;
  color: #606266;
  font-size: 14px;
}
</style>
