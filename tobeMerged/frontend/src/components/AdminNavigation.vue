<template>
  <div class="admin-navigation">
    <el-menu 
      :default-active="activeIndex" 
      mode="horizontal" 
      router
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b"
    >
      <el-menu-item index="/admin">
        <el-icon><Setting /></el-icon>
        <span>管理首页</span>
      </el-menu-item>
      
      <el-menu-item index="/admin/users">
        <el-icon><User /></el-icon>
        <span>用户管理</span>
      </el-menu-item>
      
      <el-menu-item index="/admin/students">
        <el-icon><Users /></el-icon>
        <span>学员管理</span>
      </el-menu-item>
      
      <el-menu-item index="/admin/exams">
        <el-icon><Document /></el-icon>
        <span>试卷管理</span>
      </el-menu-item>
      
      <el-menu-item index="/admin/assignments">
        <el-icon><Connection /></el-icon>
        <span>试卷分配</span>
      </el-menu-item>
      
      <el-menu-item index="/admin/permissions" v-if="currentUser?.role === 'admin'">
        <el-icon><Key /></el-icon>
        <span>权限管理</span>
      </el-menu-item>
      
      <div class="user-section">
        <span class="username">{{ currentUser?.username || '管理员' }}</span>
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
import { Setting, User, Users, Document, Connection, SwitchButton, Key } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/userStore'

export default {
  name: 'AdminNavigation',
  components: {
    Setting,
    User,
    Users,
    Document,
    Connection,
    SwitchButton
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
          '确定要退出管理系统吗？',
          '确认退出',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        userStore.logout()
        ElMessage.success('已退出管理系统')
        router.push('/')
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('退出失败')
        }
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
.admin-navigation {
  position: sticky;
  top: 0;
  z-index: 1000;
}

.user-section {
  float: right;
  display: flex;
  align-items: center;
  height: 60px;
  padding: 0 20px;
}

.username {
  color: #fff;
  margin-right: 15px;
  font-size: 14px;
}

.logout-btn {
  color: #fff;
  border: none;
  background: none;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
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
}
</style>
