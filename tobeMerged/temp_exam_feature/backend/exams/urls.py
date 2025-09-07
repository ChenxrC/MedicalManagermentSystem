from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExamViewSet, QuestionViewSet, StudentAnswerViewSet, ScoreViewSet, RecordingViewSet, EvaluationViewSet

router = DefaultRouter()
router.register(r'exams', ExamViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', StudentAnswerViewSet)
router.register(r'scores', ScoreViewSet)
router.register(r'recordings', RecordingViewSet)
router.register(r'evaluations', EvaluationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
