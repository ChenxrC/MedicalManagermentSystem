<template>
  <div class="exam-editor">
    <h2>试卷编辑</h2>
    
    <!-- 试卷基本信息 -->
    <el-form 
      ref="formRef" 
      :model="exam" 
      :rules="rules" 
      label-width="80px"
      class="exam-form"
    >
      <el-form-item label="标题" prop="title">
        <el-input 
          v-model="exam.title" 
          placeholder="请输入试卷标题"
          maxlength="255"
          show-word-limit
        />
      </el-form-item>
      
      <el-form-item label="描述" prop="description">
        <el-input 
          v-model="exam.description" 
          type="textarea" 
          :rows="4"
          placeholder="请输入试卷描述"
          maxlength="1000"
          show-word-limit
        />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="saveExam" :loading="saving">
          {{ saving ? '保存中...' : '保存试卷' }}
        </el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
    
    <!-- 问题管理 -->
    <div v-if="exam.id" class="questions-section">
      <div class="section-header">
        <h3>问题管理</h3>
        <div class="header-actions">
          <el-button type="success" @click="showAddQuestion = true" class="add-question-btn">
            <el-icon><Plus /></el-icon>
            添加问题
          </el-button>
          <el-button type="info" @click="refreshQuestions" :loading="loadingQuestions">
            <el-icon><Refresh /></el-icon>
            刷新列表
          </el-button>
        </div>
      </div>
      
      <!-- 问题统计 -->
      <div class="questions-stats">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number">{{ questions.length }}</div>
                <div class="stat-label">总题数</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number">{{ getQuestionTypeCount('multiple') }}</div>
                <div class="stat-label">单选题</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number">{{ getQuestionTypeCount('multiple_choice') }}</div>
                <div class="stat-label">多选题</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number">{{ getTotalPoints() }}</div>
                <div class="stat-label">总分</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      
      <!-- 问题列表 -->
      <div v-if="questions.length > 0" class="questions-list">
        <div class="questions-scroll-container">
          <el-card v-for="(question, index) in questions" :key="question.id" class="question-card">
            <div class="question-header">
              <div class="question-info">
                <span class="question-number">第{{ index + 1 }}题</span>
                <el-tag :type="getQuestionTypeColor(question.question_type)" size="small">
                  {{ getQuestionTypeName(question.question_type) }}
                </el-tag>
                <span class="question-points">{{ question.points }}分</span>
              </div>
              <div class="question-actions">
                <el-button type="primary" size="small" @click="editQuestion(question)">
                  编辑
                </el-button>
                <el-button type="danger" size="small" @click="deleteQuestion(question.id)">
                  删除
                </el-button>
              </div>
            </div>
            
            <div class="question-content">
              <div class="question-text">
                <strong>题目：</strong>{{ question.text }}
              </div>
              
              <!-- 显示题目图片 -->
              <div v-if="question.image_url" class="question-image">
                <img :src="question.image_url" alt="题目图片" class="question-img" />
              </div>
              
              <!-- 显示选项 -->
              <div v-if="question.options && Array.isArray(question.options) && question.options.length > 0" class="question-options">
                <div class="options-title"><strong>选项：</strong></div>
                <div class="options-list">
                  <div v-for="(option, index) in question.options" :key="option.id || index" class="option-item">
                    <span class="option-label">{{ getOptionLabel(index) }}.</span>
                    <span class="option-text">{{ option.text }}</span>
                    <span v-if="option.is_correct" class="correct-mark">✓</span>
                  </div>
                </div>
              </div>
              
              <!-- 显示答案 -->
              <div v-if="question.correct_answer" class="question-answer">
                <strong>答案：</strong>{{ question.correct_answer }}
              </div>
            </div>
          </el-card>
        </div>
      </div>
      
      <div v-else class="no-questions">
        <el-empty description="暂无问题，请添加问题" />
      </div>
    </div>
    
    <!-- 添加问题对话框 -->
    <el-dialog v-model="showAddQuestion" title="添加问题" width="800px">
      <el-form ref="questionFormRef" :model="newQuestion" :rules="questionRules" label-width="100px">
        <el-form-item label="题目类型" prop="question_type">
          <el-select v-model="newQuestion.question_type" placeholder="请选择题目类型" @change="onQuestionTypeChange">
            <el-option label="单选题" value="multiple" />
            <el-option label="多选题" value="multiple_choice" />
            <el-option label="填空题" value="fill" />
            <el-option label="问答题" value="essay" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="题目内容" prop="text">
          <el-input 
            v-model="newQuestion.text" 
            type="textarea" 
            :rows="3"
            placeholder="请输入题目内容"
          />
        </el-form-item>
        
        <!-- 图片上传 -->
        <el-form-item label="题目图片">
          <el-upload
            ref="imageUpload"
            :action="`${baseURL}/api/exams/questions/upload_image/`"
            :headers="uploadHeaders"
            :show-file-list="false"
            :on-success="handleImageSuccess"
            :on-error="handleImageError"
            :before-upload="beforeImageUpload"
            accept="image/*"
            name="image"
            class="image-upload"
          >
            <div v-if="newQuestion.image_url" class="image-preview">
              <img :src="newQuestion.image_url" alt="题目图片" class="preview-image" />
              <div class="image-actions">
                <el-button type="danger" size="small" @click="removeImage">删除图片</el-button>
              </div>
            </div>
            <div v-else class="upload-placeholder">
              <el-icon class="upload-icon"><Plus /></el-icon>
              <div class="upload-text">点击上传图片</div>
              <div class="upload-hint">支持 JPG、PNG、GIF 格式，最大 5MB</div>
            </div>
          </el-upload>
        </el-form-item>
        
        <!-- 选择题选项 -->
        <div v-if="isMultipleChoice" class="options-section">
          <el-form-item label="选项设置">
            <div class="options-container">
              <div v-for="(option, index) in newQuestion.options" :key="index" class="option-row">
                <div class="option-input-group">
                  <span class="option-label">{{ getOptionLabel(index) }}.</span>
                  <el-input 
                    v-model="option.text" 
                    placeholder="请输入选项内容"
                    class="option-input"
                  />
                  <el-checkbox 
                    v-model="option.is_correct" 
                    :disabled="!isMultipleChoice && getCorrectOptionsCount() >= 1"
                  >
                    正确答案
                  </el-checkbox>
                  <el-button 
                    type="danger" 
                    size="small" 
                    @click="removeOption(index)"
                    :disabled="newQuestion.options.length <= 2"
                  >
                    删除
                  </el-button>
                </div>
              </div>
              
              <el-button type="primary" @click="addOption" class="add-option-btn">
                <el-icon><Plus /></el-icon>
                添加选项
              </el-button>
            </div>
          </el-form-item>
        </div>
        
        <!-- 填空题和问答题的答案 -->
        <el-form-item v-if="!isMultipleChoice" label="正确答案" prop="correct_answer">
          <el-input 
            v-model="newQuestion.correct_answer" 
            type="textarea" 
            :rows="2"
            placeholder="请输入正确答案"
          />
        </el-form-item>
        
        <el-form-item label="分值" prop="points">
          <el-input-number v-model="newQuestion.points" :min="1" :max="100" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showAddQuestion = false">取消</el-button>
        <el-button type="primary" @click="addQuestion" :loading="addingQuestion">
          {{ addingQuestion ? '添加中...' : '添加问题' }}
        </el-button>
      </template>
    </el-dialog>
    
    <!-- 成功提示 -->
    <el-alert
      v-if="saveSuccess"
      title="试卷保存成功！"
      type="success"
      :closable="false"
      show-icon
      class="success-alert"
    />
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh } from '@element-plus/icons-vue'
import axios from 'axios'

