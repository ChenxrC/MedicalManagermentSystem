<template>
  <div class="home page-container">
    <div class="main-content">
      <el-card class="welcome-card enhanced-card">
        <template #header>
          <div class="card-header">
            <span class="welcome-title">教育管理系统</span>
          </div>
        </template>
        <div class="welcome-content">
          <p class="welcome-text">欢迎使用集课件/知识库管理、考试系统和人员管理系统于一体的网站。</p>
        </div>
      </el-card>
      
      <div class="published-documents">
        <el-card class="documents-card enhanced-card">
          <template #header>
            <div class="card-header">
              <span class="documents-title">最新文档</span>
            </div>
          </template>
          <div v-if="publishedDocuments.length > 0" class="documents-list">
            <el-card v-for="doc in publishedDocuments" :key="doc.id" class="document-item enhanced-card hover-scale">
              <div class="document-header">
                <h3 class="document-item-title">{{ doc.title }}</h3>
                <span class="document-date">{{ formatDate(doc.published_at) }}</span>
              </div>
              <div v-html="truncateContent(doc.content)" class="document-item-content"></div>
              <el-button type="text" @click="viewDocument(doc)">查看全文</el-button>
            </el-card>
          </div>
          <div v-else class="no-documents">
            <p>暂无发布的文档</p>
          </div>
        </el-card>
      </div>
    </div>
    
    <div class="sidebar">
      <div class="features-sidebar">
      <el-card class="feature-card enhanced-card hover-scale" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon class="feature-icon"><Document /></el-icon>
            <span>课件/知识库管理</span>
          </div>
        </template>
        <p>上传、分类和检索课件与知识文档。</p>
        <div class="card-footer">
          <el-button type="primary" class="enhanced-button" @click="$router.push('/documents')">进入管理</el-button>
        </div>
      </el-card>
      
      <el-card class="feature-card enhanced-card hover-scale" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon class="feature-icon"><Edit /></el-icon>
            <span>考试系统</span>
          </div>
        </template>
        <p>管理题库、生成试卷、在线考试和成绩统计。</p>
        <div class="card-footer">
          <el-button type="primary" class="enhanced-button" @click="$router.push('/exams')">进入管理</el-button>
        </div>
      </el-card>
      
      <el-card class="feature-card enhanced-card hover-scale" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon class="feature-icon"><User /></el-icon>
            <span>人员管理系统</span>
          </div>
        </template>
        <p>管理用户信息、角色权限和组织架构。</p>
        <div class="card-footer">
          <el-button type="primary" class="enhanced-button" @click="$router.push('/users')">进入管理</el-button>
        </div>
      </el-card>
      
      <el-card class="feature-card enhanced-card hover-scale" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon class="feature-icon"><ChatDotRound /></el-icon>
            <span>知识库问答</span>
          </div>
        </template>
        <p>基于知识库的智能问答系统，帮助您快速获取信息。</p>
        <div class="card-footer">
          <el-button type="primary" class="enhanced-button" @click="toggleChatbot">立即体验</el-button>
        </div>
      </el-card>
      
    </div>
  </div>
  
    <!-- 文档查看对话框 -->
    <el-dialog v-model="viewDialogVisible" title="查看文档" width="800px" top="5vh" class="enhanced-dialog">
      <el-card class="document-card enhanced-card">
        <template #header>
          <div class="card-header">
            <span class="document-title">{{ currentDocument.title }}</span>
          </div>
        </template>
        <div v-html="currentDocument.content" class="document-content"></div>
      </el-card>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="viewDialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>

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
import { Document, Edit, User, ChatDotRound, Close, Upload } from '@element-plus/icons-vue'
import { onMounted, onUnmounted } from 'vue'
import { isAuthenticated, getUserInfo } from '@/services/auth'
import { getPublishedDocuments } from '@/services/api'

export default {
  name: 'HomeView',
  components: {
    Document,
    Edit,
    User,
    ChatDotRound,
    Close,
    Upload
  },
  data() {
    return {
      chatbotVisible: false,
      isAuthenticated: false,
      publishedDocuments: [],
      loading: false,
      userRole: '',
      viewDialogVisible: false,
      currentDocument: {}
    }
  },
  methods: {
    toggleChatbot() {
      this.chatbotVisible = !this.chatbotVisible
    },
    checkAuthStatus() {
      this.isAuthenticated = isAuthenticated()
      const userInfo = getUserInfo()
      this.userRole = userInfo ? userInfo.role : ''
    },
    async fetchPublishedDocuments() {
      this.loading = true
      try {
        const response = await getPublishedDocuments()
        this.publishedDocuments = response.data.documents
      } catch (error) {
        this.$message.error('获取文档失败: ' + error.message)
      } finally {
        this.loading = false
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString()
    },
    truncateContent(content) {
      // 移除HTML标签并截断文本
      const plainText = content.replace(/<[^>]*>/g, '')
      return plainText.length > 150 ? plainText.slice(0, 150) + '...' : plainText
    },
    viewDocument(doc) {
      this.currentDocument = doc
      this.viewDialogVisible = true
    },
    goToDocuments() {
      this.$router.push('/documents')
    }
  },
  mounted() {
    this.checkAuthStatus()
    this.fetchPublishedDocuments()
    window.addEventListener('storage', this.checkAuthStatus)
  },
  beforeUnmount() {
    window.removeEventListener('storage', this.checkAuthStatus)
  }
}
</script>

<style scoped>
.home {
  padding: 20px;
  display: flex;
  position: relative;
}

.main-content {
  flex: 1;
  padding-right: 240px;
}

.sidebar {
  position: fixed;
  top: 20px;
  right: 20px;
  width: 220px;
}

.features-sidebar {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.published-documents {
  margin-top: 30px;
}

.document-item {
  margin-bottom: 15px;
}

.document-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.document-item-title {
  font-size: 18px;
  margin: 0;
}

.document-date {
  font-size: 12px;
  color: #666;
}

.document-item-content {
  color: #333;
  line-height: 1.6;
  margin-bottom: 10px;
  max-height: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.no-documents {
  text-align: center;
  padding: 40px 0;
  color: #999;
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