from django.contrib import admin
from .models import Exam, Question, AnswerOption, StudentAnswer, Score, Recording, Evaluation

admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(AnswerOption)
admin.site.register(StudentAnswer)
admin.site.register(Score)
admin.site.register(Recording)
admin.site.register(Evaluation)
