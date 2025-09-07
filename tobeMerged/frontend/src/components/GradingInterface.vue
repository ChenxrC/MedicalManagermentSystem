<template>
  <div>
    <h2>打分界面</h2>
    <!-- 显示学生答案，允许修改分数，加和 -->
    <el-table :data="answers">
      <el-table-column prop="question.text" label="问题"></el-table-column>
      <el-table-column prop="answer_text" label="答案"></el-table-column>
      <el-table-column label="分数">
        <template #default="scope">
          <el-input v-model="scope.row.score"></el-input>
        </template>
      </el-table-column>
    </el-table>
    <el-button @click="saveScores">保存</el-button>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  props: ['studentId', 'examId'],
  setup(props) {
    const answers = ref([])
    // fetch answers for student and exam
    const fetchAnswers = async () => {
      const response = await axios.get(`/api/exams/answers/?student=${props.studentId}&amp;question__exam=${props.examId}`)
      answers.value = response.data
    }
    const saveScores = async () => {
      for (let ans of answers.value) {
        await axios.patch(`/api/exams/answers/${ans.id}/`, { score: ans.score })
      }
      // recalculate total
    }
    fetchAnswers()
    return { answers, saveScores }
  }
}
</script>
