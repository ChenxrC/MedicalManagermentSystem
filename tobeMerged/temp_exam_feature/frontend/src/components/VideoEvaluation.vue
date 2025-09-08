<template>
  <div>
    <h2>视频评价</h2>
    <video :src="recording.video_file" controls></video>
    <el-input v-model="evaluation.comments" type="textarea"></el-input>
    <el-input v-model="evaluation.score_adjustment" type="number"></el-input>
    <el-button @click="saveEvaluation">保存</el-button>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  props: ['recordingId'],
  setup(props) {
    const recording = ref({})
    const evaluation = ref({ comments: '', score_adjustment: 0 })
    // fetch recording
    const fetchRecording = async () => {
      const response = await axios.get(`/api/exams/recordings/${props.recordingId}/`)
      recording.value = response.data
    }
    const saveEvaluation = async () => {
      await axios.post('/api/exams/evaluations/', { ...evaluation.value, recording: props.recordingId })
    }
    fetchRecording()
    return { recording, evaluation, saveEvaluation }
  }
}
</script>
