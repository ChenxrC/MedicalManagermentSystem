<template>
  <div class="student-navigation">
    <el-menu 
      :default-active="activeIndex" 
      mode="horizontal" 
      router
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b"
    >
      <el-menu-item index="/student-exams">
        <el-icon><Document /></el-icon>
        <span>我的考试</span>
      </el-menu-item>
      
      <el-menu-item index="/student-courses">
        <el-icon><Reading /></el-icon>
        <span>我的课程</span>
      </el-menu-item>
      
      <el-menu-item index="/scores">
        <el-icon><Trophy /></el-icon>
        <span>我的成绩</span>
      </el-menu-item>
      
      <el-menu-item index="/wrong-analysis">
        <el-icon><Warning /></el-icon>
        <span>错题分析</span>
      </el-menu-item>
      
      <el-menu-item index="/account">
        <el-icon><User /></el-icon>
        <span>账户管理</span>
      </el-menu-item>
      
      <div class="user-section">
        <span class="username">{{ currentUser?.username || '学员' }}</span>
        <el-button type="text" @click="handleLogout" class="logout-btn">
          <el-icon><SwitchButton /></el-icon>
          退出登录
        </el-button>
      </div>
    </el-menu>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document, Trophy, Warning, User, SwitchButton, Reading } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/userStore'

export default {
  name: 'StudentNavigation',
  components: {
    Document,
    Trophy,
    Warning,
    User,
    SwitchButton,
    Reading
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const userStore = useUserStore()
    
    const activeIndex = computed(() => {
      return route.path
    })

    const currentUser = computed(() => userStore.userInfo)

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
        
        userStore.logout()
        ElMessage.success('已退出登录')
        router.push('/')
      } catch {
        // 用户取消退出
      }
    }

    return {
      activeIndex,
      currentUser,
      handleLogout
    }
  }
}
</script>

<style scoped>
.student-navigation {
  margin-bottom: 20px;
}

.el-menu {
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  justify-content: space-between;
}

.el-menu-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.el-menu-item .el-icon {
  margin-right: 4px;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 0 20px;
  color: #fff;
}

.username {
  font-size: 14px;
  color: #ffd04b;
}

.logout-btn {
  color: #fff;
  border: none;
  background: transparent;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
}

.logout-btn:hover {
  color: #ffd04b;
  background: rgba(255, 255, 255, 0.1);
}
</style>
