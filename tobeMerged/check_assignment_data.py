#!/usr/bin/env python3
"""
检查试卷分配相关的数据库数据
"""

import os
import sys
import django

# 设置Django环境
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_viewer.settings')
django.setup()

from django.contrib.auth.models import User
from exams.models import Exam, Student, ExamStudentAssignment

def check_assignment_data():
    """检查试卷分配相关的数据"""
    
    print("=== 检查试卷分配相关数据 ===\n")
    
    # 1. 检查用户数据
    print("1. 用户数据:")
    users = User.objects.all()
    print(f"   总用户数: {users.count()}")
    for user in users[:5]:
        print(f"   - ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}")
    print()
    
    # 2. 检查学员数据
    print("2. 学员数据:")
    students = Student.objects.all()
    print(f"   总学员数: {students.count()}")
    if students.count() == 0:
        print("   ⚠️ 没有学员数据，需要创建测试学员")
        # 创建测试学员
        try:
            # 获取或创建默认用户
            default_user, created = User.objects.get_or_create(
                username='default_admin',
                defaults={
                    'email': 'admin@example.com',
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            if created:
                default_user.set_password('default123')
                default_user.save()
                print(f"   ✅ 创建默认用户: {default_user.username}")
            
            # 创建测试学员
            test_students = [
                {'student_id': '2021001', 'name': '张三', 'email': 'zhangsan@example.com'},
                {'student_id': '2021002', 'name': '李四', 'email': 'lisi@example.com'},
                {'student_id': '2022001', 'name': '王五', 'email': 'wangwu@example.com'},
            ]
            
            for student_data in test_students:
                student, created = Student.objects.get_or_create(
                    student_id=student_data['student_id'],
                    defaults={
                        'user': default_user,
                        'name': student_data['name'],
                        'email': student_data['email']
                    }
                )
                if created:
                    print(f"   ✅ 创建学员: {student.name} ({student.student_id})")
                else:
                    print(f"   ℹ️ 学员已存在: {student.name} ({student.student_id})")
        except Exception as e:
            print(f"   ❌ 创建学员失败: {e}")
    else:
        for student in students[:5]:
            print(f"   - ID: {student.id}, 姓名: {student.name}, 学号: {student.student_id}")
    print()
    
    # 3. 检查试卷数据
    print("3. 试卷数据:")
    exams = Exam.objects.all()
    print(f"   总试卷数: {exams.count()}")
    if exams.count() == 0:
        print("   ⚠️ 没有试卷数据，需要创建测试试卷")
        # 创建测试试卷
        try:
            # 获取或创建默认用户
            default_user = User.objects.get(username='default_admin')
            
            # 创建测试试卷
            test_exams = [
                {'title': '数学基础测试', 'description': '测试数学基础知识'},
                {'title': '英语水平测试', 'description': '测试英语水平'},
                {'title': '计算机基础测试', 'description': '测试计算机基础知识'},
            ]
            
            for exam_data in test_exams:
                exam, created = Exam.objects.get_or_create(
                    title=exam_data['title'],
                    defaults={
                        'description': exam_data['description'],
                        'created_by': default_user,
                        'is_active': True
                    }
                )
                if created:
                    print(f"   ✅ 创建试卷: {exam.title}")
                else:
                    print(f"   ℹ️ 试卷已存在: {exam.title}")
        except Exception as e:
            print(f"   ❌ 创建试卷失败: {e}")
    else:
        for exam in exams[:5]:
            print(f"   - ID: {exam.id}, 标题: {exam.title}, 状态: {'启用' if exam.is_active else '禁用'}")
    print()
    
    # 4. 检查试卷分配数据
    print("4. 试卷分配数据:")
    assignments = ExamStudentAssignment.objects.all()
    print(f"   总分配数: {assignments.count()}")
    if assignments.count() == 0:
        print("   ⚠️ 没有分配数据")
        # 创建测试分配
        try:
            students = Student.objects.all()
            exams = Exam.objects.all()
            
            if students.count() > 0 and exams.count() > 0:
                # 为每个学员分配第一个试卷
                for student in students[:3]:  # 只分配前3个学员
                    exam = exams.first()
                    assignment, created = ExamStudentAssignment.objects.get_or_create(
                        exam=exam,
                        student=student,
                        defaults={
                            'assigned_by': User.objects.first(),
                            'is_active': True
                        }
                    )
                    if created:
                        print(f"   ✅ 创建分配: {student.name} -> {exam.title}")
                    else:
                        print(f"   ℹ️ 分配已存在: {student.name} -> {exam.title}")
            else:
                print("   ❌ 没有学员或试卷数据，无法创建分配")
        except Exception as e:
            print(f"   ❌ 创建分配失败: {e}")
    else:
        for assignment in assignments[:5]:
            print(f"   - 试卷: {assignment.exam.title}, 学员: {assignment.student.name}, 状态: {'有效' if assignment.is_active else '已移除'}")
    print()
    
    # 5. 重新统计数据
    print("5. 数据统计:")
    print(f"   学员总数: {Student.objects.count()}")
    print(f"   试卷总数: {Exam.objects.count()}")
    print(f"   分配总数: {ExamStudentAssignment.objects.count()}")
    print(f"   有效分配: {ExamStudentAssignment.objects.filter(is_active=True).count()}")

if __name__ == '__main__':
    check_assignment_data()
