<template>
  <div class="home-page">
    <div class="hero-section">
      <h1>在线考试管理系统</h1>
      <p>专业的在线考试平台，支持多种题型，实时评分，视频录制</p>
    </div>

    <div class="role-selection">
      <h2>请选择您的身份</h2>
      
      <div class="role-cards">
        <!-- 使用原生HTML替代Element Plus卡片和按钮 -->
        <div class="role-card student-card">
          <div class="card-content">
            <div class="icon-container">
              <div class="user-icon">👤</div>
            </div>
            <h3>学员入口</h3>
            <p>查看考试列表，参加考试，查看成绩</p>
            <button class="native-button student-button" onclick="console.log('学员按钮点击'); window.location.href='/student-login'">
              进入学员系统
            </button>
          </div>
        </div>

        <div class="role-card admin-card">
          <div class="card-content">
            <div class="icon-container">
              <div class="admin-icon">⚙️</div>
            </div>
            <h3>管理员入口</h3>
            <p>创建试卷，管理考试，查看成绩</p>
            <button class="native-button admin-button" onclick="console.log('管理员按钮点击'); window.location.href='/admin'">
              进入管理系统
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="features">
      <h2>系统功能</h2>
      <div class="feature-grid">
        <div class="feature-item">
          <div class="feature-icon">📄</div>
          <h4>试卷管理</h4>
          <p>支持多种题型，灵活配置试卷</p>
        </div>
        <div class="feature-item">
          <div class="feature-icon">🎥</div>
          <h4>视频录制</h4>
          <p>考试过程全程录制，确保公平</p>
        </div>
        <div class="feature-item">
          <div class="feature-icon">🏆</div>
          <h4>自动评分</h4>
          <p>选择题自动评分，提高效率</p>
        </div>
        <div class="feature-item">
          <div class="feature-icon">⚠️</div>
          <h4>错题分析</h4>
          <p>详细的错题分析，帮助学习</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage'
}
</script>

<style scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  background: white;
  color: black;
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.hero-section {
  text-align: center;
  margin-bottom: 60px;
}

.hero-section h1 {
  font-size: 48px;
  color: black;
  margin-bottom: 20px;
}

.hero-section p {
  font-size: 18px;
  color: #333;
  max-width: 600px;
  margin: 0 auto;
}

.role-selection {
  margin-bottom: 80px;
}

.role-selection h2 {
  text-align: center;
  margin-bottom: 40px;
  color: black;
}

.role-cards {
  display: flex;
  justify-content: center;
  gap: 40px;
  flex-wrap: wrap;
}

.role-card {
  width: 300px;
  transition: all 0.3s;
  border: 2px solid transparent;
  background: white !important;
  color: black !important;
  position: relative;
}

/* 确保按钮可以被点击 */
.card-content {
  position: relative;
  z-index: 1;
}

.el-button {
  position: relative;
  z-index: 10;
  cursor: pointer !important;
  pointer-events: auto !important;
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
  color: black;
  margin-bottom: 15px;
}

.card-content p {
  color: #333;
  margin-bottom: 25px;
  line-height: 1.6;
}

.features {
  text-align: center;
}

.features h2 {
  margin-bottom: 40px;
  color: black;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
}

.feature-item {
  padding: 30px 20px;
  background: white;
  border-radius: 12px;
  transition: all 0.3s;
  border: 1px solid #e0e0e0;
}

.feature-item:hover {
  background: #fff;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.feature-item h4 {
  margin: 15px 0 10px 0;
  color: black;
  font-size: 18px;
}

.feature-item p {
  color: #333;
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
