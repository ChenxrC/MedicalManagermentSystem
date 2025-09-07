<template>
  <div>
    <h2>错题分析</h2>
    <el-table :data="wrongAnswers">
      <el-table-column prop="question.text" label="问题"></el-table-column>
      <el-table-column prop="answer_text" label="你的答案"></el-table-column>
      <el-table-column prop="question.correct_answer" label="正确答案"></el-table-column>
      <el-table-column prop="feedback" label="分析"></el-table-column>
    </el-table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const wrongAnswers = ref([])
    onMounted(async () => {
      const response = await axios.get('/api/exams/answers/?student=current&score=0')  // 假设current user
      wrongAnswers.value = response.data
    })
    return { wrongAnswers }
  }
}
</script>
