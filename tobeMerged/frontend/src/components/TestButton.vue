<template>
  <div class="test-page">
    <h1>按钮功能测试页面</h1>
    
    <div class="test-buttons">
      <!-- 测试原生按钮直接跳转 -->
      <button class="test-button" onclick="console.log('原生按钮点击 - 学员系统'); window.location.href='/student-login'">
        测试跳转到学员登录页面
      </button>
      
      <button class="test-button" onclick="console.log('原生按钮点击 - 管理员系统'); window.location.href='/admin'">
        测试跳转到管理员页面
      </button>
      
      <!-- 测试添加随机参数，防止缓存 -->
      <button class="test-button" onclick="console.log('带随机参数跳转'); window.location.href='/student-login?t=' + Date.now()">
        带随机参数跳转到学员登录页面
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TestButton'
}
</script>

<style scoped>
.test-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f5f7fa;
}

.test-buttons {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.test-button {
  padding: 15px 30px;
  font-size: 16px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.test-button:hover {
  background-color: #66b1ff;
}
</style>