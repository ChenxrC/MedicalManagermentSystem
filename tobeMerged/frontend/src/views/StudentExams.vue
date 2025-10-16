<template>
  <div class="student-exams">
    <div class="header">
      <h1>学习中心</h1>
      <p>欢迎回来，继续您的学习之旅！</p>
    </div>
    
    <div class="learning-cards">
      <!-- 我的考试卡片 -->
      <el-card class="learning-card">
        <div slot="header" class="card-header">
          <span>我的考试</span>
        </div>
        <div class="card-content">
          <el-icon><Reading /></el-icon>
          <p>查看和参加已分配的考试</p>
          <el-button type="primary" @click="viewMyExams" class="card-button">
            查看考试
          </el-button>
        </div>
      </el-card>
      
      <!-- 我的课程卡片 -->
      <el-card class="learning-card">
        <div slot="header" class="card-header">
          <span>我的课程</span>
        </div>
        <div class="card-content">
          <el-icon><School /></el-icon>
          <p>访问已报名的课程和学习资料</p>
          <el-button type="primary" @click="viewMyCourses" class="card-button">
            查看课程
          </el-button>
        </div>
      </el-card>
      
      <!-- 学习记录卡片 -->
      <el-card class="learning-card">
        <div slot="header" class="card-header">
          <span>学习记录</span>
        </div>
        <div class="card-content">
          <el-icon><Document /></el-icon>
          <p>查看您的学习进度和历史成绩</p>
          <el-button type="primary" @click="viewLearningRecords" class="card-button">
            查看记录
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { Reading, School, Document } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

export default {
  name: 'StudentExams',
  components: {
    Reading,
    School,
    Document
  },
  setup() {
    const router = useRouter()
    
    const viewMyExams = () => {
      // 假设我的考试页面的路由是 /student/exams/list
      try {
        router.push('/student/exams/list')
      } catch (error) {
        ElMessage.warning('考试列表功能正在开发中')
      }
    }
    
    const viewMyCourses = () => {
      // 假设我的课程页面的路由是 /student/courses
      try {
        router.push('/student/courses')
      } catch (error) {
        ElMessage.warning('课程列表功能正在开发中')
      }
    }
    
    const viewLearningRecords = () => {
      // 假设学习记录页面的路由是 /student/records
      try {
        router.push('/student/records')
      } catch (error) {
        ElMessage.warning('学习记录功能正在开发中')
      }
    }
    
    return {
      viewMyExams,
      viewMyCourses,
      viewLearningRecords
    }
  }
}
</script>

<style scoped>
.student-exams {
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

.learning-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.learning-card {
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