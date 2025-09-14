from django.db import models
from django.conf import settings

class Student(models.Model):
    """学员模型"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True, verbose_name='学号')
    name = models.CharField(max_length=100, verbose_name='姓名')
    email = models.EmailField(verbose_name='邮箱')
    phone = models.CharField(max_length=20, blank=True, verbose_name='电话')
    department = models.CharField(max_length=100, blank=True, verbose_name='院系')
    major = models.CharField(max_length=100, blank=True, verbose_name='专业')
    grade = models.CharField(max_length=20, blank=True, verbose_name='年级')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '学员'
        verbose_name_plural = '学员'

    def __str__(self):
        return f"{self.student_id} - {self.name}"

class Exam(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 添加试卷状态字段
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    start_time = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = (
        ('multiple', 'Single Choice'),
        ('multiple_choice', 'Multiple Choice'),
        ('fill', 'Fill in the Blank'),
        ('essay', 'Essay'),
    )
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=15, choices=QUESTION_TYPES)
    correct_answer = models.TextField(blank=True)  # For fill and essay
    points = models.IntegerField(default=1)
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)  # 新增图片字段

    def __str__(self):
        return self.text[:50]

class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class StudentAnswer(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
    selected_option = models.ForeignKey(AnswerOption, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.FloatField(default=0)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='答题时间')

    class Meta:
        verbose_name = '学员答案'
        verbose_name_plural = '学员答案'
        unique_together = ['student', 'question']  # 确保每个学员对每个题目只能有一个答案

    def __str__(self):
        return f"{self.student.username} - {self.question.text[:30]}"

class ExamSubmission(models.Model):
    """考试提交记录"""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='学员')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name='考试')
    total_score = models.FloatField(default=0, verbose_name='总分')
    max_score = models.FloatField(default=0, verbose_name='满分')
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')
    is_completed = models.BooleanField(default=True, verbose_name='是否完成')
    time_spent = models.IntegerField(default=0, verbose_name='用时(秒)')
    
    class Meta:
        verbose_name = '考试提交记录'
        verbose_name_plural = '考试提交记录'
        unique_together = ['student', 'exam']  # 确保每个学员对每个考试只能提交一次

    def __str__(self):
        return f"{self.student.username} - {self.exam.title} - {self.total_score}分"

class Score(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    total_score = models.FloatField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

class Recording(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='recordings/')
    recorded_at = models.DateTimeField(auto_now_add=True)

class Evaluation(models.Model):
    recording = models.ForeignKey(Recording, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comments = models.TextField()
    score_adjustment = models.FloatField(default=0)
    evaluated_at = models.DateTimeField(auto_now_add=True)

class ExamStudentAssignment(models.Model):
    """试卷-学员分配模型"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='student_assignments', verbose_name='试卷')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_assignments', verbose_name='学员')
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name='分配时间')
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='分配人')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        verbose_name = '试卷分配'
        verbose_name_plural = '试卷分配'
        unique_together = ['exam', 'student']  # 确保一个学员不会被重复分配同一份试卷

    def __str__(self):
        return f"{self.exam.title} - {self.student.name}"

class ExamSession(models.Model):
    """考试会话记录"""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='学员')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name='考试')
    started_at = models.DateTimeField(auto_now_add=True, verbose_name='开始时间')
    ended_at = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    is_active = models.BooleanField(default=True, verbose_name='是否活跃')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    user_agent = models.TextField(blank=True, verbose_name='用户代理')

    class Meta:
        verbose_name = '考试会话'
        verbose_name_plural = '考试会话'

    def __str__(self):
        return f"{self.student.username} - {self.exam.title} - {self.started_at}"
