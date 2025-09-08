<template>
  <div class="admin-dashboard">
    <AdminNavigation />
    <div class="dashboard-content">
    <div class="dashboard-header">
      <h1>管理系统</h1>
      <p>欢迎使用在线考试管理系统</p>
    </div>

    <div class="dashboard-stats">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon size="40" color="#409eff"><User /></el-icon>
              </div>
              <div class="stat-info">
                <h3>{{ stats.studentCount }}</h3>
                <p>学员总数</p>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon size="40" color="#67c23a"><Document /></el-icon>
              </div>
              <div class="stat-info">
                <h3>{{ stats.examCount }}</h3>
                <p>试卷总数</p>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon size="40" color="#e6a23c"><Trophy /></el-icon>
              </div>
              <div class="stat-info">
                <h3>{{ stats.activeExamCount }}</h3>
                <p>进行中考试</p>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon size="40" color="#f56c6c"><Warning /></el-icon>
              </div>
              <div class="stat-info">
                <h3>{{ stats.assignmentCount }}</h3>
                <p>试卷分配</p>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="dashboard-sections">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card class="section-card">
            <template #header>
              <div class="card-header">
                <span>学员管理</span>
                <el-button type="primary" size="small" @click="goToStudentManagement">
                  管理学员
                </el-button>
              </div>
            </template>
            <div class="section-content">
              <p>查看和管理系统中的所有学员信息</p>
              <ul>
                <li>查看学员列表</li>
                <li>添加新学员</li>
                <li>编辑学员信息</li>
                <li>删除学员</li>
              </ul>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="12">
          <el-card class="section-card">
            <template #header>
              <div class="card-header">
                <span>试卷管理</span>
                <el-button type="success" size="small" @click="goToExamManagement">
                  管理试卷
                </el-button>
              </div>
            </template>
            <div class="section-content">
              <p>创建和管理考试试卷</p>
              <ul>
                <li>创建新试卷</li>
                <li>编辑现有试卷</li>
                <li>删除试卷</li>
                <li>查看试卷详情</li>
              </ul>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="24">
          <el-card class="section-card">
            <template #header>
              <div class="card-header">
                <span>试卷分配</span>
                <el-button type="warning" size="small" @click="goToAssignmentManagement">
                  分配管理
                </el-button>
              </div>
            </template>
            <div class="section-content">
              <p>为学员分配试卷，建立学员和试卷的多对多关系</p>
              <ul>
                <li>为学员分配试卷</li>
                <li>查看分配关系</li>
                <li>移除试卷分配</li>
                <li>批量分配管理</li>
              </ul>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="dashboard-actions">
      <el-button type="primary" size="large" @click="goToStudentManagement">
        <el-icon><User /></el-icon>
        学员管理
      </el-button>
      <el-button type="success" size="large" @click="goToExamManagement">
        <el-icon><Document /></el-icon>
        试卷管理
      </el-button>
      <el-button type="warning" size="large" @click="goToAssignmentManagement">
        <el-icon><Connection /></el-icon>
        试卷分配
      </el-button>
    </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Document, Trophy, Warning, Connection } from '@element-plus/icons-vue'
import AdminNavigation from './AdminNavigation.vue'

export default {
  name: 'AdminDashboard',
  components: {
    User,
    Document,
    Trophy,
    Warning,
    Connection,
    AdminNavigation
  },
  setup() {
    const router = useRouter()
    
    const stats = ref({
      studentCount: 0,
      examCount: 0,
      activeExamCount: 0,
      assignmentCount: 0
    })

    const loadStats = async () => {
      try {
        // 模拟统计数据
        stats.value = {
          studentCount: 25,
          examCount: 12,
          activeExamCount: 3,
          assignmentCount: 45
        }
      } catch (error) {
        console.error('加载统计数据失败:', error)
        ElMessage.error('加载统计数据失败')
      }
    }

    const goToStudentManagement = () => {
      router.push('/admin/students')
    }

    const goToExamManagement = () => {
      router.push('/admin/exams')
    }

    const goToAssignmentManagement = () => {
      router.push('/admin/assignments')
    }

    onMounted(() => {
      loadStats()
    })

    return {
      stats,
      goToStudentManagement,
      goToExamManagement,
      goToAssignmentManagement
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.dashboard-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 40px;
}

.dashboard-header h1 {
  font-size: 36px;
  color: #1e3a8a;
  margin-bottom: 10px;
}

.dashboard-header p {
  font-size: 16px;
  color: #606266;
}

.dashboard-stats {
  margin-bottom: 40px;
}

.stat-card {
  height: 120px;
}

.stat-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.stat-icon {
  margin-right: 20px;
}

.stat-info h3 {
  font-size: 28px;
  color: #1e3a8a;
  margin: 0 0 5px 0;
}

.stat-info p {
  color: #1e3a8a;
  margin: 0;
}

.dashboard-sections {
  margin-bottom: 40px;
}

.section-card {
  height: 200px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-content p {
  color: #1e3a8a;
  margin-bottom: 15px;
}

.section-content ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.section-content li {
  color: #1e3a8a;
  margin-bottom: 8px;
  padding-left: 20px;
  position: relative;
}

.section-content li::before {
  content: "•";
  color: #409eff;
  position: absolute;
  left: 0;
}

.dashboard-actions {
  text-align: center;
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

.dashboard-actions .el-button {
  min-width: 150px;
}

@media (max-width: 768px) {
  .dashboard-stats .el-col {
    margin-bottom: 20px;
  }
  
  .dashboard-sections .el-col {
    margin-bottom: 20px;
  }
  
  .dashboard-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .dashboard-actions .el-button {
    width: 100%;
    max-width: 300px;
  }
}
</style>
