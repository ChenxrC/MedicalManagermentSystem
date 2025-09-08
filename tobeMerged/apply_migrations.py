#!/usr/bin/env python3
"""
手动应用数据库迁移的脚本
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def apply_migrations():
    """应用数据库迁移"""
    # 设置Django环境
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_viewer.settings')
    
    # 切换到backend目录
    backend_dir = os.path.join(os.getcwd(), 'backend')
    if os.path.exists(backend_dir):
        os.chdir(backend_dir)
    
    # 初始化Django
    django.setup()
    
    print("🚀 开始应用数据库迁移...")
    
    try:
        # 应用所有迁移
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ 数据库迁移应用成功！")
        
        # 专门应用exams应用的迁移
        execute_from_command_line(['manage.py', 'migrate', 'exams'])
        print("✅ exams应用迁移应用成功！")
        
        # 显示迁移状态
        print("\n📋 当前迁移状态：")
        execute_from_command_line(['manage.py', 'showmigrations'])
        
    except Exception as e:
        print(f"❌ 迁移过程中出现错误: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = apply_migrations()
    if success:
        print("\n🎉 所有迁移应用完成！现在可以重新启动Django服务器。")
    else:
        print("\n💥 迁移失败，请检查错误信息。")
