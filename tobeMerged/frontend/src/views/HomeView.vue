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

    <!-- 知识库问答聊天机器人 (已暂时移除外部资源引用) -->
  </div>
</template>

<script>
import { Document, Edit, User, Upload } from '@element-plus/icons-vue'
import { onMounted, onUnmounted } from 'vue'
import { getToken, getCurrentUser } from '@/services/auth'
import { getPublishedDocuments } from '@/services/api'

export default {
  name: 'HomeView',
  components: {
    Document,
    Edit,
    User,
    Upload
  },
  data() {
    return {
      isAuthenticated: false,
      publishedDocuments: [],
      loading: false,
      userRole: '',
      viewDialogVisible: false,
      currentDocument: {}
    }
  },
  methods: {
    checkAuthStatus() {
      this.isAuthenticated = !!getToken()
      const userInfo = getCurrentUser()
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
/* 设置整个页面为亮色白底 */
.home {
  padding: 0 20px 40px 20px;
  display: flex;
  position: relative;
  background-color: #ffffff;
  min-height: calc(100vh - 100px);
  margin-top: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

/* 主内容区域样式 */
.main-content {
  flex: 1;
  margin-right: 260px;
}

/* 侧边栏样式 */
.sidebar {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 240px;
  z-index: 10;
  margin-bottom: 40px;
}

.features-sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 文档区域样式 */
.published-documents {
  margin-top: 40px;
}

.document-item {
  margin-bottom: 20px;
  background-color: #ffffff;
  border-radius: 12px;
}

.document-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}

.document-item-title {
  font-size: 18px;
  margin: 0;
  color: #000000;
  font-weight: 600;
}

.document-date {
  font-size: 12px;
  color: #666666;
  background-color: #f8f9fa;
  padding: 2px 8px;
  border-radius: 12px;
}

.document-item-content {
  color: #333333;
  line-height: 1.7;
  margin-bottom: 12px;
  max-height: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.no-documents {
  text-align: center;
  padding: 60px 0;
  color: #666666;
  background-color: #f8f9fa;
  border-radius: 12px;
}

/* 欢迎卡片样式 */
.welcome-card {
  margin-bottom: 40px;
  background-color: #ffffff;
  border-radius: 12px;
}

.welcome-title {
  font-size: 32px;
  font-weight: bold;
  color: #000000;
  margin-bottom: 16px;
  position: relative;
  display: inline-block;
}

.welcome-title:after {
  content: '';
  position: absolute;
  bottom: -6px;
  left: 0;
  width: 60px;
  height: 4px;
  background-color: #409eff;
  border-radius: 2px;
}

.welcome-text {
  font-size: 16px;
  color: #333333;
  line-height: 1.8;
  padding-left: 2px;
}

/* 功能卡片样式 */
.features {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 24px;
}

.feature-card {
  width: 240px;
  min-height: 220px;
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
  border-radius: 12px;
}

.card-header {
  display: flex;
  align-items: center;
  font-size: 18px;
  font-weight: 600;
  color: #000000;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 12px;
}

.feature-icon {
  margin-right: 12px;
  font-size: 24px;
  color: #409eff;
}

.card-footer {
  margin-top: auto;
  text-align: right;
  padding-top: 16px;
  padding-bottom: 8px;
  border-top: 1px solid #f0f0f0;
}

/* 确保卡片内容不被截断 */
.el-card__body {
  min-height: 100px;
  display: flex;
  flex-direction: column;
}

/* 按钮样式优化 */
.el-button--primary {
  background-color: #409eff;
  border-color: #409eff;
  border-radius: 6px;
}

.el-button--primary:hover {
  background-color: #66b1ff;
  border-color: #66b1ff;
}

.el-button--text {
  color: #409eff;
}

.el-button--text:hover {
  color: #66b1ff;
  background-color: rgba(64, 158, 255, 0.05);
}


/* Element Plus 组件样式覆盖 */
.enhanced-card {
  background-color: #ffffff !important;
  border: 1px solid #f0f0f0;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
}

.el-card__body {
  color: #333333 !important;
  padding: 24px !important;
}

.el-card__header {
  color: #000000 !important;
  border-bottom: 1px solid #f0f0f0;
  padding: 20px 24px !important;
}

/* 响应式设计 */
@media screen and (max-width: 1200px) {
  .main-content {
    padding-right: 240px;
  }
  
  .sidebar {
    width: 220px;
  }
  
  .feature-card {
    width: 220px;
  }
}

@media screen and (max-width: 992px) {
  .home {
    flex-direction: column;
    padding: 16px;
  }
  
  .main-content {
    padding-right: 0;
    width: 100%;
  }
  
  .sidebar {
    position: relative;
    top: 0;
    right: 0;
    width: 100%;
    margin-top: 30px;
  }
  
  .features-sidebar {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 12px;
  }
  
  .feature-card {
    flex: 1;
    min-width: 200px;
    height: 180px;
  }
  
  .welcome-title {
    font-size: 28px;
  }
}

@media screen and (max-width: 768px) {
  .features-sidebar {
    flex-direction: column;
  }
  
  .feature-card {
    width: 100%;
    min-width: unset;
  }
  
  .welcome-title {
    font-size: 24px;
  }
  
  .welcome-text {
    font-size: 14px;
  }
  
  .document-item-title {
    font-size: 16px;
  }
  
}
</style>