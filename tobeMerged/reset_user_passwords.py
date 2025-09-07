#!/usr/bin/env python3
"""
重置用户密码
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

def reset_user_passwords():
    """重置用户密码"""
    
    print("=== 重置用户密码 ===\n")
    
    # 1. 查看现有用户
    print("1. 现有用户账号:")
    users = User.objects.all()
    print(f"   总用户数: {users.count()}")
    
    for user in users:
        print(f"   - {user.username} ({user.email})")
    print()
    
    # 2. 重置学员密码
    print("2. 重置学员密码:")
    students = Student.objects.all()
    
    if students.count() == 0:
        print("   ❌ 没有学员账号")
        return
    
    # 为每个学员重置密码
    for student in students:
        user = student.user
        # 设置密码为用户名
        new_password = user.username
        user.set_password(new_password)
        user.save()
        
        print(f"   ✅ 重置 {student.name} 的密码")
        print(f"      用户名: {user.username}")
        print(f"      新密码: {new_password}")
        print()
    
    # 3. 重置管理员密码
    print("3. 重置管理员密码:")
    admin_users = User.objects.filter(is_staff=True)
    
    for admin_user in admin_users:
        new_password = "admin123"
        admin_user.set_password(new_password)
        admin_user.save()
        
        print(f"   ✅ 重置管理员 {admin_user.username} 的密码")
        print(f"      用户名: {admin_user.username}")
        print(f"      新密码: {new_password}")
        print()
    
    # 4. 创建测试账号
    print("4. 创建测试账号:")
    
    # 检查testuser是否存在
    try:
        testuser = User.objects.get(username='testuser')
        print("   ℹ️ testuser已存在，重置密码")
        testuser.set_password('testuser123')
        testuser.save()
        print("   ✅ testuser密码已重置为: testuser123")
    except User.DoesNotExist:
        # 创建testuser
        testuser = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testuser123'
        )
        print("   ✅ 创建testuser账号")
        print("      用户名: testuser")
        print("      密码: testuser123")
        
        # 创建对应的学员记录
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
            print("   ✅ 创建testuser学员记录")
        else:
            print("   ℹ️ testuser学员记录已存在")
    
    print()
    
    # 5. 显示所有可用账号
    print("5. 可用测试账号:")
    print("   学员账号:")
    for student in students:
        user = student.user
        print(f"   - 用户名: {user.username}")
        print(f"     密码: {user.username}")
        print(f"     姓名: {student.name}")
        print()
    
    print("   管理员账号:")
    for admin_user in admin_users:
        print(f"   - 用户名: {admin_user.username}")
        print(f"     密码: admin123")
        print()
    
    print("   测试账号:")
    print(f"   - 用户名: testuser")
    print(f"     密码: testuser123")
    print()
    
    print("=== 密码重置完成 ===")
    print("\n💡 提示:")
    print("1. 学员密码已重置为用户名")
    print("2. 管理员密码已重置为 admin123")
    print("3. testuser密码已设置为 testuser123")
    print("4. 现在可以使用这些账号进行测试")

if __name__ == '__main__':
    reset_user_passwords()
