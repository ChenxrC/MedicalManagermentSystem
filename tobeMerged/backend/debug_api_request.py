"""
模拟前端API请求，调试人员管理系统显示为空的问题
"""
import os
import sys
import django
import requests
import json

# 设置Django环境
sys.path.append(os.path.join(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_viewer.settings')
django.setup()

from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


def debug_api_request():
    """模拟前端API请求，调试人员管理系统显示为空的问题"""
    print("=== 调试API请求 ===\n")
    
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
    
    # 3. 模拟前端请求方式 - 测试用户列表API
    print("\n3. 模拟前端请求方式 - 测试用户列表API")
    
    # 后端API地址
    api_url = 'http://localhost:8000/api/users/'
    print(f"   ✓ 请求地址: {api_url}")
    
    # 请求头，模拟前端axios配置
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    try:
        # 发送GET请求
        response = requests.get(api_url, headers=headers, timeout=10)
        
        print(f"   ✓ 响应状态码: {response.status_code}")
        
        # 尝试解析JSON响应
        try:
            data = response.json()
            print(f"   ✓ 响应数据类型: {type(data)}")
            
            # 检查响应数据结构
            if isinstance(data, dict):
                print(f"   ✓ 响应数据键: {list(data.keys())}")
                
                # 检查是否包含users字段
                if 'users' in data:
                    print(f"   ✓ 找到了users字段")
                    print(f"   ✓ 用户数量: {len(data['users'])}")
                    
                    # 打印第一个用户的详细信息（如果有）
                    if data['users']:
                        print(f"   ✓ 第一个用户数据:")
                        first_user = data['users'][0]
                        for key, value in first_user.items():
                            print(f"     - {key}: {value}")
                else:
                    print("   ✗ 响应数据中不包含users字段")
                    print(f"   ✗ 完整响应数据: {data}")
            else:
                print("   ✗ 响应数据不是字典类型")
                print(f"   ✗ 响应内容: {response.text}")
                
        except json.JSONDecodeError:
            print("   ✗ 无法解析JSON响应")
            print(f"   ✗ 响应内容: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ✗ 请求失败: {str(e)}")
        print("   ✗ 请确保后端服务器正在运行")
    
    # 4. 测试登录API，模拟用户登录流程
    print("\n4. 测试登录API，模拟用户登录流程")
    
    login_url = 'http://localhost:8000/api/users/auth/login'
    login_data = {
        'username': admin_user.username,
        'password': 'admin123'  # 假设密码是admin123
    }
    
    try:
        login_response = requests.post(login_url, json=login_data, headers={'Content-Type': 'application/json'}, timeout=10)
        
        print(f"   ✓ 登录请求状态码: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            print(f"   ✓ 登录成功")
            print(f"   ✓ 返回数据结构: {list(login_data.keys())}")
        else:
            print(f"   ✗ 登录失败")
            print(f"   ✗ 登录响应: {login_response.text}")
            
    except Exception as e:
        print(f"   ✗ 登录请求失败: {str(e)}")
    
    print("\n=== 调试完成 ===")
    print("如果所有测试都通过，但前端仍看不到数据，请检查前端的登录状态和token存储是否正确")
    print("建议在浏览器控制台查看网络请求和token信息")

if __name__ == '__main__':
    debug_api_request()