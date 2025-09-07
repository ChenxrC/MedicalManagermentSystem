<template>
  <div>
    <h2>答题</h2>
    <video ref="video" autoplay></video>
    <el-button @click="startRecording">开始录制</el-button>
    <el-button @click="stopRecording">停止录制</el-button>
    <!-- 问题列表和答案输入 -->
    <el-button @click="submit">提交</el-button>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useExamStore } from '@/stores/examStore'
import axios from 'axios'

export default {
  setup() {
    const video = ref(null)
    const mediaRecorder = ref(null)
    const chunks = ref([])
    const examStore = useExamStore()

    onMounted(async () => {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true })
      video.value.srcObject = stream
      mediaRecorder.value = new MediaRecorder(stream)
      mediaRecorder.value.ondataavailable = (e) => chunks.value.push(e.data)
    })

    const startRecording = () => mediaRecorder.value.start()
    const stopRecording = async () => {
      mediaRecorder.value.stop()
      mediaRecorder.value.onstop = async () => {
        const blob = new Blob(chunks.value, { type: 'video/webm' })
        const formData = new FormData()
        formData.append('video_file', blob)
        formData.append('exam', examStore.currentExam.id)
        await axios.post('/api/exams/recordings/', formData)
      }
    }

    const submit = () => {
      // 提交答案
      examStore.submitAnswers(examStore.currentExam.id, /* answers */)
    }

    return { video, startRecording, stopRecording, submit }
  }
}
</script>

