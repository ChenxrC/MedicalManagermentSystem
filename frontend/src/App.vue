<template>
  <div id="app">
    <nav>
      <router-link to="/">首页</router-link> |
      <router-link to="/courses">课程管理</router-link> |
      <router-link to="/documents">文档管理</router-link> |
      <router-link to="/exams">考试系统</router-link> |
      <router-link to="/chatbot">知识库问答</router-link>
      <template v-if="!isAuthenticated">
        | <router-link to="/login">登录</router-link> |
        <router-link to="/register">注册</router-link>
      </template>
      <template v-else>
        <el-dropdown @command="handleUserCommand" class="user-dropdown">
          <span class="el-dropdown-link">
            <el-avatar :icon="UserFilled" size="small"></el-avatar>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人资料</el-dropdown-item>
              <el-dropdown-item command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </template>
    </nav>
    <router-view/>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { isAuthenticated as authIsAuthenticated, clearUserInfo } from '@/services/auth'
import { UserFilled } from '@element-plus/icons-vue'

export default {
  name: 'App',
  setup() {
    const router = useRouter()
    const isAuthenticated = ref(false)

    // 检查用户是否已认证
    const checkAuthStatus = () => {
      isAuthenticated.value = authIsAuthenticated()
    }

    // 处理用户命令
    const handleUserCommand = (command) => {
      if (command === 'profile') {
        // 跳转到个人资料页面
        router.push('/profile')
      } else if (command === 'logout') {
        // 清除用户信息并跳转到登录页面
        clearUserInfo()
        isAuthenticated.value = false
        router.push('/login')
      }
    }

    // 在组件挂载时检查认证状态
    onMounted(() => {
      checkAuthStatus()
      
      // 监听认证状态变化事件
      window.addEventListener('auth-status-changed', checkAuthStatus)
    })
    
    // 在组件卸载前移除事件监听器
    onUnmounted(() => {
      window.removeEventListener('auth-status-changed', checkAuthStatus)
    })

    return {
      isAuthenticated,
      handleUserCommand,
      UserFilled
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

.user-dropdown {
  float: right;
  margin-right: 20px;
  margin-top: 10px;
}

.el-dropdown-link {
  cursor: pointer;
  color: #409eff;
}
</style>