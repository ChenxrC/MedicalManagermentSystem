import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = '/api/exams/'

export const useExamStore = defineStore('exam', () => {
  const exams = ref([])
  const currentExam = ref(null)
  const scores = ref([])

  const fetchExams = async () => {
    const response = await axios.get(`${API_BASE_URL}exams/`)
    exams.value = response.data
  }

  const fetchExam = async (id) => {
    const response = await axios.get(`${API_BASE_URL}exams/${id}/`)
    currentExam.value = response.data
  }

  const submitAnswers = async (examId, answers) => {
    const response = await axios.post(`${API_BASE_URL}answers/submit_answers/`, { exam_id: examId, answers })
    return response.data
  }

  const fetchScores = async () => {
    const response = await axios.get(`${API_BASE_URL}scores/`)
    scores.value = response.data
  }

  return { exams, currentExam, scores, fetchExams, fetchExam, submitAnswers, fetchScores }
})
