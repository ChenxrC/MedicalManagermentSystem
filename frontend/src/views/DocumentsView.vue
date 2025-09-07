<template>
  <div class="documents page-container">
    <el-card class="header-card enhanced-card">
      <template #header>
        <div class="card-header">
          <span class="card-title">课件/知识库管理</span>
          <el-button 
            v-if="userRole === 'teacher' || userRole === 'admin'" 
            type="primary" 
            class="enhanced-button"
            @click="onUploadDocument"
          >
            上传文档
          </el-button>
        </div>
      </template>
      <div class="card-content">
        <el-table :data="documents" style="width: 100%;" v-loading="loading" stripe class="enhanced-table">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="title" label="文档名称" />
          <el-table-column prop="created_at" label="上传日期" />
          <el-table-column label="操作" width="200">
            <template #default="scope">
              <el-button size="small" class="enhanced-button" @click="onView(scope.row)">查看</el-button>
              <el-button 
                v-if="userRole === 'teacher' || userRole === 'admin'"
                size="small" 
                type="danger" 
                class="enhanced-button"
                @click="onDelete(scope.row)"
              >
                删除
              </el-button>
              <el-button 
                v-if="userRole === 'admin' && !scope.row.published"
                size="small" 
                type="primary" 
                class="enhanced-button"
                @click="publishToHomepage(scope.row)"
              >
                发布到主页
              </el-button>
              <el-button 
                v-if="userRole === 'admin' && scope.row.published"
                size="small" 
                type="success" 
                disabled
                class="enhanced-button"
              >
                已发布
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
    
    <el-dialog v-model="uploadDialogVisible" title="上传文档" width="500px" top="10vh" class="enhanced-dialog">
      <el-form :model="documentForm" label-width="100px" :rules="documentRules" ref="documentForm" class="enhanced-form">
        <el-form-item label="文档名称" prop="title">
          <el-input v-model="documentForm.title" placeholder="请输入文档名称" />
        </el-form-item>
        <el-form-item label="所属课程" prop="course_id">
          <el-select v-model="documentForm.course_id" placeholder="请选择课程">
            <el-option
              v-for="course in courses"
              :key="course.id"
              :label="course.title"
              :value="course.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="文档内容" prop="content">
          <el-input v-model="documentForm.content" type="textarea" :rows="10" placeholder="请输入文档内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="uploadDialogVisible = false">取消</el-button>
          <el-button 
            type="primary" 
            @click="uploadDocument" 
            :loading="uploading"
            class="enhanced-button"
          >
            上传
          </el-button>
        </span>
      </template>
    </el-dialog>
    
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
  </div>
</template>

<script>
import { getDocuments, uploadDocument, getCourses, publishDocumentToHomepage } from '@/services/api'
import { getUserInfo } from '@/services/auth'

export default {
  name: 'DocumentsView',
  data() {
    return {
      documents: [],
      courses: [],
      uploadDialogVisible: false,
      viewDialogVisible: false,
      loading: false,
      uploading: false,
      userRole: '',
      documentForm: {
        title: '',
        course_id: null,
        content: ''
      },
      currentDocument: {
        title: '',
        content: ''
      },
      documentRules: {
        title: [
          { required: true, message: '请输入文档名称', trigger: 'blur' }
        ],
        course_id: [
          { required: true, message: '请选择所属课程', trigger: 'change' }
        ],
        content: [
          { required: true, message: '请输入文档内容', trigger: 'blur' }
        ]
      }
    }
  },
  async created() {
    // 获取用户角色
    const userInfo = getUserInfo()
    if (userInfo) {
      this.userRole = userInfo.role
    }
    
    // 获取文档列表
    await this.fetchDocuments()
    
    // 获取课程列表
    await this.fetchCourses()
  },
  methods: {
    async fetchDocuments() {
      this.loading = true
      try {
        const response = await getDocuments()
        this.documents = response.data.documents
      } catch (error) {
        this.$message.error('获取文档列表失败: ' + error.message)
      } finally {
        this.loading = false
      }
    },
    async fetchCourses() {
      try {
        const response = await getCourses()
        this.courses = response.data.courses
      } catch (error) {
        this.$message.error('获取课程列表失败: ' + error.message)
      }
    },
    onUploadDocument() {
      this.documentForm = { title: '', course_id: null, content: '' }
      this.uploadDialogVisible = true
    },
    onView(row) {
      this.currentDocument = { ...row }
      this.viewDialogVisible = true
    },
    onDelete(row) {
      this.$message.info('删除功能待实现')
    },
    async publishToHomepage(row) {
      try {
        await publishDocumentToHomepage(row.id)
        row.published = true
        row.published_at = new Date().toISOString()
        this.$message.success('文档已成功发布到主页')
      } catch (error) {
        this.$message.error('发布失败: ' + error.message)
      }
    },
    async uploadDocument() {
      this.$refs.documentForm.validate(async (valid) => {
        if (valid) {
          this.uploading = true
          try {
            const response = await uploadDocument(this.documentForm)
            this.$message.success('文档上传成功')
            this.uploadDialogVisible = false
            this.documentForm = { title: '', course_id: null, content: '' }
            await this.fetchDocuments()
          } catch (error) {
            this.$message.error('文档上传失败: ' + error.message)
          } finally {
            this.uploading = false
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.documents {
  padding: 20px;
}

.header-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
}

.card-content {
  margin-top: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.document-card {
  margin-bottom: 20px;
}

.document-title {
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
}

.document-content {
  text-align: left;
  padding: 20px;
  line-height: 1.6;
}
</style>