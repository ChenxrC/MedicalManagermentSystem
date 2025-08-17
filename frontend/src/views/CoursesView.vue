<template>
  <div class="courses">
    <el-card class="header-card">
      <template #header>
        <div class="card-header">
          <span class="card-title">课程管理</span>
          <el-button 
            v-if="userRole === 'teacher' || userRole === 'admin'" 
            type="primary" 
            @click="onCreateCourse"
          >
            创建课程
          </el-button>
        </div>
      </template>
      <div class="card-content">
        <el-table :data="courses" style="width: 100%;" v-loading="loading" stripe>
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="title" label="课程名称" />
          <el-table-column prop="description" label="描述" />
          <el-table-column prop="created_at" label="创建时间" />
          <el-table-column label="操作" width="200">
            <template #default="scope">
              <el-button size="small" @click="viewCourse(scope.row)">查看</el-button>
              <el-button 
                v-if="userRole === 'teacher' || userRole === 'admin'" 
                size="small" 
                type="danger" 
                @click="onDelete(scope.row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
    
    <el-dialog v-model="dialogVisible" title="课程信息" width="500px" top="10vh">
      <el-form :model="courseForm" label-width="100px" :rules="courseRules" ref="courseForm">
        <el-form-item label="课程名称" prop="title">
          <el-input v-model="courseForm.title" placeholder="请输入课程名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="courseForm.description" type="textarea" placeholder="请输入课程描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button 
            type="primary" 
            @click="saveCourse" 
            :loading="saving"
          >
            保存
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { getCourses, createCourse } from '@/services/api'
import { getUserInfo } from '@/services/auth'

export default {
  name: 'CoursesView',
  data() {
    return {
      courses: [],
      dialogVisible: false,
      loading: false,
      saving: false,
      userRole: '',
      courseForm: {
        title: '',
        description: ''
      },
      courseRules: {
        title: [
          { required: true, message: '请输入课程名称', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请输入描述', trigger: 'blur' }
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
    
    // 获取课程列表
    await this.fetchCourses()
  },
  methods: {
    async fetchCourses() {
      this.loading = true
      try {
        const response = await getCourses()
        this.courses = response.data.courses
      } catch (error) {
        this.$message.error('获取课程列表失败: ' + error.message)
      } finally {
        this.loading = false
      }
    },
    onCreateCourse() {
      this.courseForm = { title: '', description: '' }
      this.dialogVisible = true
    },
    viewCourse(course) {
      // 跳转到课程详情页
      this.$router.push(`/courses/${course.id}`)
    },
    onDelete(row) {
      this.$message.info('删除功能待实现')
    },
    async saveCourse() {
      this.$refs.courseForm.validate(async (valid) => {
        if (valid) {
          this.saving = true
          try {
            const response = await createCourse(this.courseForm)
            this.$message.success('课程创建成功')
            this.dialogVisible = false
            this.courseForm = { title: '', description: '' }
            await this.fetchCourses()
          } catch (error) {
            this.$message.error('课程创建失败: ' + error.message)
          } finally {
            this.saving = false
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.courses {
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
</style>