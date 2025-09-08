<template>
  <div class="login-test">
    <div class="test-container">
      <h2>登录输入框测试</h2>
      
      <!-- 原生HTML输入框测试 -->
      <div class="test-section">
        <h3>原生HTML输入框测试</h3>
        <input 
          v-model="nativeUsername" 
          type="text" 
          placeholder="原生用户名输入框"
          @input="onNativeInput"
          @focus="onNativeFocus"
          @blur="onNativeBlur"
        />
        <input 
          v-model="nativePassword" 
          type="password" 
          placeholder="原生密码输入框"
          @input="onNativeInput"
          @focus="onNativeFocus"
          @blur="onNativeBlur"
        />
      </div>

      <!-- Element Plus输入框测试 -->
      <div class="test-section">
        <h3>Element Plus输入框测试</h3>
        <el-input 
          v-model="elementUsername" 
          placeholder="Element Plus用户名输入框"
          @input="onElementInput"
          @focus="onElementFocus"
          @blur="onElementBlur"
        />
        <el-input 
          v-model="elementPassword" 
          type="password"
          placeholder="Element Plus密码输入框"
          @input="onElementInput"
          @focus="onElementFocus"
          @blur="onElementBlur"
        />
      </div>

      <!-- 调试信息 -->
      <div class="debug-info">
        <h3>调试信息</h3>
        <p>原生用户名: {{ nativeUsername }}</p>
        <p>原生密码: {{ nativePassword ? '已输入' : '未输入' }}</p>
        <p>Element用户名: {{ elementUsername }}</p>
        <p>Element密码: {{ elementPassword ? '已输入' : '未输入' }}</p>
      </div>

      <el-button @click="clearAll">清空所有</el-button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'StudentLoginTest',
  setup() {
    const nativeUsername = ref('')
    const nativePassword = ref('')
    const elementUsername = ref('')
    const elementPassword = ref('')

    const onNativeInput = (event) => {
      console.log('原生输入事件:', event.target.value, event.target.type)
    }

    const onNativeFocus = (event) => {
      console.log('原生获得焦点:', event.target.type)
    }

    const onNativeBlur = (event) => {
      console.log('原生失去焦点:', event.target.type)
    }

    const onElementInput = (value) => {
      console.log('Element输入事件:', value)
    }

    const onElementFocus = () => {
      console.log('Element获得焦点')
    }

    const onElementBlur = () => {
      console.log('Element失去焦点')
    }

    const clearAll = () => {
      nativeUsername.value = ''
      nativePassword.value = ''
      elementUsername.value = ''
      elementPassword.value = ''
    }

    return {
      nativeUsername,
      nativePassword,
      elementUsername,
      elementPassword,
      onNativeInput,
      onNativeFocus,
      onNativeBlur,
      onElementInput,
      onElementFocus,
      onElementBlur,
      clearAll
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

.test-section input,
.test-section .el-input {
  margin-bottom: 15px;
  width: 100%;
}

.test-section input {
  padding: 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.test-section input:focus {
  outline: none;
  border-color: #409eff;
}

.debug-info {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.debug-info h3 {
  margin-bottom: 15px;
  color: #303133;
}

.debug-info p {
  margin: 5px 0;
  color: #606266;
}
</style>
