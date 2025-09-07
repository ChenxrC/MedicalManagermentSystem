#!/usr/bin/env python3
"""
测试图片上传API端点
"""

import requests
import os

def test_image_upload():
    """测试图片上传功能"""
    base_url = "http://localhost:8000"
    
    print("🧪 测试图片上传API端点...")
    print("=" * 50)
    
    # 1. 测试API端点是否存在
    print("1. 检查API端点...")
    try:
        response = requests.get(f"{base_url}/api/exams/questions/")
        if response.status_code == 200:
            print("✅ API端点可访问")
        else:
            print(f"❌ API端点返回状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到API: {e}")
        return False
    
    # 2. 测试图片上传端点
    print("\n2. 测试图片上传端点...")
    upload_url = f"{base_url}/api/exams/questions/upload_image/"
    
    try:
        # 创建一个简单的测试图片（1x1像素的PNG）
        test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xd7\xd4\xc2\x00\x00\x00\x00IEND\xaeB`\x82'
        
        files = {'image': ('test.png', test_image_data, 'image/png')}
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        
        response = requests.post(upload_url, files=files, headers=headers)
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 201:
            print("✅ 图片上传成功！")
            data = response.json()
            print(f"图片URL: {data.get('image_url', 'N/A')}")
            return True
        else:
            print(f"❌ 图片上传失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return False

def test_django_server():
    """检查Django服务器是否运行"""
    print("🔍 检查Django服务器状态...")
    
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ Django服务器正在运行")
            return True
        else:
            print(f"⚠️ Django服务器返回状态码: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Django服务器未运行")
        print("请先启动Django服务器：")
        print("cd backend")
        print(".\\venv\\Scripts\\Activate.ps1")
        print("python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ 检查服务器时出现错误: {e}")
        return False

if __name__ == '__main__':
    print("🚀 开始测试图片上传功能...")
    print("=" * 60)
    
    # 检查服务器状态
    if not test_django_server():
        exit(1)
    
    # 测试图片上传
    if test_image_upload():
        print("\n🎉 所有测试通过！图片上传功能正常工作。")
    else:
        print("\n💥 测试失败，请检查配置。")
