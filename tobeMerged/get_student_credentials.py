#!/usr/bin/env python3
"""
获取数据库中学员的账号密码信息
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

def get_student_credentials():
    """获取学员账号密码信息"""
    
    print("=== 获取学员账号密码信息 ===\n")
    
    # 获取所有学员
    students = Student.objects.all()
    
    if not students.exists():
        print("❌ 数据库中没有学员数据")
        return
    
    print(f"✅ 找到 {students.count()} 个学员\n")
    
    # 创建结果列表
    student_info = []
    
    for student in students:
        try:
            # 获取关联的用户账号
            user = student.user
            student_data = {
                'id': student.id,
                'name': student.name,
                'student_id': student.student_id,
                'username': user.username,
                'email': user.email,
                'department': student.department,
                'grade': student.grade,
                'phone': student.phone,
                'major': student.major
            }
            student_info.append(student_data)
            
            print(f"学员 {student.id}: {student.name}")
            print(f"  - 学号: {student.student_id}")
            print(f"  - 用户名: {user.username}")
            print(f"  - 邮箱: {user.email}")
            print(f"  - 院系: {student.department}")
            print(f"  - 年级: {student.grade}")
            print(f"  - 专业: {student.major}")
            print(f"  - 电话: {student.phone}")
            print()
            
        except Exception as e:
            print(f"❌ 获取学员 {student.id} 信息失败: {e}")
            print()
    
    # 生成markdown内容
    markdown_content = generate_markdown(student_info)
    
    # 写入文件
    with open('学员账号密码信息.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print("✅ 学员账号密码信息已保存到 '学员账号密码信息.md' 文件")
    
    return student_info

def generate_markdown(student_info):
    """生成markdown格式的内容"""
    
    content = """# 学员账号密码信息

## 说明
本文档包含数据库中所有学员的账号信息，用于测试系统功能。

## 注意事项
- 密码信息出于安全考虑不在此文档中显示
- 如需重置密码，请联系系统管理员
- 请妥善保管账号信息，不要泄露给他人

## 学员列表

"""
    
    for student in student_info:
        content += f"""### {student['name']} (ID: {student['id']})

| 字段 | 值 |
|------|-----|
| 学号 | {student['student_id']} |
| 用户名 | {student['username']} |
| 邮箱 | {student['email']} |
| 院系 | {student['department']} |
| 年级 | {student['grade']} |
| 专业 | {student['major']} |
| 电话 | {student['phone']} |

**登录信息:**
- 用户名: `{student['username']}`
- 邮箱: `{student['email']}`
- 密码: 请联系管理员获取或重置

---

"""
    
    content += f"""
## 统计信息

- 总学员数: {len(student_info)} 人
- 数据更新时间: {django.utils.timezone.now().strftime('%Y-%m-%d %H:%M:%S')}

## 测试建议

1. **登录测试**: 使用上述用户名和邮箱进行登录测试
2. **权限测试**: 验证学员只能访问自己的考试
3. **功能测试**: 测试学员界面的各项功能
4. **数据一致性**: 验证学员信息在前后端显示一致

## 联系支持

如有问题，请联系系统管理员。
"""
    
    return content

def get_admin_credentials():
    """获取管理员账号信息"""
    
    print("=== 获取管理员账号信息 ===\n")
    
    # 获取超级用户
    superusers = User.objects.filter(is_superuser=True)
    
    if not superusers.exists():
        print("❌ 数据库中没有超级用户")
        return
    
    print(f"✅ 找到 {superusers.count()} 个超级用户\n")
    
    admin_info = []
    
    for admin in superusers:
        admin_data = {
            'id': admin.id,
            'username': admin.username,
            'email': admin.email,
            'first_name': admin.first_name,
            'last_name': admin.last_name,
            'is_staff': admin.is_staff,
            'is_superuser': admin.is_superuser,
            'date_joined': admin.date_joined
        }
        admin_info.append(admin_data)
        
        print(f"管理员 {admin.id}: {admin.username}")
        print(f"  - 用户名: {admin.username}")
        print(f"  - 邮箱: {admin.email}")
        print(f"  - 姓名: {admin.first_name} {admin.last_name}")
        print(f"  - 员工权限: {'是' if admin.is_staff else '否'}")
        print(f"  - 超级用户: {'是' if admin.is_superuser else '否'}")
        print(f"  - 注册时间: {admin.date_joined}")
        print()
    
    return admin_info

if __name__ == '__main__':
    print("开始获取账号信息...\n")
    
    # 获取学员信息
    students = get_student_credentials()
    
    print("\n" + "="*50 + "\n")
    
    # 获取管理员信息
    admins = get_admin_credentials()
    
    print("\n=== 获取完成 ===")
    print("请查看生成的 '学员账号密码信息.md' 文件获取详细信息")
