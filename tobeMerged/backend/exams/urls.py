from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'exams', views.ExamViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'answer-options', views.AnswerOptionViewSet)
router.register(r'student-answers', views.StudentAnswerViewSet)
router.register(r'scores', views.ScoreViewSet)
router.register(r'recordings', views.RecordingViewSet)
router.register(r'evaluations', views.EvaluationViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'exam-assignments', views.ExamStudentAssignmentViewSet)
router.register(r'exam-submissions', views.ExamSubmissionViewSet)
router.register(r'exam-sessions', views.ExamSessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='student_login'),
    path('logout/', views.LogoutView.as_view(), name='student_logout'),
    path('user-info/', views.UserInfoView.as_view(), name='user_info'),
]
