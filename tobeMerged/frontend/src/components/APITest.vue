<template>
  <div class="api-test">
    <h1>API测试页面</h1>
    
    <div class="test-section">
      <h2>后端连接测试</h2>
      <el-button @click="testBackendConnection" :loading="testing">
        {{ testing ? '测试中...' : '测试后端连接' }}
      </el-button>
      <div v-if="connectionResult" class="result">
        <pre>{{ connectionResult }}</pre>
      </div>
    </div>

    <div class="test-section">
      <h2>API端点测试</h2>
      <el-button @click="testStudentsAPI" :loading="testingStudents">
        {{ testingStudents ? '测试中...' : '测试学员API' }}
      </el-button>
      <el-button @click="testExamsAPI" :loading="testingExams">
        {{ testingExams ? '测试中...' : '测试试卷API' }}
      </el-button>
      <el-button @click="testAssignmentsAPI" :loading="testingAssignments">
        {{ testingAssignments ? '测试中...' : '测试分配API' }}
      </el-button>
      
      <div v-if="apiResults.length > 0" class="results">
        <h3>测试结果：</h3>
        <div v-for="(result, index) in apiResults" :key="index" class="result-item">
          <h4>{{ result.endpoint }}</h4>
          <pre>{{ result.data }}</pre>
        </div>
      </div>
    </div>

    <div class="test-section">
      <h2>错误日志</h2>
      <div v-if="errors.length > 0" class="errors">
        <div v-for="(error, index) in errors" :key="index" class="error-item">
          <strong>{{ error.endpoint }}:</strong> {{ error.message }}
        </div>
      </div>
      <div v-else class="no-errors">
        暂无错误
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'APITest',
  setup() {
    const testing = ref(false)
    const testingStudents = ref(false)
    const testingExams = ref(false)
    const testingAssignments = ref(false)
    const connectionResult = ref('')
    const apiResults = ref([])
    const errors = ref([])

    const addError = (endpoint, message) => {
      errors.value.push({ endpoint, message })
    }

    const testBackendConnection = async () => {
      testing.value = true
      try {
        const response = await fetch('http://localhost:8000/api/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        })
        
        connectionResult.value = {
          status: response.status,
          statusText: response.statusText,
          ok: response.ok,
          url: response.url,
          headers: Object.fromEntries(response.headers.entries())
        }
        
        if (response.ok) {
          ElMessage.success('后端连接成功')
        } else {
          ElMessage.error('后端连接失败')
        }
      } catch (error) {
        connectionResult.value = {
          error: error.message,
          type: error.name
        }
        ElMessage.error(`连接错误: ${error.message}`)
        addError('Backend Connection', error.message)
      } finally {
        testing.value = false
      }
    }

    const testStudentsAPI = async () => {
      testingStudents.value = true
      try {
        const response = await fetch('http://localhost:8000/api/students/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        })
        
        const data = await response.json()
        
        apiResults.value.push({
          endpoint: 'Students API',
          data: {
            status: response.status,
            ok: response.ok,
            dataType: typeof data,
            isArray: Array.isArray(data),
            length: Array.isArray(data) ? data.length : 'N/A',
            hasResults: data && data.results ? Array.isArray(data.results) : false,
            sample: Array.isArray(data) && data.length > 0 ? data[0] : data
          }
        })
        
        ElMessage.success('学员API测试完成')
      } catch (error) {
        ElMessage.error(`学员API错误: ${error.message}`)
        addError('Students API', error.message)
      } finally {
        testingStudents.value = false
      }
    }

    const testExamsAPI = async () => {
      testingExams.value = true
      try {
        const response = await fetch('http://localhost:8000/api/exams/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        })
        
        const data = await response.json()
        
        apiResults.value.push({
          endpoint: 'Exams API',
          data: {
            status: response.status,
            ok: response.ok,
            dataType: typeof data,
            isArray: Array.isArray(data),
            length: Array.isArray(data) ? data.length : 'N/A',
            hasResults: data && data.results ? Array.isArray(data.results) : false,
            sample: Array.isArray(data) && data.length > 0 ? data[0] : data
          }
        })
        
        ElMessage.success('试卷API测试完成')
      } catch (error) {
        ElMessage.error(`试卷API错误: ${error.message}`)
        addError('Exams API', error.message)
      } finally {
        testingExams.value = false
      }
    }

    const testAssignmentsAPI = async () => {
      testingAssignments.value = true
      try {
        const response = await fetch('http://localhost:8000/api/exam-assignments/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        })
        
        const data = await response.json()
        
        apiResults.value.push({
          endpoint: 'Assignments API',
          data: {
            status: response.status,
            ok: response.ok,
            dataType: typeof data,
            isArray: Array.isArray(data),
            length: Array.isArray(data) ? data.length : 'N/A',
            hasResults: data && data.results ? Array.isArray(data.results) : false,
            sample: Array.isArray(data) && data.length > 0 ? data[0] : data
          }
        })
        
        ElMessage.success('分配API测试完成')
      } catch (error) {
        ElMessage.error(`分配API错误: ${error.message}`)
        addError('Assignments API', error.message)
      } finally {
        testingAssignments.value = false
      }
    }

    return {
      testing,
      testingStudents,
      testingExams,
      testingAssignments,
      connectionResult,
      apiResults,
      errors,
      testBackendConnection,
      testStudentsAPI,
      testExamsAPI,
      testAssignmentsAPI
    }
  }
}
</script>

<style scoped>
.api-test {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.test-section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.test-section h2 {
  margin-bottom: 15px;
  color: #1e3a8a;
}

.test-section h3 {
  margin-top: 20px;
  margin-bottom: 10px;
  color: #1e3a8a;
}

.result {
  margin-top: 15px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.result pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.results {
  margin-top: 20px;
}

.result-item {
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.result-item h4 {
  margin: 0 0 10px 0;
  color: #1e3a8a;
}

.errors {
  margin-top: 15px;
}

.error-item {
  margin-bottom: 10px;
  padding: 10px;
  background-color: #fef0f0;
  border: 1px solid #fbc4c4;
  border-radius: 4px;
  color: #f56c6c;
}

.no-errors {
  color: #67c23a;
  font-style: italic;
}

.el-button {
  margin-right: 10px;
  margin-bottom: 10px;
}
</style>
