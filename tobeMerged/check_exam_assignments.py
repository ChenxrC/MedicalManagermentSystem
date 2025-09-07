#!/usr/bin/env python3
"""
检查考试分配情况，诊断403错误
"""

import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_viewer.settings')
django.setup()

from django.contrib.auth.models import User
from exams.models import Student, Exam, ExamStudentAssignment, Score

def check_exam_assignments():
    """检查考试分配情况"""
    
    print("=== 检查考试分配情况 ===\n")
    
    # 1. 检查学员数据
    print("1. 学员数据:")
    students = Student.objects.all()
    print(f"   总学员数: {students.count()}")
    
    if students.count() == 0:
        print("   ❌ 没有学员数据")
        return
    
    for student in students:
        print(f"   - ID: {student.id}, 姓名: {student.name}, 学号: {student.student_id}")
        print(f"     用户名: {student.user.username}, 邮箱: {student.user.email}")
    print()
    
    # 2. 检查考试数据
    print("2. 考试数据:")
    exams = Exam.objects.all()
    print(f"   总考试数: {exams.count()}")
    
    if exams.count() == 0:
        print("   ❌ 没有考试数据")
        return
    
    for exam in exams[:5]:  # 只显示前5个
        print(f"   - ID: {exam.id}, 标题: {exam.title}")
        print(f"     状态: {'启用' if exam.is_active else '禁用'}")
    if exams.count() > 5:
        print(f"   ... 还有 {exams.count() - 5} 个考试")
    print()
    
    # 3. 检查考试分配数据
    print("3. 考试分配数据:")
    assignments = ExamStudentAssignment.objects.all()
    print(f"   总分配数: {assignments.count()}")
    print(f"   有效分配: {assignments.filter(is_active=True).count()}")
    
    if assignments.count() == 0:
        print("   ❌ 没有分配数据")
        print("   💡 需要为学员分配考试才能提交答案")
        return
    
    for assignment in assignments:
        print(f"   - 考试: {assignment.exam.title} (ID: {assignment.exam.id})")
        print(f"     学员: {assignment.student.name} (用户名: {assignment.student.user.username})")
        print(f"     状态: {'有效' if assignment.is_active else '已移除'}")
        print(f"     分配时间: {assignment.assigned_at}")
        print()
    
    # 4. 检查成绩数据
    print("4. 成绩数据:")
    scores = Score.objects.all()
    print(f"   总成绩数: {scores.count()}")
    
    if scores.count() > 0:
        for score in scores[:3]:  # 只显示前3个
            print(f"   - 学员: {score.student.name}, 考试: {score.exam.title}")
            print(f"     得分: {score.total_score}, 提交时间: {score.submitted_at}")
        if scores.count() > 3:
            print(f"   ... 还有 {scores.count() - 3} 个成绩记录")
    else:
        print("   ℹ️ 没有成绩数据")
    print()
    
    # 5. 检查特定用户的分配情况
    print("5. 检查特定用户分配情况:")
    
    # 检查testuser是否存在
    try:
        testuser = User.objects.get(username='testuser')
        print(f"   ✅ 找到用户: testuser (ID: {testuser.id})")
        
        # 检查是否有对应的学员记录
        try:
            test_student = Student.objects.get(user=testuser)
            print(f"   ✅ 找到学员记录: {test_student.name} (ID: {test_student.id})")
            
            # 检查该学员的考试分配
            student_assignments = ExamStudentAssignment.objects.filter(
                student=test_student,
                is_active=True
            )
            print(f"   📊 该学员有 {student_assignments.count()} 个有效分配")
            
            if student_assignments.count() > 0:
                for assignment in student_assignments:
                    print(f"      - 考试: {assignment.exam.title} (ID: {assignment.exam.id})")
                    print(f"        分配时间: {assignment.assigned_at}")
            else:
                print("      ❌ 该学员没有被分配任何考试")
                print("      💡 这就是导致403错误的原因！")
                
        except Student.DoesNotExist:
            print("   ❌ testuser没有对应的学员记录")
            print("   💡 需要创建学员记录或使用其他账号")
            
    except User.DoesNotExist:
        print("   ❌ 没有找到testuser用户")
        print("   💡 需要使用存在的用户账号")
    
    print()
    
    # 6. 推荐测试账号
    print("6. 推荐测试账号:")
    if students.count() > 0:
        print("   可以使用以下学员账号进行测试:")
        for student in students[:3]:
            print(f"   - 用户名: {student.user.username}")
            print(f"     姓名: {student.name}, 学号: {student.student_id}")
            print(f"     邮箱: {student.user.email}")
            print()
    else:
        print("   ❌ 没有可用的学员账号")
    
    # 7. 解决方案
    print("7. 解决方案:")
    print("   如果testuser没有被分配考试，可以:")
    print("   1. 使用其他已分配考试的学员账号")
    print("   2. 为testuser分配考试")
    print("   3. 创建新的测试学员并分配考试")
    print()
    
    print("=== 检查完成 ===")

def create_test_assignment():
    """为testuser创建测试分配"""
    print("=== 为testuser创建测试分配 ===\n")
    
    try:
        # 获取testuser
        testuser = User.objects.get(username='testuser')
        print(f"✅ 找到用户: testuser")
        
        # 获取或创建学员记录
        student, created = Student.objects.get_or_create(
            user=testuser,
            defaults={
                'student_id': 'testuser001',
                'name': '测试学员',
                'email': 'testuser@example.com',
                'department': '测试部门',
                'major': '测试专业',
                'grade': '2024级',
                'phone': '13800138000'
            }
        )
        
        if created:
            print(f"✅ 创建学员记录: {student.name}")
        else:
            print(f"ℹ️ 学员记录已存在: {student.name}")
        
        # 获取第一个启用的考试
        exam = Exam.objects.filter(is_active=True).first()
        if not exam:
            print("❌ 没有启用的考试")
            return
        
        print(f"✅ 找到考试: {exam.title}")
        
        # 检查是否已经分配
        existing_assignment = ExamStudentAssignment.objects.filter(
            exam=exam,
            student=student,
            is_active=True
        ).first()
        
        if existing_assignment:
            print(f"ℹ️ 已经分配过: {exam.title} -> {student.name}")
            return
        
        # 创建分配
        assignment = ExamStudentAssignment.objects.create(
            exam=exam,
            student=student,
            assigned_by=User.objects.first()  # 使用第一个用户作为分配人
        )
        
        print(f"✅ 成功创建分配: {exam.title} -> {student.name}")
        print(f"   分配ID: {assignment.id}")
        print(f"   分配时间: {assignment.assigned_at}")
        
    except User.DoesNotExist:
        print("❌ 没有找到testuser用户")
    except Exception as e:
        print(f"❌ 创建分配失败: {e}")

if __name__ == '__main__':
    check_exam_assignments()
    print("\n" + "="*50 + "\n")
    create_test_assignment()
