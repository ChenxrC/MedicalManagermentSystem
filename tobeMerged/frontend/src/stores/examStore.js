import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = '/api/exams/'

export const useExamStore = defineStore('exam', () => {
  const exams = ref([])
  const currentExam = ref(null)
  const scores = ref([])
  const studentExams = ref([])

  const fetchExams = async () => {
    const response = await axios.get(`${API_BASE_URL}`)
    exams.value = response.data
  }

  const fetchExam = async (id) => {
    const response = await axios.get(`${API_BASE_URL}${id}/`)
    currentExam.value = response.data
  }

  const fetchStudentExams = async (studentId = null) => {
    // 获取学员的考试列表
    // 如果提供了studentId，则获取特定学员的考试
    // 否则获取当前登录学员的考试
    const url = studentId 
      ? `${API_BASE_URL}?student=${studentId}`
      : `${API_BASE_URL}`
    
    const response = await axios.get(url)
    studentExams.value = response.data
  }

  const submitAnswers = async (examId, answers) => {
    const response = await axios.post(`${API_BASE_URL}student-answers/submit_answers/`, { exam_id: examId, answers })
    return response.data
  }

  const fetchScores = async () => {
    const response = await axios.get(`${API_BASE_URL}scores/`)
    scores.value = response.data
  }

  const fetchStudentScores = async (studentId = null) => {
    // 获取学员的成绩
    const url = studentId 
      ? `${API_BASE_URL}scores/?student=${studentId}`
      : `${API_BASE_URL}scores/`
    
    const response = await axios.get(url)
    return response.data
  }

  return { 
    exams, 
    currentExam, 
    scores, 
    studentExams,
    fetchExams, 
    fetchExam, 
    fetchStudentExams,
    submitAnswers, 
    fetchScores,
    fetchStudentScores
  }
})
