#!/usr/bin/env python3
"""
数据库查询脚本 - 查看student_id和exam_id
"""

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_viewer.settings')
django.setup()

from django.contrib.auth.models import User
from exams.models import Exam, Question, StudentAnswer, Score, Recording, Evaluation

def query_database():
    """查询数据库中的student_id和exam_id"""
    print("🔍 数据库查询结果")
    print("=" * 60)
    
    # 1. 查看所有用户（学生）
    print("\n📋 所有用户（学生）：")
    print("-" * 40)
    users = User.objects.all()
    if users:
        for user in users:
            print(f"用户ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}")
    else:
        print("暂无用户数据")
    
    # 2. 查看所有试卷
    print("\n📋 所有试卷：")
    print("-" * 40)
    exams = Exam.objects.all()
    if exams:
        for exam in exams:
            print(f"试卷ID: {exam.id}, 标题: {exam.title}, 创建者: {exam.created_by.username if exam.created_by else '未知'}")
    else:
        print("暂无试卷数据")
    
    # 3. 查看所有问题
    print("\n📋 所有问题：")
    print("-" * 40)
    questions = Question.objects.all()
    if questions:
        for question in questions:
            print(f"问题ID: {question.id}, 试卷ID: {question.exam.id}, 题目: {question.text[:50]}...")
    else:
        print("暂无问题数据")
    
    # 4. 查看学生答案
    print("\n📋 学生答案：")
    print("-" * 40)
    student_answers = StudentAnswer.objects.all()
    if student_answers:
        for answer in student_answers:
            print(f"答案ID: {answer.id}, 学生ID: {answer.student.id}, 问题ID: {answer.question.id}, 试卷ID: {answer.question.exam.id}")
    else:
        print("暂无学生答案数据")
    
    # 5. 查看成绩
    print("\n📋 成绩记录：")
    print("-" * 40)
    scores = Score.objects.all()
    if scores:
        for score in scores:
            print(f"成绩ID: {score.id}, 学生ID: {score.student.id}, 试卷ID: {score.exam.id}, 总分: {score.total_score}")
    else:
        print("暂无成绩数据")
    
    # 6. 查看录制视频
    print("\n📋 录制视频：")
    print("-" * 40)
    recordings = Recording.objects.all()
    if recordings:
        for recording in recordings:
            print(f"录制ID: {recording.id}, 学生ID: {recording.student.id}, 试卷ID: {recording.exam.id}")
    else:
        print("暂无录制视频数据")
    
    # 7. 查看评价
    print("\n📋 评价记录：")
    print("-" * 40)
    evaluations = Evaluation.objects.all()
    if evaluations:
        for evaluation in evaluations:
            print(f"评价ID: {evaluation.id}, 学生ID: {evaluation.student.id}, 试卷ID: {evaluation.exam.id}")
    else:
        print("暂无评价数据")
    
    print("\n" + "=" * 60)
    print("✅ 数据库查询完成")

if __name__ == '__main__':
    query_database()
