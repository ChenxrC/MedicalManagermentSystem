<template>
  <div class="top-navigation">
    <el-menu 
      :default-active="activeIndex" 
      mode="horizontal" 
      router
      background-color="#ffffff"
      text-color="#303133"
      active-text-color="#409eff"
      border-bottom="1px solid #e4e7ed"
    >
      <el-menu-item index="/" class="brand-item">
        <el-icon><School /></el-icon>
        <span>教育管理系统</span>
      </el-menu-item>
      
      <!-- 主要导航链接 -->
      <el-menu-item index="/documents" v-if="isAuthenticated">
        <el-icon><Document /></el-icon>
        <span>文档中心</span>
      </el-menu-item>
      
      <!-- 管理员入口 -->
      <el-menu-item index="/admin" v-if="userRole === 'admin'">
        <el-icon><Setting /></el-icon>
        <span>管理中心</span>
      </el-menu-item>
      
      <!-- 学员入口 -->
      <el-menu-item index="/student-exams" v-if="userRole === 'student'">
        <el-icon><Reading /></el-icon>
        <span>学习中心</span>
      </el-menu-item>
      
      <!-- 用户部分 -->
      <div class="user-section">
        <!-- 未登录状态 -->
        <template v-if="!isAuthenticated">
          <el-button type="text" @click="goToLogin" class="nav-button">
            <el-icon><User /></el-icon>
            登录
          </el-button>
          <el-button type="primary" @click="goToRegister" class="nav-button">
            注册
          </el-button>
        </template>
        
        <!-- 已登录状态 -->
        <template v-else>
          <span class="username">{{ currentUser?.username || '用户' }}</span>
          <el-button type="text" @click="handleLogout" class="logout-btn">
            <el-icon><SwitchButton /></el-icon>
            退出登录
          </el-button>
        </template>
      </div>
    </el-menu>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { School, Document, Setting, Reading, User, SwitchButton } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/userStore'

export default {
  name: 'TopNavigation',
  components: {
    School,
    Document,
    Setting,
    Reading,
    User,
    SwitchButton
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const userStore = useUserStore()
    
    const activeIndex = computed(() => {
      return route.path
    })

    const isAuthenticated = computed(() => {
      return userStore.isAuthenticated
    })

    const currentUser = computed(() => {
      return userStore.userInfo
    })

    const userRole = computed(() => {
      return currentUser.value?.role || ''
    })

    const goToLogin = () => {
      router.push('/login')
    }

    const goToRegister = () => {
      // 如果注册页面不存在，可以根据项目实际情况处理
      router.push('/login?mode=register')
    }

    const handleLogout = async () => {
      try {
        await ElMessageBox.confirm(
          '确定要退出登录吗？',
          '提示',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
          }
        )
        
        // 清除用户信息
        userStore.logout()
        ElMessage.success('已退出登录')
        router.push('/')
      } catch {
        // 用户取消退出
      }
    }

    // 初始化用户状态
    onMounted(() => {
      userStore.initUser()
    })

    return {
      activeIndex,
      isAuthenticated,
      currentUser,
      userRole,
      goToLogin,
      goToRegister,
      handleLogout
    }
  }
}
</script>

<style scoped>
.top-navigation {
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.brand-item {
  font-weight: bold;
  font-size: 18px;
}

.brand-item .el-icon {
  font-size: 24px;
  margin-right: 8px;
}

.user-section {
  float: right;
  display: flex;
  align-items: center;
  height: 60px;
  padding: 0 20px;
}

.username {
  color: #606266;
  margin-right: 15px;
  font-size: 14px;
}

.nav-button {
  margin-right: 10px;
}

.logout-btn {
  color: #606266;
  border: none;
  background: none;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.logout-btn .el-icon {
  margin-right: 5px;
}

@media (max-width: 768px) {
  .user-section {
    padding: 0 10px;
  }
  
  .username {
    display: none;
  }
  
  .brand-item span {
    display: none;
  }
}
</style>