<template>
  <div class="admin-center">
    <AdminNavigation />
    <div class="admin-content">
      <div class="page-header">
        <h1>管理员中心</h1>
        <div class="user-info">
          <span>欢迎，{{ currentUser?.first_name || currentUser?.username }}</span>
          <el-button type="primary" size="small" @click="handleLogout">退出登录</el-button>
        </div>
      </div>

      <div class="dashboard-cards">
        <el-card class="dashboard-card">
          <div slot="header" class="clearfix">
            <span>系统概览</span>
          </div>
          <div class="card-content">
            <div class="stats-row">
              <div class="stat-item">
                <div class="stat-number">{{ totalUsers }}</div>
                <div class="stat-label">总用户数</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">{{ totalStudents }}</div>
                <div class="stat-label">学生数</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">{{ totalTeachers }}</div>
                <div class="stat-label">老师数</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">{{ totalAdmins }}</div>
                <div class="stat-label">管理员数</div>
              </div>
            </div>
          </div>
        </el-card>
      </div>

      <div class="admin-functions">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card class="function-card" @click="navigateTo('/admin/users')">
              <div class="function-icon">
                <el-icon><User /></el-icon>
              </div>
              <div class="function-title">用户管理</div>
              <div class="function-desc">查看所有用户并管理用户角色和权限</div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="function-card" @click="navigateTo('/admin/students')">
              <div class="function-icon">
                <el-icon><School /></el-icon>
              </div>
              <div class="function-title">学员管理</div>
              <div class="function-desc">管理学生账户和学习信息</div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="function-card" @click="navigateTo('/admin/exams')">
              <div class="function-icon">
                <el-icon><Document /></el-icon>
              </div>
              <div class="function-title">考试管理</div>
              <div class="function-desc">创建和管理考试内容</div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useRouter } from 'vue-router'
import api from '@/utils/axios'
import { ElMessage } from 'element-plus'
import { User, School, Document } from '@element-plus/icons-vue'
import AdminNavigation from './AdminNavigation.vue'

export default {
  name: 'AdminCenter',
  components: {
    User,
    School,
    Document,
    AdminNavigation
  },
  setup() {
    const userStore = useUserStore()
    const router = useRouter()
    const currentUser = computed(() => userStore.currentUser)
    
    // 系统统计数据
    const totalUsers = ref(0)
    const totalStudents = ref(0)
    const totalTeachers = ref(0)
    const totalAdmins = ref(0)
    
    // 获取系统统计数据
    const fetchSystemStats = async () => {
      try {
        const response = await api.get('/users/')
        const users = response.data.results || response.data
        
        totalUsers.value = users.length
        totalStudents.value = users.filter(user => user.role === 'student').length
        totalTeachers.value = users.filter(user => user.role === 'teacher').length
        totalAdmins.value = users.filter(user => user.role === 'admin').length
      } catch (error) {
        console.error('获取系统统计数据失败:', error)
        ElMessage.error('获取系统统计数据失败')
      }
    }
    
    // 导航到指定路径
    const navigateTo = (path) => {
      router.push(path)
    }
    
    // 退出登录
    const handleLogout = async () => {
      try {
        await userStore.logout()
        router.push('/login')
      } catch (error) {
        console.error('退出登录失败:', error)
        ElMessage.error('退出登录失败')
      }
    }
    
    // 初始化
    onMounted(() => {
      fetchSystemStats()
    })
    
    return {
      currentUser,
      totalUsers,
      totalStudents,
      totalTeachers,
      totalAdmins,
      navigateTo,
      handleLogout
    }
  }
}
</script>

<style scoped>
.admin-center {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.admin-content {
  flex: 1;
  padding: 20px;
  background-color: #f5f7fa;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.dashboard-cards {
  margin-bottom: 30px;
}

.dashboard-card {
    background: #ffffff;
    border: 1px solid #e4e7ed;
    color: #303133;
  }

  .stat-number {
    font-weight: bold;
    color: #000000;
  }

  .stat-label {
    color: #000000;
  }

.card-content {
  padding: 20px 0;
}

.stats-row {
  display: flex;
  justify-content: space-around;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

.admin-functions {
  margin-top: 30px;
}

.function-card {
  height: 100%;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e6e6e6;
}

.function-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.function-icon {
  font-size: 48px;
  color: #667eea;
  margin-bottom: 16px;
  text-align: center;
}

.function-title {
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 8px;
}

.function-desc {
  font-size: 14px;
  color: #606266;
  text-align: center;
}
</style>