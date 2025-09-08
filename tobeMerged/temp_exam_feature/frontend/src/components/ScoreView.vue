<template>
  <div>
    <h2>分数查看</h2>
    <el-table :data="scores">
      <el-table-column prop="exam.title" label="试卷"></el-table-column>
      <el-table-column prop="total_score" label="总分"></el-table-column>
    </el-table>
  </div>
</template>

<script>
import { useExamStore } from '@/stores/examStore'
import { onMounted } from 'vue'

export default {
  setup() {
    const examStore = useExamStore()
    onMounted(() => examStore.fetchScores())
    return { scores: examStore.scores }
  }
}
</script>
