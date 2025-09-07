<template>
  <div class="home">
    <el-card class="welcome-card">
      <template #header>
        <div class="card-header">
          <span class="welcome-title">教育管理系统</span>
        </div>
      </template>
      <div class="welcome-content">
        <p class="welcome-text">欢迎使用集课件/知识库管理、考试系统和人员管理系统于一体的网站。</p>
      </div>
    </el-card>
    
    <div class="features">
      <el-card class="feature-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon class="feature-icon"><Document /></el-icon>
            <span>课件/知识库管理</span>
          </div>
        </template>
        <p>上传、分类和检索课件与知识文档。</p>
        <div class="card-footer">
          <el-button type="primary" @click="$router.push('/documents')">进入管理</el-button>
        </div>
      </el-card>
      
      <el-card class="feature-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon class="feature-icon"><Edit /></el-icon>
            <span>考试系统</span>
          </div>
        </template>
        <p>管理题库、生成试卷、在线考试和成绩统计。</p>
        <div class="card-footer">
          <el-button type="primary" @click="$router.push('/exams')">进入管理</el-button>
        </div>
      </el-card>
      
      <el-card class="feature-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon class="feature-icon"><User /></el-icon>
            <span>人员管理系统</span>
          </div>
        </template>
        <p>管理用户信息、角色权限和组织架构。</p>
        <div class="card-footer">
          <el-button type="primary">进入管理</el-button>
        </div>
      </el-card>
      
      <el-card class="feature-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon class="feature-icon"><ChatDotRound /></el-icon>
            <span>知识库问答</span>
          </div>
        </template>
        <p>基于知识库的智能问答系统，帮助您快速获取信息。</p>
        <div class="card-footer">
          <el-button type="primary" @click="toggleChatbot">立即体验</el-button>
        </div>
      </el-card>
    </div>
    
    <!-- 知识库问答聊天机器人 -->
    <div class="chatbot-container">
      <div class="chatbot-toggle" @click="toggleChatbot">
        <el-icon v-if="!chatbotVisible"><ChatDotRound /></el-icon>
        <el-icon v-else><Close /></el-icon>
      </div>
      <div v-show="chatbotVisible" class="chatbot-iframe">
        <iframe 
          src="https://udify.app/chatbot/5O3wFflOxVUinqz9" 
          style="width: 100%; height: 100%; min-height: 700px" 
          frameborder="0" 
          allow="microphone"> 
        </iframe>
      </div>
    </div>
  </div>
</template>

<script>
import { Document, Edit, User, ChatDotRound, Close } from '@element-plus/icons-vue'
import { onMounted, onUnmounted } from 'vue'
import { isAuthenticated } from '@/services/auth'

export default {
  name: 'HomeView',
  components: {
    Document,
    Edit,
    User,
    ChatDotRound,
    Close
  },
  data() {
    return {
      chatbotVisible: false,
      isAuthenticated: false
    }
  },
  methods: {
    toggleChatbot() {
      this.chatbotVisible = !this.chatbotVisible
    },
    checkAuthStatus() {
      this.isAuthenticated = isAuthenticated()
    }
  },
  mounted() {
    this.checkAuthStatus()
    // 监听存储事件以更新认证状态
    window.addEventListener('storage', this.checkAuthStatus)
  },
  beforeUnmount() {
    // 移除事件监听器
    window.removeEventListener('storage', this.checkAuthStatus)
  }
}
</script>

<style scoped>
.home {
  padding: 20px;
}

.welcome-card {
  margin-bottom: 30px;
}

.welcome-title {
  font-size: 28px;
  font-weight: bold;
  color: #409eff;
}

.welcome-text {
  font-size: 16px;
  color: #666;
  line-height: 1.6;
}

.features {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 20px;
}

.feature-card {
  width: 350px;
  height: 200px;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
}

.feature-icon {
  margin-right: 10px;
  font-size: 20px;
}

.card-footer {
  margin-top: auto;
  text-align: right;
}

/* 聊天机器人样式 */
.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.chatbot-toggle {
  width: 50px;
  height: 50px;
  background-color: #409eff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  color: white;
  font-size: 20px;
  transition: all 0.3s;
}

.chatbot-toggle:hover {
  background-color: #66b1ff;
  transform: scale(1.1);
}

.chatbot-iframe {
  position: fixed;
  bottom: 80px;
  right: 20px;
  width: 400px;
  height: 600px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}
</style>