export default {
  name: 'ExamEditor',
  components: {
    Plus,
    Refresh
  },
  setup() {
    const formRef = ref(null)
    const questionFormRef = ref(null)
    const saving = ref(false)
    const saveSuccess = ref(false)
    const addingQuestion = ref(false)
    const loadingQuestions = ref(false)
    const showAddQuestion = ref(false)
    const questions = ref([])
    
    const exam = reactive({
      id: null,
      title: '',
      description: ''
    })
    
    const newQuestion = reactive({
      question_type: 'multiple',
      text: '',
      correct_answer: '',
      points: 1,
      image: null,
      image_url: '',
      options: [
        { text: '', is_correct: false },
        { text: '', is_correct: false }
      ]
    })
    
    // 图片上传相关
    const baseURL = 'http://localhost:8000'
    const uploadHeaders = {
      'X-Requested-With': 'XMLHttpRequest'
    }
    
    // 计算属性
    const isMultipleChoice = computed(() => {
      return newQuestion.question_type === 'multiple' || newQuestion.question_type === 'multiple_choice'
    })
    
    const rules = {
      title: [
        { required: true, message: '请输入试卷标题', trigger: 'blur' },
        { min: 2, max: 255, message: '标题长度在 2 到 255 个字符', trigger: 'blur' }
      ],
      description: [
        { max: 1000, message: '描述长度不能超过 1000 个字符', trigger: 'blur' }
      ]
    }
    
    const questionRules = {
      question_type: [
        { required: true, message: '请选择题目类型', trigger: 'change' }
      ],
      text: [
        { required: true, message: '请输入题目内容', trigger: 'blur' }
      ],
      points: [
        { required: true, message: '请输入分值', trigger: 'blur' }
      ]
    }
    
    const getQuestionTypeName = (type) => {
      const typeMap = {
        'multiple': '单选题',
        'multiple_choice': '多选题',
        'fill': '填空题',
        'essay': '问答题'
      }
      return typeMap[type] || type
    }
    
    const getQuestionTypeColor = (type) => {
      const colorMap = {
        'multiple': 'primary',
        'multiple_choice': 'success',
        'fill': 'warning',
        'essay': 'info'
      }
      return colorMap[type] || 'default'
    }
    
    const getQuestionTypeCount = (type) => {
      if (!Array.isArray(questions.value)) {
        return 0
      }
      return questions.value.filter(q => q.question_type === type).length
    }
    
    const getTotalPoints = () => {
      if (!Array.isArray(questions.value)) {
        return 0
      }
      return questions.value.reduce((total, q) => total + q.points, 0)
    }
    
    const getOptionLabel = (index) => {
      const labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
      return labels[index] || String.fromCharCode(97 + index)
    }
    
    const getCorrectOptionsCount = () => {
      return newQuestion.options.filter(option => option.is_correct).length
    }
    
    const onQuestionTypeChange = () => {
      // 重置选项
      if (isMultipleChoice.value) {
        newQuestion.options = [
          { text: '', is_correct: false },
          { text: '', is_correct: false }
        ]
        newQuestion.correct_answer = ''
      } else {
        newQuestion.options = []
        newQuestion.correct_answer = ''
      }
    }
    
    const addOption = () => {
      if (newQuestion.options.length < 10) {
        newQuestion.options.push({ text: '', is_correct: false })
      } else {
        ElMessage.warning('最多只能添加10个选项')
      }
    }
    
    const removeOption = (index) => {
      if (newQuestion.options.length > 2) {
        newQuestion.options.splice(index, 1)
      } else {
        ElMessage.warning('至少需要保留2个选项')
      }
    }
    
    // 图片上传相关方法
    const beforeImageUpload = (file) => {
      const isImage = file.type.startsWith('image/')
      const isLt5M = file.size / 1024 / 1024 < 5
      
      if (!isImage) {
        ElMessage.error('只能上传图片文件!')
        return false
      }
      if (!isLt5M) {
        ElMessage.error('图片大小不能超过 5MB!')
        return false
      }
      return true
    }
    
    const handleImageSuccess = (response) => {
      newQuestion.image = response.image
      newQuestion.image_url = response.image_url
      ElMessage.success('图片上传成功!')
    }
    
    const handleImageError = (error, file, fileList) => {
      console.error('图片上传失败:', error)
      console.error('错误详情:', error.response?.data)
      console.error('文件信息:', file)
      
      let errorMessage = '图片上传失败，请重试'
      if (error.response?.data?.error) {
        errorMessage = `图片上传失败: ${error.response.data.error}`
      }
      
      ElMessage.error(errorMessage)
    }
    
    const removeImage = () => {
      newQuestion.image = null
      newQuestion.image_url = ''
    }
    
    const saveExam = async () => {
      try {
        await formRef.value.validate()
        
        saving.value = true
        saveSuccess.value = false
        
        const response = await axios.post('/exams/', exam)
        
        ElMessage.success('试卷保存成功！')
        saveSuccess.value = true
        
        // 更新exam.id以便后续添加问题
        exam.id = response.data.id
        
        // 自动获取问题列表
        await fetchQuestions()
        
        console.log('保存的试卷:', response.data)
        
      } catch (error) {
        console.error('保存试卷失败:', error)
        handleError(error, '保存试卷失败')
      } finally {
        saving.value = false
      }
    }
    
    const addQuestion = async () => {
      try {
        await questionFormRef.value.validate()
        
        // 验证选项
        if (isMultipleChoice.value) {
          const validOptions = newQuestion.options.filter(option => option.text.trim())
          if (validOptions.length < 2) {
            ElMessage.error('请至少填写2个选项')
            return
          }
          
          const correctOptions = validOptions.filter(option => option.is_correct)
          if (correctOptions.length === 0) {
            ElMessage.error('请至少选择一个正确答案')
            return
          }
          
          if (newQuestion.question_type === 'multiple' && correctOptions.length > 1) {
            ElMessage.error('单选题只能有一个正确答案')
            return
          }
        }
        
        addingQuestion.value = true
        
        const questionData = {
          exam: exam.id,
          text: newQuestion.text,
          question_type: newQuestion.question_type,
          points: newQuestion.points
        }
        
        // 根据题目类型设置答案
        if (isMultipleChoice.value) {
          const correctOptions = newQuestion.options
            .filter(option => option.is_correct && option.text.trim())
            .map(option => option.text)
          questionData.correct_answer = correctOptions.join('|')
        } else {
          questionData.correct_answer = newQuestion.correct_answer
        }
        
        // 添加图片字段（如果已上传）
        if (newQuestion.image) {
          questionData.image = newQuestion.image
        }
        
        const response = await axios.post('/exams/questions/', questionData)
        
        // 如果是选择题，创建选项
        if (isMultipleChoice.value) {
          const questionId = response.data.id
          for (const option of newQuestion.options) {
            if (option.text.trim()) {
              await axios.post('/exams/answeroptions/', {
                question: questionId,
                text: option.text,
                is_correct: option.is_correct
              })
            }
          }
        }
        
        ElMessage.success('问题添加成功！')
        
        // 重新获取问题列表以显示选项
        await fetchQuestions()
        
        // 重置表单
        resetQuestionForm()
        showAddQuestion.value = false
        
      } catch (error) {
        console.error('添加问题失败:', error)
        handleError(error, '添加问题失败')
      } finally {
        addingQuestion.value = false
      }
    }
    
    const fetchQuestions = async () => {
      try {
        loadingQuestions.value = true
        const response = await axios.get(`/exams/questions/?exam=${exam.id}`)
        
        // 确保questions是一个数组
        if (response.data && Array.isArray(response.data)) {
          questions.value = response.data
        } else if (response.data && response.data.results && Array.isArray(response.data.results)) {
          // 如果API返回的是分页格式
          questions.value = response.data.results
        } else {
          questions.value = []
        }
        
        console.log('获取到的问题列表:', questions.value)
      } catch (error) {
        console.error('获取问题列表失败:', error)
        ElMessage.error('获取问题列表失败')
        questions.value = []
      } finally {
        loadingQuestions.value = false
      }
    }
    
    const refreshQuestions = async () => {
      await fetchQuestions()
      ElMessage.success('问题列表已刷新')
    }
    
    const editQuestion = (question) => {
      ElMessage.info('编辑功能开发中...')
      // TODO: 实现编辑功能
    }
    
    const deleteQuestion = async (questionId) => {
      try {
        await ElMessageBox.confirm(
          '确定要删除这个问题吗？删除后无法恢复。',
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
          }
        )
        
        await axios.delete(`/exams/questions/${questionId}/`)
        ElMessage.success('问题删除成功！')
        
        // 确保questions是数组后再进行过滤
        if (Array.isArray(questions.value)) {
          questions.value = questions.value.filter(q => q.id !== questionId)
        }
        
        // 重新获取问题列表以确保数据同步
        await fetchQuestions()
        
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除问题失败:', error)
          handleError(error, '删除问题失败')
        }
      }
    }
    
    const resetForm = () => {
      exam.id = null
      exam.title = ''
      exam.description = ''
      saveSuccess.value = false
      questions.value = []
      formRef.value?.resetFields()
    }
    
    const resetQuestionForm = () => {
      newQuestion.question_type = 'multiple'
      newQuestion.text = ''
      newQuestion.correct_answer = ''
      newQuestion.points = 1
      newQuestion.image = null
      newQuestion.image_url = ''
      newQuestion.options = [
        { text: '', is_correct: false },
        { text: '', is_correct: false }
      ]
      questionFormRef.value?.resetFields()
    }
    
    const handleError = (error, defaultMessage) => {
      if (error.response) {
        const errorData = error.response.data
        if (typeof errorData === 'object') {
          const errorMessages = Object.values(errorData).flat()
          ElMessage.error(`${defaultMessage}: ${errorMessages.join(', ')}`)
        } else {
          ElMessage.error(`${defaultMessage}: ${errorData}`)
        }
      } else if (error.request) {
        ElMessage.error('网络连接失败，请检查服务器状态')
      } else {
        ElMessage.error(`${defaultMessage}，请重试`)
      }
    }
    
    // 监听exam.id变化，自动获取问题列表
    watch(() => exam.id, (newVal) => {
      if (newVal) {
        fetchQuestions()
      }
    }, { immediate: true })
    
    return {
      formRef,
      questionFormRef,
      exam,
      newQuestion,
      rules,
      questionRules,
      saving,
      saveSuccess,
      addingQuestion,
      loadingQuestions,
      showAddQuestion,
      questions,
      isMultipleChoice,
      baseURL,
      uploadHeaders,
      saveExam,
      addQuestion,
      deleteQuestion,
      editQuestion,
      refreshQuestions,
      resetForm,
      resetQuestionForm,
      getQuestionTypeName,
      getQuestionTypeColor,
      getQuestionTypeCount,
      getTotalPoints,
      getOptionLabel,
      getCorrectOptionsCount,
      onQuestionTypeChange,
      addOption,
      removeOption,
      beforeImageUpload,
      handleImageSuccess,
      handleImageError,
      removeImage
    }
  }
}
</script>

