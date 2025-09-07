<template>
  <div class="home-page">
    <div class="hero-section">
      <h1>在线考试管理系统</h1>
      <p>专业的在线考试平台，支持多种题型，实时评分，视频录制</p>
    </div>

    <div class="role-selection">
      <h2>请选择您的身份</h2>
      
      <div class="role-cards">
        <el-card class="role-card student-card" @click="goToStudent">
          <div class="card-content">
            <div class="icon-container">
              <el-icon size="60" color="#409eff"><User /></el-icon>
            </div>
            <h3>学员入口</h3>
            <p>查看考试列表，参加考试，查看成绩</p>
            <el-button type="primary" size="large">进入学员系统</el-button>
          </div>
        </el-card>

        <el-card class="role-card admin-card" @click="goToAdmin">
          <div class="card-content">
            <div class="icon-container">
              <el-icon size="60" color="#67c23a"><Setting /></el-icon>
            </div>
            <h3>管理员入口</h3>
            <p>创建试卷，管理考试，查看成绩</p>
            <el-button type="success" size="large">进入管理系统</el-button>
          </div>
        </el-card>
      </div>
    </div>

    <div class="features">
      <h2>系统功能</h2>
      <div class="feature-grid">
        <div class="feature-item">
          <el-icon size="40" color="#409eff"><Document /></el-icon>
          <h4>试卷管理</h4>
          <p>支持多种题型，灵活配置试卷</p>
        </div>
        <div class="feature-item">
          <el-icon size="40" color="#67c23a"><VideoCamera /></el-icon>
          <h4>视频录制</h4>
          <p>考试过程全程录制，确保公平</p>
        </div>
        <div class="feature-item">
          <el-icon size="40" color="#e6a23c"><Trophy /></el-icon>
          <h4>自动评分</h4>
          <p>选择题自动评分，提高效率</p>
        </div>
        <div class="feature-item">
          <el-icon size="40" color="#f56c6c"><Warning /></el-icon>
          <h4>错题分析</h4>
          <p>详细的错题分析，帮助学习</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { User, Setting, Document, VideoCamera, Trophy, Warning } from '@element-plus/icons-vue'

export default {
  name: 'HomePage',
  components: {
    User,
    Setting,
    Document,
    VideoCamera,
    Trophy,
    Warning
  },
  setup() {
    const router = useRouter()

    const goToStudent = () => {
      router.push('/student-login')
    }

    const goToAdmin = () => {
      router.push('/admin')
    }

    return {
      goToStudent,
      goToAdmin
    }
  }
}
</script>

<style scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.hero-section {
  text-align: center;
  margin-bottom: 60px;
}

.hero-section h1 {
  font-size: 48px;
  color: #303133;
  margin-bottom: 20px;
}

.hero-section p {
  font-size: 18px;
  color: #606266;
  max-width: 600px;
  margin: 0 auto;
}

.role-selection {
  margin-bottom: 80px;
}

.role-selection h2 {
  text-align: center;
  margin-bottom: 40px;
  color: #303133;
}

.role-cards {
  display: flex;
  justify-content: center;
  gap: 40px;
  flex-wrap: wrap;
}

.role-card {
  width: 300px;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.role-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.student-card:hover {
  border-color: #409eff;
}

.admin-card:hover {
  border-color: #67c23a;
}

.card-content {
  text-align: center;
  padding: 20px;
}

.icon-container {
  margin-bottom: 20px;
}

.card-content h3 {
  font-size: 24px;
  color: #303133;
  margin-bottom: 15px;
}

.card-content p {
  color: #606266;
  margin-bottom: 25px;
  line-height: 1.6;
}

.features {
  text-align: center;
}

.features h2 {
  margin-bottom: 40px;
  color: #303133;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
}

.feature-item {
  padding: 30px 20px;
  background: #f8f9fa;
  border-radius: 12px;
  transition: all 0.3s;
}

.feature-item:hover {
  background: #fff;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.feature-item h4 {
  margin: 15px 0 10px 0;
  color: #303133;
  font-size: 18px;
}

.feature-item p {
  color: #606266;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .hero-section h1 {
    font-size: 36px;
  }
  
  .role-cards {
    flex-direction: column;
    align-items: center;
  }
  
  .role-card {
    width: 100%;
    max-width: 300px;
  }
  
  .feature-grid {
    grid-template-columns: 1fr;
  }
}
</style>
