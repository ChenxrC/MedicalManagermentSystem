"""
验证用户API路径是否正确
"""
import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.join(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_viewer.settings')
django.setup()

from users.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


def verify_user_api_path():
    """验证用户API路径是否正确"""
    print("=== 验证用户API路径 ===\n")
    
    # 1. 创建测试客户端
    client = APIClient()
    
    # 2. 获取管理员用户的JWT令牌
    print("1. 获取管理员用户的JWT令牌")
    admin_user = User.objects.filter(role='admin').first()
    
    if not admin_user:
        print("   ! 未找到管理员用户")
        return
    
    # 生成JWT令牌
    refresh = RefreshToken.for_user(admin_user)
    access_token = str(refresh.access_token)
    print(f"   ✓ 生成令牌成功: {access_token[:20]}...")
    
    # 3. 设置Authorization头
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    # 4. 测试正确的API路径: /api/users/
    print("\n2. 测试正确的API路径: /api/users/")
    url = '/api/users/'
    response = client.get(url)
    
    print(f"   ✓ 状态码: {response.status_code}")
    print(f"   ✓ 响应数据类型: {type(response.data)}")
    
    if response.status_code == 200:
        if isinstance(response.data, dict) and 'users' in response.data:
            print(f"   ✓ 找到了users字段，包含 {len(response.data['users'])} 个用户")
            print("   ✓ API路径验证成功！")
        else:
            print(f"   ✗ 响应数据不包含users字段: {list(response.data.keys()) if isinstance(response.data, dict) else '不是字典类型'}")
            print(f"   ✗ 完整响应数据: {response.data}")
    else:
        print(f"   ✗ API请求失败，状态码: {response.status_code}")
        print(f"   ✗ 响应数据: {response.data}")
    
    print("\n=== 验证完成 ===")
    print("前端已更新为使用正确的API路径: /api/users/")
    print("请登录系统，访问人员管理页面查看是否能显示用户列表")

if __name__ == '__main__':
    verify_user_api_path()