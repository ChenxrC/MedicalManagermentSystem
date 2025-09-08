#!/usr/bin/env python
"""
简化的API测试脚本
"""
import requests
import json

BASE_URL = 'http://localhost:8000'

def test_student_api():
    """测试学员API"""
    print("测试学员API...")
    
    # 测试获取学员列表
    try:
        response = requests.get(f'{BASE_URL}/api/students/')
        print(f"GET /api/students/ - 状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"学员数量: {len(data) if isinstance(data, list) else len(data.get('results', []))}")
            print(f"数据格式: {type(data)}")
            if isinstance(data, list) and len(data) > 0:
                print(f"第一个学员: {data[0]}")
            elif isinstance(data, dict) and data.get('results'):
                print(f"第一个学员: {data['results'][0]}")
        else:
            print(f"错误响应: {response.text}")
            
    except Exception as e:
        print(f"请求失败: {e}")

def test_create_student():
    """测试创建学员"""
    print("\n测试创建学员...")
    
    student_data = {
        'student_id': 'test001',
        'name': '测试学员',
        'email': 'test@example.com',
        'phone': '13800138000',
        'department': '北京',
        'major': '测试部',
        'grade': '2024级'
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/students/',
            json=student_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"POST /api/students/ - 状态码: {response.status_code}")
        
        if response.status_code == 201:
            print("学员创建成功")
            print(f"响应数据: {response.json()}")
        else:
            print(f"创建失败: {response.text}")
            
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == '__main__':
    test_student_api()
    test_create_student()
