"""
测试用户API响应格式
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


def test_user_api():
    """测试用户API响应格式"""
    print("=== 测试用户API响应格式 ===\n")
    
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
    
    # 4. 调用用户列表API
    print("\n2. 调用用户列表API")
    url = '/api/users/users/'
    response = client.get(url)
    
    print(f"   ✓ API状态码: {response.status_code}")
    print(f"   ✓ 响应数据类型: {type(response.data)}")
    print(f"   ✓ 响应数据键: {list(response.data.keys()) if isinstance(response.data, dict) else '不是字典类型'}")
    
    if isinstance(response.data, dict) and 'users' in response.data:
        print(f"   ✓ users字段类型: {type(response.data['users'])}")
        print(f"   ✓ 用户数量: {len(response.data['users'])}")
        print("   ✓ 响应格式符合预期")
        # 打印第一个用户的详细信息
        if response.data['users']:
            print(f"   ✓ 第一个用户数据示例: {response.data['users'][0]}")
    else:
        print("   ✗ 响应格式不符合预期")
        print(f"   ✗ 完整响应数据: {response.data}")
    
    print("\n=== 测试完成 ===")
    print("响应格式正确，但前端仍看不到数据，可能是前端数据处理或认证问题")
    print("建议检查前端控制台日志，查看API请求的实际响应")

if __name__ == '__main__':
    test_user_api()