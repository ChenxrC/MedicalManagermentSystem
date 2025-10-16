"""
初始化管理员用户
此脚本用于确保系统中有一个具有管理员权限的账户
"""
import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.join(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_viewer.settings')
django.setup()

from users.models import User, UserRole
from django.contrib.auth.models import User as DjangoUser

def init_admin_user():
    """初始化管理员用户"""
    print("=== 初始化管理员用户 ===\n")
    
    # 1. 检查是否已有管理员用户
    print("1. 检查现有管理员用户:")
    admin_users = User.objects.filter(role=UserRole.ADMIN)
    
    if admin_users.exists():
        print(f"   ✓ 已存在 {admin_users.count()} 个管理员用户:")
        for user in admin_users:
            print(f"     - {user.username} (邮箱: {user.email})")
        print()
    else:
        print("   ! 未找到管理员用户，将创建一个新的管理员账户\n")
    
    # 2. 确保至少有一个可登录的管理员账户
    print("2. 确保有一个默认管理员账户:")
    
    # 检查default_admin是否存在
    try:
        admin_user = User.objects.get(username='default_admin')
        print(f"   ✓ 找到default_admin账户")
        
        # 检查角色是否正确
        if admin_user.role != UserRole.ADMIN:
            print(f"   ! 当前角色: {admin_user.role}，需要修改为admin")
            admin_user.role = UserRole.ADMIN
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            print(f"   ✓ 已更新角色为admin")
        else:
            print(f"   ✓ 角色已正确设置为admin")
        
        # 重置密码
        admin_user.set_password('admin123')
        admin_user.save()
        print("   ✓ 已重置密码为: admin123")
        
    except User.DoesNotExist:
        # 创建管理员用户
        print("   ! default_admin账户不存在，创建新的管理员账户")
        admin_user = User.objects.create_user(
            username='default_admin',
            email='admin@example.com',
            password='admin123'
        )
        
        # 设置为管理员角色
        admin_user.role = UserRole.ADMIN
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        
        print(f"   ✓ 已创建管理员账户: default_admin")
        print(f"   ✓ 用户名: default_admin")
        print(f"   ✓ 密码: admin123")
        print(f"   ✓ 邮箱: admin@example.com")
    
    print()
    print("=== 管理员用户初始化完成 ===")
    print("请使用以下凭据登录系统：")
    print("用户名: default_admin")
    print("密码: admin123")
    print("登录后即可看到管理中心菜单")

if __name__ == '__main__':
    init_admin_user()