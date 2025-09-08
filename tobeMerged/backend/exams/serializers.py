from rest_framework import serializers
from .models import (
    Exam, Question, AnswerOption, StudentAnswer, Score, Recording, 
    Evaluation, Student, ExamStudentAssignment, ExamSubmission, ExamSession
)
from django.contrib.auth.models import User

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = '__all__'

class StudentAnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.text', read_only=True)
    question_type = serializers.CharField(source='question.question_type', read_only=True)
    question_points = serializers.IntegerField(source='question.points', read_only=True)
    
    class Meta:
        model = StudentAnswer
        fields = '__all__'

class ExamSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    
    class Meta:
        model = ExamSubmission
        fields = '__all__'

class ExamSessionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    
    class Meta:
        model = ExamSession
        fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Exam
        fields = '__all__'

class ScoreSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    
    class Meta:
        model = Score
        fields = '__all__'

class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = '__all__'

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'

class ExamStudentAssignmentSerializer(serializers.ModelSerializer):
    """试卷分配序列化器"""
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    
    class Meta:
        model = ExamStudentAssignment
        fields = '__all__'

class SubmitAnswerSerializer(serializers.Serializer):
    """提交答案序列化器"""
    exam_id = serializers.IntegerField()
    answers = serializers.ListField(
        child=serializers.DictField()
    )

class ExamResultSerializer(serializers.Serializer):
    """考试结果序列化器"""
    exam_id = serializers.IntegerField()
    total_score = serializers.FloatField()
    max_score = serializers.FloatField()
    answered_questions = serializers.IntegerField()
    total_questions = serializers.IntegerField()
    time_spent = serializers.IntegerField()
    submission_id = serializers.IntegerField()

class StudentExamDetailSerializer(serializers.ModelSerializer):
    """学员考试详情序列化器"""
    questions = QuestionSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    student_answers = serializers.SerializerMethodField()
    submission = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = '__all__'
    
    def get_student_answers(self, obj):
        """获取学员的答案"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            answers = StudentAnswer.objects.filter(
                student=request.user,
                question__exam=obj
            )
            return StudentAnswerSerializer(answers, many=True).data
        return []
    
    def get_submission(self, obj):
        """获取提交记录"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            submission = ExamSubmission.objects.filter(
                student=request.user,
                exam=obj
            ).first()
            if submission:
                return ExamSubmissionSerializer(submission).data
        return None