<style scoped>
.exam-editor {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.exam-form {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.questions-section {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.questions-stats {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.stat-content {
  padding: 10px;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 5px;
}

.stat-label {
  color: #666;
  font-size: 14px;
}

.questions-list {
  margin-top: 20px;
  max-height: 400px; /* 设置最大高度 */
  overflow-y: auto; /* 添加滚动条 */
  -webkit-overflow-scrolling: touch; /* 优化移动端滚动 */
  
  /* 自定义滚动条样式 */
  scrollbar-width: thin; /* Firefox */
  scrollbar-color: #c1c1c1 #f1f1f1; /* Firefox */
}

/* Webkit浏览器的滚动条样式 */
.questions-list::-webkit-scrollbar {
  width: 8px;
}

.questions-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.questions-list::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.questions-list::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.questions-scroll-container {
  display: flex;
  flex-direction: column;
  gap: 15px; /* 卡片之间的间距 */
}

.question-card {
  margin-bottom: 15px;
  border: 1px solid #e4e7ed;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.question-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.question-number {
  font-weight: bold;
  color: #409eff;
  font-size: 16px;
}

.question-points {
  color: #e6a23c;
  font-weight: bold;
  background: #fdf6ec;
  padding: 2px 8px;
  border-radius: 4px;
}

.question-actions {
  display: flex;
  gap: 8px;
}

.question-content {
  line-height: 1.6;
}

.question-text {
  margin-bottom: 15px;
  font-size: 15px;
}

.question-image {
  margin-bottom: 15px;
  text-align: center;
}

.question-img {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.question-options {
  margin: 15px 0;
  padding: 15px;
  background: #f9f9f9;
  border-radius: 6px;
}

.options-title {
  margin-bottom: 10px;
  font-weight: bold;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.option-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background: white;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
}

.option-label {
  font-weight: bold;
  color: #409eff;
  margin-right: 10px;
  min-width: 20px;
}

.option-text {
  flex: 1;
}

.correct-mark {
  color: #67c23a;
  font-weight: bold;
  margin-left: 10px;
  font-size: 16px;
}

.question-answer {
  margin-top: 15px;
  padding: 10px 15px;
  background: #f0f9ff;
  border-left: 4px solid #409eff;
  border-radius: 4px;
}

.options-section {
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 15px;
  background: #f9f9f9;
}

.options-container {
  width: 100%;
}

.option-row {
  margin-bottom: 10px;
}

.option-input-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.option-label {
  font-weight: bold;
  color: #409eff;
  min-width: 20px;
}

.option-input {
  flex: 1;
}

.add-option-btn {
  margin-top: 10px;
}

.image-upload {
  width: 100%;
}

.upload-placeholder {
  border: 2px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  padding: 40px 20px;
  text-align: center;
  transition: border-color 0.3s;
}

.upload-placeholder:hover {
  border-color: #409eff;
}

.upload-icon {
  font-size: 28px;
  color: #8c939d;
  margin-bottom: 10px;
}

.upload-text {
  font-size: 16px;
  color: #606266;
  margin-bottom: 5px;
}

.upload-hint {
  font-size: 12px;
  color: #909399;
}

.image-preview {
  position: relative;
  display: inline-block;
  max-width: 100%;
}

.preview-image {
  max-width: 100%;
  max-height: 200px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.image-actions {
  position: absolute;
  top: 10px;
  right: 10px;
  opacity: 0;
  transition: opacity 0.3s;
}

.image-preview:hover .image-actions {
  opacity: 1;
}

.no-questions {
  text-align: center;
  padding: 40px 0;
}

.success-alert {
  margin-top: 20px;
}

h2, h3 {
  text-align: center;
  color: #303133;
  margin-bottom: 30px;
}

h3 {
  margin-bottom: 0;
}
</style>
