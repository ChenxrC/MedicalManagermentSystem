<template>
  <div class="admin-dashboard">
    <div class="header">
      <h1>管理中心</h1>
      <p>欢迎回来，管理员！</p>
    </div>
    
    <div class="dashboard-cards">
      <!-- 用户管理卡片 -->
      <el-card class="dashboard-card">
        <div slot="header" class="card-header">
          <span>用户管理</span>
        </div>
        <div class="card-content">
          <el-icon><User /></el-icon>
          <p>管理系统用户、角色和权限</p>
          <el-button type="primary" @click="goToUserManagement" class="card-button">
            进入管理
          </el-button>
        </div>
      </el-card>
      
      <!-- 考试管理卡片 -->
      <el-card class="dashboard-card">
        <div slot="header" class="card-header">
          <span>考试管理</span>
        </div>
        <div class="card-content">
          <el-icon><Reading /></el-icon>
          <p>创建和管理考试试卷、题库</p>
          <el-button type="primary" @click="goToExamManagement" class="card-button">
            进入管理
          </el-button>
        </div>
      </el-card>
      
      <!-- 文档管理卡片 -->
      <el-card class="dashboard-card">
        <div slot="header" class="card-header">
          <span>文档管理</span>
        </div>
        <div class="card-content">
          <el-icon><Document /></el-icon>
          <p>管理系统文档和学习资料</p>
          <el-button type="primary" @click="goToDocumentManagement" class="card-button">
            进入管理
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { User, Reading, Document } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

export default {
  name: 'AdminDashboard',
  components: {
    User,
    Reading,
    Document
  },
  setup() {
    const router = useRouter()
    
    const goToUserManagement = () => {
      // 假设用户管理页面的路由是 /admin/users
      // 如果该页面不存在，可以显示提示并跳转到首页
      try {
        router.push('/admin/users')
      } catch (error) {
        ElMessage.warning('用户管理功能正在开发中')
      }
    }
    
    const goToExamManagement = () => {
      // 假设考试管理页面的路由是 /admin/exams
      try {
        router.push('/admin/exams')
      } catch (error) {
        ElMessage.warning('考试管理功能正在开发中')
      }
    }
    
    const goToDocumentManagement = () => {
      // 假设文档管理页面的路由是 /admin/documents
      try {
        router.push('/admin/documents')
      } catch (error) {
        ElMessage.warning('文档管理功能正在开发中')
      }
    }
    
    return {
      goToUserManagement,
      goToExamManagement,
      goToDocumentManagement
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
}

.header {
  margin-bottom: 30px;
  text-align: center;
}

.header h1 {
  font-size: 28px;
  margin-bottom: 10px;
}

.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.dashboard-card {
  height: 200px;
  display: flex;
  flex-direction: column;
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.card-content .el-icon {
  font-size: 48px;
  margin-bottom: 15px;
  color: #409eff;
}

.card-content p {
  margin-bottom: 20px;
  color: #606266;
}

.card-button {
  width: 120px;
}
</style>