from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Exam, Question, StudentAnswer, Score, Recording, Evaluation
from .serializers import ExamSerializer, QuestionSerializer, StudentAnswerSerializer, ScoreSerializer, RecordingSerializer, EvaluationSerializer
from django.db.models import Sum

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class StudentAnswerViewSet(viewsets.ModelViewSet):
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer

    @action(detail=False, methods=['post'])
    def submit_answers(self, request):
        # 假设请求数据有student_id, exam_id, answers list
        student = request.user  # 假设认证
        exam = get_object_or_404(Exam, pk=request.data['exam_id'])
        total_score = 0
        for ans in request.data['answers']:
            question = get_object_or_404(Question, pk=ans['question_id'])
            student_ans = StudentAnswer.objects.create(
                student=student,
                question=question,
                answer_text=ans.get('answer_text', ''),
                selected_option_id=ans.get('selected_option')
            )
            # 自动评分
            if question.question_type == 'multiple':
                if student_ans.selected_option and student_ans.selected_option.is_correct:
                    student_ans.score = question.points
            elif question.question_type == 'fill':
                if student_ans.answer_text.lower() == question.correct_answer.lower():
                    student_ans.score = question.points
            # Essay manual
            student_ans.save()
            total_score += student_ans.score
        score = Score.objects.create(student=student, exam=exam, total_score=total_score)
        return Response({'score': total_score}, status=status.HTTP_201_CREATED)

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

class RecordingViewSet(viewsets.ModelViewSet):
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
