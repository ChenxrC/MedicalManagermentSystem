#!/usr/bin/env python3
"""
检查数据库中的学员和考试数据
"""

import os
import sys
import django

# 设置Django环境
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_viewer.settings')
django.setup()

from django.contrib.auth.models import User
from exams.models import Exam, Student, ExamStudentAssignment, Question, AnswerOption

def check_database():
    """检查数据库中的数据"""
    
    print("=== 数据库数据检查 ===\n")
    
    # 检查用户
    print("1. 用户数据:")
    users = User.objects.all()
    print(f"   总用户数: {users.count()}")
    for user in users[:5]:  # 只显示前5个
        print(f"   - ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}")
    print()
    
    # 检查学员
    print("2. 学员数据:")
    students = Student.objects.all()
    print(f"   总学员数: {students.count()}")
    for student in students[:5]:  # 只显示前5个
        print(f"   - ID: {student.id}, 姓名: {student.name}, 学号: {student.student_id}, 用户ID: {student.user.id}")
    print()
    
    # 检查考试
    print("3. 考试数据:")
    exams = Exam.objects.all()
    print(f"   总考试数: {exams.count()}")
    for exam in exams[:5]:  # 只显示前5个
        print(f"   - ID: {exam.id}, 标题: {exam.title}, 启用状态: {exam.is_active}")
    print()
    
    # 检查考试分配
    print("4. 考试分配数据:")
    assignments = ExamStudentAssignment.objects.all()
    print(f"   总分配数: {assignments.count()}")
    for assignment in assignments[:5]:  # 只显示前5个
        print(f"   - 考试: {assignment.exam.title}, 学员: {assignment.student.name}, 状态: {assignment.is_active}")
    print()
    
    # 检查题目
    print("5. 题目数据:")
    questions = Question.objects.all()
    print(f"   总题目数: {questions.count()}")
    for question in questions[:5]:  # 只显示前5个
        print(f"   - ID: {question.id}, 考试: {question.exam.title}, 题型: {question.question_type}")
    print()
    
    # 检查选项
    print("6. 选项数据:")
    options = AnswerOption.objects.all()
    print(f"   总选项数: {options.count()}")
    for option in options[:5]:  # 只显示前5个
        print(f"   - ID: {option.id}, 题目: {option.question.text[:30]}..., 正确: {option.is_correct}")
    print()

if __name__ == '__main__':
    check_database()
