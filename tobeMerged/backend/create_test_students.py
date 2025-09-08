#!/usr/bin/env python
"""
创建测试学员数据
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_viewer.settings')
django.setup()

from django.contrib.auth.models import User
from exams.models import Student

def create_test_students():
    """创建测试学员数据"""
    print("开始创建测试学员数据...")
    
    # 确保有一个默认用户
    try:
        default_user = User.objects.get(username='default_admin')
    except User.DoesNotExist:
        default_user = User.objects.create_user(
            username='default_admin',
            email='admin@example.com',
            password='default123'
        )
        print(f"创建默认用户: {default_user.username}")
    
    # 测试学员数据
    test_students = [
        {
            'student_id': 'user001',
            'name': '张三',
            'email': 'zhangsan@example.com',
            'phone': '13800138001',
            'department': '北京',
            'major': '技术部',
            'grade': '2021级'
        },
        {
            'student_id': 'user002',
            'name': '李四',
            'email': 'lisi@example.com',
            'phone': '13800138002',
            'department': '上海',
            'major': '市场部',
            'grade': '2021级'
        },
        {
            'student_id': 'user003',
            'name': '王五',
            'email': 'wangwu@example.com',
            'phone': '13800138003',
            'department': '深圳',
            'major': '产品部',
            'grade': '2022级'
        },
        {
            'student_id': 'user004',
            'name': '赵六',
            'email': 'zhaoliu@example.com',
            'phone': '13800138004',
            'department': '广州',
            'major': '设计部',
            'grade': '2022级'
        },
        {
            'student_id': 'user005',
            'name': '钱七',
            'email': 'qianqi@example.com',
            'phone': '13800138005',
            'department': '杭州',
            'major': '运营部',
            'grade': '2023级'
        }
    ]
    
    created_count = 0
    for student_data in test_students:
        # 检查学员是否已存在
        if not Student.objects.filter(student_id=student_data['student_id']).exists():
            # 创建用户
            user = User.objects.create_user(
                username=student_data['student_id'],
                email=student_data['email'],
                password='123456'
            )
            
            # 创建学员
            student = Student.objects.create(
                user=user,
                **student_data
            )
            print(f"创建学员: {student.name} ({student.student_id})")
            created_count += 1
        else:
            print(f"学员已存在: {student_data['name']} ({student_data['student_id']})")
    
    print(f"\n完成！创建了 {created_count} 个新学员")
    print(f"数据库中总共有 {Student.objects.count()} 个学员")

if __name__ == '__main__':
    create_test_students()
