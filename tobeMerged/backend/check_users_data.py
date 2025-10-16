"""
检查用户数据和权限配置
"""
import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.join(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_viewer.settings')
django.setup()

from users.models import User, UserRole
from django.contrib.auth.models import Permission


def check_users_data():
    """检查用户数据和权限配置"""
    print("=== 检查用户数据 ===\n")
    
    # 1. 查看所有用户
    print("1. 数据库中的所有用户:")
    users = User.objects.all()
    
    if not users.exists():
        print("   ! 数据库中没有任何用户数据")
    else:
        print(f"   ✓ 找到 {users.count()} 个用户")
        
        for user in users:
            print(f"\n   用户ID: {user.id}")
            print(f"   用户名: {user.username}")
            print(f"   邮箱: {user.email}")
            print(f"   角色: {user.role}")
            print(f"   权限列表: {user.get_permissions()}")
            print(f"   是管理员: {user.is_superuser}")
            print(f"   是员工: {user.is_staff}")
            print(f"   账号状态: {'活跃' if user.is_active else '禁用'}")
    
    print("\n=== 检查管理员账户权限 ===\n")
    
    # 2. 检查管理员账户权限配置
    admin_users = User.objects.filter(role=UserRole.ADMIN)
    
    if not admin_users.exists():
        print("   ! 没有找到管理员账户")
    else:
        print(f"   ✓ 找到 {admin_users.count()} 个管理员账户")
        
        # 3. 尝试直接调用list方法(模拟API调用)
        from users.views import UserViewSet
        from django.test import RequestFactory
        
        # 创建一个模拟请求对象
        factory = RequestFactory()
        request = factory.get('/api/users/users/')
        
        # 为请求设置管理员用户
        for admin in admin_users:
            print(f"\n   测试管理员: {admin.username}")
            request.user = admin
            
            # 创建视图实例
            view = UserViewSet.as_view({'get': 'list'})
            
            try:
                # 检查权限
                view.check_permissions(request)
                print(f"   ✓ 权限检查通过")
                
                # 尝试获取用户列表
                response = view(request)
                user_count = len(response.data.get('users', []))
                print(f"   ✓ 成功获取用户列表，共 {user_count} 个用户")
            except Exception as e:
                print(f"   ✗ 测试失败: {str(e)}")
    
    print("\n=== 检查完成 ===")
    print("如果数据库中没有用户数据，可以运行init_admin_user.py创建管理员账户")
    print("如果权限验证有问题，请检查用户模型和视图集中的权限配置")

if __name__ == '__main__':
    check_users_data()