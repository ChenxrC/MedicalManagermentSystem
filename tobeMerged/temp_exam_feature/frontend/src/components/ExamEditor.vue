<template>
  <div>
    <h2>试卷编辑</h2>
    <el-form>
      <el-input v-model="exam.title" placeholder="标题"></el-input>
      <el-input v-model="exam.description" placeholder="描述"></el-input>
      <!-- 添加问题等 -->
      <el-button @click="saveExam">保存</el-button>
    </el-form>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const exam = ref({ title: '', description: '' })
    const saveExam = async () => {
      await axios.post('/api/exams/exams/', exam.value)
    }
    return { exam, saveExam }
  }
}
</script>
