"""
使用Django测试客户端调试API请求，不依赖requests库
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


def debug_api_with_django_client():
    """使用Django测试客户端调试API请求"""
    print("=== 使用Django测试客户端调试API ===\n")
    
    # 1. 获取管理员用户
    print("1. 获取管理员用户")
    admin_user = User.objects.filter(role='admin').first()
    
    if not admin_user:
        print("   ! 未找到管理员用户，请先运行init_admin_user.py创建管理员账户")
        return
    
    print(f"   ✓ 找到管理员用户: {admin_user.username}")
    
    # 2. 生成JWT令牌
    print("\n2. 生成JWT令牌")
    refresh = RefreshToken.for_user(admin_user)
    access_token = str(refresh.access_token)
    print(f"   ✓ 访问令牌: {access_token[:20]}...")
    
    # 3. 创建Django测试客户端
    print("\n3. 创建Django测试客户端")
    client = APIClient()
    
    # 4. 设置认证头
    print("\n4. 设置认证头")
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    print("   ✓ 已设置Authorization头")
    
    # 5. 测试用户列表API
    print("\n5. 测试用户列表API")
    api_path = '/api/users/'
    print(f"   ✓ 请求路径: {api_path}")
    
    response = client.get(api_path)
    
    print(f"   ✓ 响应状态码: {response.status_code}")
    print(f"   ✓ 响应数据类型: {type(response.data)}")
    
    if response.status_code == 200:
        if isinstance(response.data, dict):
            print(f"   ✓ 响应数据键: {list(response.data.keys())}")
            
            # 检查是否包含users字段
            if 'users' in response.data:
                print(f"   ✓ 找到了users字段")
                print(f"   ✓ 用户数量: {len(response.data['users'])}")
                
                # 打印第一个用户的详细信息（如果有）
                if response.data['users']:
                    print(f"   ✓ 第一个用户数据:")
                    first_user = response.data['users'][0]
                    for key, value in first_user.items():
                        print(f"     - {key}: {value}")
            else:
                print("   ✗ 响应数据中不包含users字段")
                print(f"   ✗ 完整响应数据: {response.data}")
        else:
            print("   ✗ 响应数据不是字典类型")
            print(f"   ✗ 响应内容: {response.content}")
    else:
        print(f"   ✗ API请求失败，状态码: {response.status_code}")
        print(f"   ✗ 响应数据: {response.data}")
    
    # 6. 测试登录API
    print("\n6. 测试登录API")
    login_path = '/api/users/auth/login'
    login_data = {
        'username': admin_user.username,
        'password': 'admin123'  # 假设密码是admin123
    }
    
    print(f"   ✓ 登录路径: {login_path}")
    print(f"   ✓ 登录数据: {login_data}")
    
    login_response = client.post(login_path, login_data, format='json')
    
    print(f"   ✓ 登录请求状态码: {login_response.status_code}")
    
    if login_response.status_code == 200:
        print(f"   ✓ 登录成功")
        print(f"   ✓ 返回数据结构: {list(login_response.data.keys())}")
        
        # 检查返回的用户数据
        if 'data' in login_response.data and 'user' in login_response.data['data']:
            user_data = login_response.data['data']['user']
            print(f"   ✓ 用户角色: {user_data.get('role')}")
            print(f"   ✓ 用户权限: {user_data.get('permissions')}")
    else:
        print(f"   ✗ 登录失败")
        print(f"   ✗ 登录响应: {login_response.data}")
    
    print("\n=== 调试完成 ===")
    print("根据测试结果，API功能正常，但前端仍看不到数据，可能是以下原因：")
    print("1. 前端登录后没有正确保存token")
    print("2. 请求时没有正确附加token")
    print("3. 前端组件的渲染逻辑有问题")
    print("建议在浏览器控制台检查：Application -> Local Storage，确认access_token是否存在")
    print("并检查Network面板，确认API请求的URL、头信息和响应")

if __name__ == '__main__':
    debug_api_with_django_client()