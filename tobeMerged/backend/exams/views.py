from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import (
    Exam, Question, AnswerOption, StudentAnswer, Score, Recording, 
    Evaluation, Student, ExamStudentAssignment, ExamSubmission, ExamSession
)
from .serializers import (
    ExamSerializer, QuestionSerializer, AnswerOptionSerializer, 
    StudentAnswerSerializer, ScoreSerializer, RecordingSerializer, 
    EvaluationSerializer, StudentSerializer, ExamStudentAssignmentSerializer,
    ExamSubmissionSerializer, ExamSessionSerializer, SubmitAnswerSerializer,
    ExamResultSerializer, StudentExamDetailSerializer
)
from django.db.models import Sum
from django.utils import timezone

class LoginView(APIView):
    """学员登录视图"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': '用户名和密码是必需的'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # 获取学员信息
            try:
                student = Student.objects.get(user=user)
                return Response({
                    'message': '登录成功',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'student_profile': {
                            'id': student.id,
                            'student_id': student.student_id,
                            'name': student.name,
                            'department': student.department,
                            'major': student.major,
                            'grade': student.grade
                        }
                    }
                })
            except Student.DoesNotExist:
                return Response({'error': '用户不是学员'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    """学员登出视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({'message': '登出成功'})

class UserInfoView(APIView):
    """获取用户信息视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        try:
            student = Student.objects.get(user=user)
            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'student_profile': {
                        'id': student.id,
                        'student_id': student.student_id,
                        'name': student.name,
                        'department': student.department,
                        'major': student.major,
                        'grade': student.grade
                    }
                }
            })
        except Student.DoesNotExist:
            return Response({'error': '用户不是学员'}, status=status.HTTP_403_FORBIDDEN)

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def for_student(self, request, pk=None):
        """获取学员的考试详情"""
        exam = self.get_object()
        
        # 检查学员是否被分配了这份考试
        assignment = ExamStudentAssignment.objects.filter(
            exam=exam,
            student__user=request.user,
            is_active=True
        ).first()
        
        if not assignment:
            return Response({'error': '您没有被分配这份考试'}, status=status.HTTP_403_FORBIDDEN)
        
        # 检查是否已经提交过
        submission = ExamSubmission.objects.filter(
            student=request.user,
            exam=exam
        ).first()
        
        if submission:
            return Response({'error': '您已经提交过这份考试'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = StudentExamDetailSerializer(exam, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def student_exams(self, request):
        """获取学员的考试列表"""
        # 获取分配给该学员的考试
        assignments = ExamStudentAssignment.objects.filter(
            student__user=request.user,
            is_active=True
        ).select_related('exam')
        
        exams = [assignment.exam for assignment in assignments]
        
        # 为每个考试添加提交状态
        for exam in exams:
            submission = ExamSubmission.objects.filter(
                student=request.user,
                exam=exam
            ).first()
            exam.has_submission = submission is not None
            if submission:
                exam.submission_data = ExamSubmissionSerializer(submission).data
        
        serializer = self.get_serializer(exams, many=True)
        return Response(serializer.data)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerOptionViewSet(viewsets.ModelViewSet):
    queryset = AnswerOption.objects.all()
    serializer_class = AnswerOptionSerializer

class StudentAnswerViewSet(viewsets.ModelViewSet):
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def submit_answers(self, request):
        """提交考试答案"""
        try:
            # 获取请求数据
            exam_id = request.data.get('exam_id')
            answers_data = request.data.get('answers', [])
            time_spent = request.data.get('time_spent', 0)
            
            if not exam_id:
                return Response({'error': '考试ID是必需的'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not answers_data:
                return Response({'error': '答案数据是必需的'}, status=status.HTTP_400_BAD_REQUEST)
            
            # 获取考试和学员信息
            exam = get_object_or_404(Exam, pk=exam_id)
            
            # 检查用户是否已认证
            if not request.user.is_authenticated:
                return Response({'error': '请先登录'}, status=status.HTTP_401_UNAUTHORIZED)
            
            student = request.user
            
            # 检查学员是否被分配了这份考试
            assignment = ExamStudentAssignment.objects.filter(
                exam=exam,
                student__user=student,
                is_active=True
            ).first()
            
            if not assignment:
                return Response({'error': '您没有被分配这份考试'}, status=status.HTTP_403_FORBIDDEN)
            
            # 检查是否已经提交过
            existing_submission = ExamSubmission.objects.filter(
                student=student, 
                exam=exam
            ).first()
            
            if existing_submission:
                return Response({'error': '您已经提交过这份考试'}, status=status.HTTP_400_BAD_REQUEST)
            
            total_score = 0
            max_score = 0
            student_answers = []
            
            # 计算满分
            questions = exam.questions.all()
            max_score = sum(question.points for question in questions)
            
            # 处理每个答案
            for answer_data in answers_data:
                question_id = answer_data.get('question_id')
                answer_text = answer_data.get('answer_text', '')
                selected_option = answer_data.get('selected_option')
                
                if not question_id:
                    continue
                
                question = get_object_or_404(Question, pk=question_id, exam=exam)
                
                # 创建学员答案记录
                student_answer = StudentAnswer.objects.create(
                    student=student,
                    question=question,
                    answer_text=answer_text,
                    selected_option_id=selected_option if not isinstance(selected_option, list) else None
                )
                
                # 自动评分
                score = 0
                if question.question_type == 'multiple':
                    # 单选题
                    if student_answer.selected_option and student_answer.selected_option.is_correct:
                        score = question.points
                elif question.question_type == 'multiple_choice':
                    # 多选题 - 需要检查所有选项
                    if selected_option and isinstance(selected_option, list):
                        correct_options = question.options.filter(is_correct=True)
                        selected_options = question.options.filter(id__in=selected_option)
                        
                        if correct_options.count() == selected_options.count() and \
                           all(opt.is_correct for opt in selected_options):
                            score = question.points
                elif question.question_type == 'fill':
                    # 填空题 - 简单字符串比较
                    if answer_text.lower().strip() == question.correct_answer.lower().strip():
                        score = question.points
                elif question.question_type == 'essay':
                    # 问答题 - 需要人工评分，暂时给0分
                    score = 0
                
                student_answer.score = score
                student_answer.save()
                
                total_score += score
                student_answers.append(student_answer)
            
            # 创建考试提交记录
            submission = ExamSubmission.objects.create(
                student=student,
                exam=exam,
                total_score=total_score,
                max_score=max_score,
                time_spent=time_spent
            )
            
            # 结束考试会话
            ExamSession.objects.filter(
                student=student,
                exam=exam,
                is_active=True
            ).update(
                ended_at=timezone.now(),
                is_active=False
            )
            
            return Response({
                'message': '考试提交成功',
                'submission_id': submission.id,
                'total_score': total_score,
                'max_score': max_score,
                'answered_questions': len(student_answers),
                'total_questions': questions.count(),
                'time_spent': time_spent
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': f'提交失败: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def start_exam(self, request):
        """开始考试"""
        try:
            exam_id = request.data.get('exam_id')
            if not exam_id:
                return Response({'error': '考试ID是必需的'}, status=status.HTTP_400_BAD_REQUEST)
            
            exam = get_object_or_404(Exam, pk=exam_id)
            
            # 检查权限
            assignment = ExamStudentAssignment.objects.filter(
                exam=exam,
                student__user=request.user,
                is_active=True
            ).first()
            
            if not assignment:
                return Response({'error': '您没有被分配这份考试'}, status=status.HTTP_403_FORBIDDEN)
            
            # 检查是否已经提交过
            if ExamSubmission.objects.filter(student=request.user, exam=exam).exists():
                return Response({'error': '您已经提交过这份考试'}, status=status.HTTP_400_BAD_REQUEST)
            
            # 创建或更新考试会话
            session, created = ExamSession.objects.get_or_create(
                student=request.user,
                exam=exam,
                is_active=True,
                defaults={
                    'ip_address': request.META.get('REMOTE_ADDR'),
                    'user_agent': request.META.get('HTTP_USER_AGENT', '')
                }
            )
            
            return Response({
                'message': '考试开始',
                'session_id': session.id,
                'started_at': session.started_at
            })
            
        except Exception as e:
            return Response({'error': f'开始考试失败: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ExamSubmissionViewSet(viewsets.ModelViewSet):
    queryset = ExamSubmission.objects.all()
    serializer_class = ExamSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_submissions(self, request):
        """获取当前用户的提交记录"""
        submissions = ExamSubmission.objects.filter(student=request.user)
        serializer = self.get_serializer(submissions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def result(self, request, pk=None):
        """获取考试结果详情"""
        submission = self.get_object()
        
        # 检查权限
        if submission.student != request.user:
            return Response({'error': '无权访问此结果'}, status=status.HTTP_403_FORBIDDEN)
        
        # 获取详细答案
        answers = StudentAnswer.objects.filter(
            student=request.user,
            question__exam=submission.exam
        )
        
        result_data = {
            'submission': ExamSubmissionSerializer(submission).data,
            'answers': StudentAnswerSerializer(answers, many=True).data
        }
        
        return Response(result_data)

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

class RecordingViewSet(viewsets.ModelViewSet):
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer

class StudentViewSet(viewsets.ModelViewSet):
    """学员管理视图集"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=False, methods=['get'])
    def list_students(self, request):
        """获取学员列表"""
        students = Student.objects.all()
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign_exam(self, request, pk=None):
        """为学员分配试卷"""
        student = self.get_object()
        exam_id = request.data.get('exam_id')
        
        if not exam_id:
            return Response({'error': '试卷ID是必需的'}, status=status.HTTP_400_BAD_REQUEST)
        
        exam = get_object_or_404(Exam, id=exam_id)
        
        # 检查是否已经分配过
        if ExamStudentAssignment.objects.filter(exam=exam, student=student, is_active=True).exists():
            return Response({'error': '该学员已经被分配过这份试卷'}, status=status.HTTP_400_BAD_REQUEST)
        
        assignment = ExamStudentAssignment.objects.create(
            exam=exam,
            student=student,
            assigned_by=request.user
        )
        
        serializer = ExamStudentAssignmentSerializer(assignment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ExamStudentAssignmentViewSet(viewsets.ModelViewSet):
    """试卷分配管理视图集"""
    queryset = ExamStudentAssignment.objects.all()
    serializer_class = ExamStudentAssignmentSerializer

    @action(detail=False, methods=['get'])
    def exam_assignments(self, request):
        """获取试卷分配列表"""
        exam_id = request.query_params.get('exam_id')
        if exam_id:
            assignments = ExamStudentAssignment.objects.filter(exam_id=exam_id, is_active=True)
        else:
            assignments = ExamStudentAssignment.objects.filter(is_active=True)
        
        serializer = self.get_serializer(assignments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def remove_assignment(self, request, pk=None):
        """移除试卷分配"""
        assignment = self.get_object()
        assignment.is_active = False
        assignment.save()
        return Response({'message': '分配已移除'}, status=status.HTTP_200_OK)

class ExamSessionViewSet(viewsets.ModelViewSet):
    """考试会话管理视图集"""
    queryset = ExamSession.objects.all()
    serializer_class = ExamSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_sessions(self, request):
        """获取当前用户的考试会话"""
        sessions = ExamSession.objects.filter(student=request.user)
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)
