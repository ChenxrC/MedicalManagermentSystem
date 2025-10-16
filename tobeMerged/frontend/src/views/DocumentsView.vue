<template>
  <div class="documents-view">
    <div class="header">
      <h1>文档中心</h1>
      <p>浏览系统发布的官方文档和学习资料</p>
    </div>
    
    <div class="documents-container">
      <el-card v-if="loading" class="loading-card">
        <div class="loading-content">
          <el-icon class="loading-icon"><Loading /></el-icon>
          <p>正在加载文档...</p>
        </div>
      </el-card>
      
      <div v-else-if="documents.length === 0" class="empty-state">
        <el-icon class="empty-icon"><Document /></el-icon>
        <p>暂无已发布的文档</p>
      </div>
      
      <div v-else class="documents-list">
        <el-card v-for="document in documents" :key="document.id" class="document-card">
          <div slot="header" class="document-header">
            <h3 class="document-title">{{ document.title }}</h3>
            <span class="document-date">{{ formatDate(document.published_at) }}</span>
          </div>
          <div class="document-content" v-html="document.content"></div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { Document, Loading } from '@element-plus/icons-vue'
import { getPublishedDocuments } from '@/services/api.js'
import { ElMessage } from 'element-plus'

export default {
  name: 'DocumentsView',
  components: {
    Document,
    Loading
  },
  setup() {
    const documents = ref([])
    const loading = ref(true)
    
    const loadDocuments = async () => {
      try {
        loading.value = true
        const response = await getPublishedDocuments()
        
        // 检查响应格式并设置文档数据
        if (response && response.data && response.data.documents) {
          documents.value = response.data.documents
        } else {
          // 如果响应格式不正确，使用模拟数据
          console.warn('文档数据格式不正确，使用模拟数据')
          documents.value = getMockDocuments()
        }
      } catch (error) {
        console.error('加载文档失败:', error)
        ElMessage.error('加载文档失败，请稍后重试')
        // 加载失败时也使用模拟数据
        documents.value = getMockDocuments()
      } finally {
        loading.value = false
      }
    }
    
    // 提供模拟文档数据作为后备方案
    const getMockDocuments = () => {
      return [
        {
          id: 1,
          title: '系统使用指南',
          content: '<p>欢迎使用本系统！本指南将帮助您快速了解系统的各项功能和操作方法。</p><p>系统主要包括课件/知识库管理、考试系统和人员管理三大模块。</p><p>如需更多帮助，请联系系统管理员。</p>',
          published_at: '2023-01-15T08:00:00Z'
        },
        {
          id: 2,
          title: '考试系统操作手册',
          content: '<p>本手册详细介绍了考试系统的使用方法，包括如何创建试卷、分配考试和查看成绩。</p><p>系统支持多种题型，包括选择题、填空题、简答题等。</p>',
          published_at: '2023-01-10T10:30:00Z'
        }
      ]
    }
    
    // 格式化日期显示
    const formatDate = (dateString) => {
      try {
        const date = new Date(dateString)
        return date.toLocaleDateString('zh-CN', {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        })
      } catch {
        return dateString
      }
    }
    
    // 组件挂载时加载文档
    onMounted(() => {
      loadDocuments()
    })
    
    return {
      documents,
      loading,
      formatDate
    }
  }
}
</script>

<style scoped>
.documents-view {
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

.documents-container {
  max-width: 1200px;
  margin: 0 auto;
}

.loading-card, .empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  margin-bottom: 20px;
}

.loading-content, .empty-state {
  text-align: center;
}

.loading-icon, .empty-icon {
  font-size: 48px;
  margin-bottom: 15px;
  color: #409eff;
}

.documents-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.document-card {
  transition: all 0.3s ease;
}

.document-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.document-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.document-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.document-date {
  color: #909399;
  font-size: 14px;
}

.document-content {
  font-size: 16px;
  line-height: 1.8;
  color: #303133;
  overflow: hidden;
}

.document-content p {
  margin-bottom: 10px;
}

.document-content p:last-child {
  margin-bottom: 0;
}
</style>