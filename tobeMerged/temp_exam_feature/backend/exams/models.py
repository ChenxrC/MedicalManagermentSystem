from django.db import models
from django.contrib.auth.models import User

class Exam(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = (
        ('multiple', 'Multiple Choice'),
        ('fill', 'Fill in the Blank'),
        ('essay', 'Essay'),
    )
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    correct_answer = models.TextField(blank=True)  # For fill and essay
    points = models.IntegerField(default=1)

    def __str__(self):
        return self.text[:50]

class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class StudentAnswer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
    selected_option = models.ForeignKey(AnswerOption, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.FloatField(default=0)
    feedback = models.TextField(blank=True)

class Score(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    total_score = models.FloatField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

class Recording(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='recordings/')
    recorded_at = models.DateTimeField(auto_now_add=True)

class Evaluation(models.Model):
    recording = models.ForeignKey(Recording, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField()
    score_adjustment = models.FloatField(default=0)
    evaluated_at = models.DateTimeField(auto_now_add=True)
