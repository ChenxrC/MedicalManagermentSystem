<template>
  <div class="exams">
    <el-card class="exam-card">
      <template #header>
        <div class="card-header">
          <h1>考试系统</h1>
          <el-button v-if="userRole === 'teacher' || userRole === 'admin'" type="primary" @click="onCreateExam">创建考试</el-button>
        </div>
      </template>
    
      <el-table :data="exams" style="width: 100%;" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="考试名称" />
        <el-table-column prop="course_title" label="所属课程" />
        <el-table-column prop="created_at" label="创建日期" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="onView(scope.row)">查看</el-button>
            <el-button v-if="userRole === 'teacher' || userRole === 'admin'" size="small" type="danger" @click="onDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <el-dialog v-model="createDialogVisible" title="创建考试" width="500px" top="10vh">
      <el-form :model="examForm" :rules="examRules" ref="examFormRef" label-width="100px">
        <el-form-item label="考试名称" prop="title">
          <el-input v-model="examForm.title" placeholder="请输入考试名称" />
        </el-form-item>
        <el-form-item label="所属课程" prop="course_id">
          <el-select v-model="examForm.course_id" placeholder="请选择课程">
            <el-option
              v-for="course in courses"
              :key="course.id"
              :label="course.title"
              :value="course.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="题目列表" prop="question_ids">
          <el-select v-model="examForm.question_ids" multiple placeholder="请选择题目">
            <el-option
              v-for="question in questions"
              :key="question.id"
              :label="question.content"
              :value="question.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="createDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="createExam" :loading="saving">创建</el-button>
        </span>
      </template>
    </el-dialog>
    
    <el-dialog v-model="viewDialogVisible" title="查看考试" width="800px">
      <h2>{{ currentExam.title }}</h2>
      <p>所属课程: {{ currentExam.course }}</p>
      <p>创建日期: {{ currentExam.date }}</p>
      <div class="questions">
        <h3>题目列表</h3>
        <div v-for="(question, index) in currentExam.questions" :key="question.id" class="question">
          <p>{{ index + 1 }}. {{ question.content }}</p>
          <div v-if="question.options" class="options">
            <div v-for="(option, key) in question.options" :key="key">
              {{ key }}. {{ option }}
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="viewDialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { getExams, getCourses, getQuestions, createExam } from '@/services/api'
import { getUserRole } from '@/services/auth'

export default {
  name: 'ExamsView',
  data() {
    return {
      loading: false,
      saving: false,
      userRole: '',
      exams: [],
      courses: [],
      questions: [],
      createDialogVisible: false,
      viewDialogVisible: false,
      examForm: {
        title: '',
        course_id: null,
        question_ids: []
      },
      currentExam: {
        title: '',
        course_title: '',
        created_at: '',
        questions: []
      },
      examRules: {
        title: [{ required: true, message: '请输入考试名称', trigger: 'blur' }],
        course_id: [{ required: true, message: '请选择所属课程', trigger: 'change' }],
        question_ids: [{ required: true, message: '请选择题目列表', trigger: 'change' }]
      }
    }
  },
  async created() {
    this.userRole = getUserRole()
    await this.fetchExams()
    await this.fetchCourses()
    await this.fetchQuestions()
  },
  methods: {
    async fetchExams() {
      this.loading = true
      try {
        const response = await getExams()
        // 正确获取考试数据，后端返回格式为{exams: [...]}
        this.exams = response.data && response.data.exams ? response.data.exams : []
      } catch (error) {
        console.error('获取考试列表失败:', error)
        this.exams = []
      } finally {
        this.loading = false
      }
    },
    async fetchCourses() {
      try {
        const response = await getCourses()
        // 正确获取课程数据，后端返回格式为{courses: [...]}
        this.courses = response.data && response.data.courses ? response.data.courses : []
      } catch (error) {
        console.error('获取课程列表失败:', error)
        this.courses = []
      }
    },
    async fetchQuestions() {
      try {
        const response = await getQuestions()
        // 正确获取题目数据，后端返回格式为{questions: [...]}        
        this.questions = response.data && response.data.questions ? response.data.questions : []
      } catch (error) {
        console.error('获取题目列表失败:', error)
        this.questions = []
      }
    },
    onCreateExam() {
      this.examForm = { title: '', course_id: null, question_ids: [] }
      this.createDialogVisible = true
    },
    onView(row) {
      this.currentExam = { ...row }
      this.viewDialogVisible = true
    },
    onDelete(row) {
      this.$message.info('删除考试功能待实现: ' + row.title)
    },
    async createExam() {
      this.$refs.examFormRef.validate(async (valid) => {
        if (valid) {
          this.saving = true
          try {
            const response = await createExam(this.examForm)
            this.exams.push(response.data)
            this.createDialogVisible = false
            this.$message.success('创建考试成功')
          } catch (error) {
            console.error('创建考试失败:', error)
            this.$message.error('创建考试失败')
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
.exams {
  padding: 20px;
}

.exam-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.questions {
  margin-top: 20px;
}

.question {
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #ddd;
}

.options {
  margin-top: 10px;
  padding-left: 20px;
}
</style>