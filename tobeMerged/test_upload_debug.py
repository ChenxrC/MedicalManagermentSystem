#!/usr/bin/env python3
"""
调试图片上传功能
"""

import requests
import os

def test_upload_with_debug():
    """测试图片上传并显示详细信息"""
    base_url = "http://localhost:8000"
    upload_url = f"{base_url}/api/exams/questions/upload_image/"
    
    print("🔍 调试图片上传功能...")
    print("=" * 50)
    
    # 创建一个简单的测试图片
    test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xd7\xd4\xc2\x00\x00\x00\x00IEND\xaeB`\x82'
    
    try:
        # 方法1：使用files参数
        print("方法1：使用files参数")
        files = {'image': ('test.png', test_image_data, 'image/png')}
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'multipart/form-data'
        }
        
        response = requests.post(upload_url, files=files, headers=headers)
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 201:
            print("✅ 方法1成功！")
            return True
        else:
            print(f"❌ 方法1失败: {response.status_code}")
        
        # 方法2：使用data参数
        print("\n方法2：使用data参数")
        data = {'image': ('test.png', test_image_data, 'image/png')}
        response2 = requests.post(upload_url, data=data, headers=headers)
        
        print(f"状态码: {response2.status_code}")
        print(f"响应内容: {response2.text}")
        
        if response2.status_code == 201:
            print("✅ 方法2成功！")
            return True
        else:
            print(f"❌ 方法2失败: {response2.status_code}")
            
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return False

def check_django_logs():
    """检查Django日志"""
    print("\n📋 Django日志分析：")
    print("如果看到 '没有找到图片文件' 错误，说明前端没有正确发送文件")
    print("如果看到 '不支持的文件类型' 错误，说明文件类型验证失败")
    print("如果看到 '文件大小不能超过5MB' 错误，说明文件大小超限")

if __name__ == '__main__':
    print("🚀 开始调试图片上传功能...")
    print("=" * 60)
    
    success = test_upload_with_debug()
    
    if success:
        print("\n🎉 测试成功！API端点工作正常。")
        print("问题可能在于前端文件上传配置。")
    else:
        print("\n💥 测试失败，请检查后端配置。")
    
    check_django_logs()
