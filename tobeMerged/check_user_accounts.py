#!/usr/bin/env python3
"""
查看用户账号信息
"""

import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_viewer.settings')
django.setup()

from django.contrib.auth.models import User
from exams.models import Student

def check_user_accounts():
    """查看用户账号信息"""
    
    print("=== 查看用户账号信息 ===\n")
    
    # 1. 查看所有用户
    print("1. 所有用户账号:")
    users = User.objects.all()
    print(f"   总用户数: {users.count()}")
    
    for user in users:
        print(f"   - ID: {user.id}")
        print(f"     用户名: {user.username}")
        print(f"     邮箱: {user.email}")
        print(f"     姓名: {user.first_name} {user.last_name}")
        print(f"     是否激活: {'是' if user.is_active else '否'}")
        print(f"     是否员工: {'是' if user.is_staff else '否'}")
        print(f"     是否超级用户: {'是' if user.is_superuser else '否'}")
        print(f"     创建时间: {user.date_joined}")
        print()
    
    # 2. 查看学员账号
    print("2. 学员账号:")
    students = Student.objects.all()
    print(f"   总学员数: {students.count()}")
    
    for student in students:
        user = student.user
        print(f"   - 学员ID: {student.id}")
        print(f"     姓名: {student.name}")
        print(f"     学号: {student.student_id}")
        print(f"     用户名: {user.username}")
        print(f"     邮箱: {user.email}")
        print(f"     院系: {student.department}")
        print(f"     专业: {student.major}")
        print(f"     年级: {student.grade}")
        print(f"     电话: {student.phone}")
        print()
    
    # 3. 推荐测试账号
    print("3. 推荐测试账号:")
    if students.count() > 0:
        print("   可以使用以下学员账号进行测试:")
        for student in students[:3]:
            user = student.user
            print(f"   - 用户名: {user.username}")
            print(f"     姓名: {student.name}")
            print(f"     学号: {student.student_id}")
            print(f"     邮箱: {user.email}")
            print()
    else:
        print("   ❌ 没有可用的学员账号")
    
    print("=== 查看完成 ===")

def reset_user_password():
    """重置用户密码"""
    print("=== 重置用户密码 ===\n")
    
    # 获取所有用户
    users = User.objects.all()
    
    if users.count() == 0:
        print("❌ 没有用户账号")
        return
    
    print("可用的用户账号:")
    for i, user in enumerate(users, 1):
        print(f"{i}. {user.username} ({user.email})")
    
    print("\n注意: 出于安全考虑，无法查看现有密码")
    print("建议的操作:")
    print("1. 使用Django管理后台重置密码")
    print("2. 使用Django shell重置密码")
    print("3. 创建新的测试账号")
    
    # 提供重置密码的代码示例
    print("\n重置密码的代码示例:")
    print("```python")
    print("# 在Django shell中执行:")
    print("from django.contrib.auth.models import User")
    print("user = User.objects.get(username='用户名')")
    print("user.set_password('新密码')")
    print("user.save()")
    print("```")

if __name__ == '__main__':
    check_user_accounts()
    print("\n" + "="*50 + "\n")
    reset_user_password()


