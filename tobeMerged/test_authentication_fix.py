#!/usr/bin/env python3
"""
测试认证修复
"""

import requests
import json

BASE_URL = 'http://localhost:8000'

def test_authentication_fix():
    """测试认证修复"""
    
    print("=== 测试认证修复 ===\n")
    
    # 创建会话对象来保持cookies
    session = requests.Session()
    
    # 1. 测试登录API
    print("1. 测试登录API...")
    try:
        login_data = {
            'username': 'user001',  # 使用已知的学员账号
            'password': 'user001'  # 使用已知的密码
        }
        
        response = session.post(
            f"{BASE_URL}/api/auth/login/",
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   - 响应状态: {response.status_code}")
        print(f"   - 响应内容: {response.text}")
        
        if response.status_code == 200:
            print(f"   ✅ 登录成功")
            user_data = response.json()
            print(f"   - 用户ID: {user_data['user']['id']}")
            print(f"   - 用户名: {user_data['user']['username']}")
            print(f"   - 学员姓名: {user_data['user']['student_profile']['name']}")
        else:
            print(f"   ❌ 登录失败")
            return
            
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return
    
    print()
    
    # 2. 测试获取用户信息API
    print("2. 测试获取用户信息API...")
    try:
        response = session.get(f"{BASE_URL}/api/auth/user-info/")
        
        print(f"   - 响应状态: {response.status_code}")
        print(f"   - 响应内容: {response.text}")
        
        if response.status_code == 200:
            print(f"   ✅ 获取用户信息成功")
        else:
            print(f"   ❌ 获取用户信息失败")
            
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 3. 测试提交答案API（已认证）
    print("3. 测试提交答案API（已认证）...")
    try:
        # 首先获取考试信息
        exam_response = session.get(f"{BASE_URL}/api/exams/")
        if exam_response.status_code == 200:
            exams = exam_response.json()
            if exams:
                exam_id = exams[0]['id']
                print(f"   - 使用考试ID: {exam_id}")
                
                # 构造测试数据
                submit_data = {
                    'exam_id': exam_id,
                    'answers': [
                        {
                            'question_id': 1,
                            'answer_text': '测试答案',
                            'selected_option': None
                        }
                    ]
                }
                
                response = session.post(
                    f"{BASE_URL}/api/student-answers/submit_answers/",
                    json=submit_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                print(f"   - 响应状态: {response.status_code}")
                print(f"   - 响应内容: {response.text}")
                
                if response.status_code == 201:
                    print(f"   ✅ 提交答案成功")
                elif response.status_code == 403:
                    print(f"   ⚠️ 权限不足（可能没有分配考试）")
                elif response.status_code == 400:
                    print(f"   ⚠️ 请求错误: {response.json().get('error', '未知错误')}")
                else:
                    print(f"   ❌ 提交失败: {response.status_code}")
            else:
                print(f"   ⚠️ 没有考试数据")
        else:
            print(f"   ❌ 获取考试信息失败: {exam_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 4. 测试登出API
    print("4. 测试登出API...")
    try:
        response = session.post(f"{BASE_URL}/api/auth/logout/")
        
        print(f"   - 响应状态: {response.status_code}")
        print(f"   - 响应内容: {response.text}")
        
        if response.status_code == 200:
            print(f"   ✅ 登出成功")
        else:
            print(f"   ❌ 登出失败")
            
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 5. 测试提交答案API（未认证）
    print("5. 测试提交答案API（未认证）...")
    try:
        submit_data = {
            'exam_id': 1,
            'answers': []
        }
        
        response = session.post(
            f"{BASE_URL}/api/student-answers/submit_answers/",
            json=submit_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   - 响应状态: {response.status_code}")
        print(f"   - 响应内容: {response.text}")
        
        if response.status_code == 401:
            print(f"   ✅ 正确返回401（未认证）")
        else:
            print(f"   ⚠️ 意外响应: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print("\n=== 测试完成 ===")
    print("\n📝 修复说明:")
    print("1. 添加了会话认证支持")
    print("2. 创建了登录/登出/用户信息API")
    print("3. 修复了前端认证状态管理")
    print("4. 配置了正确的权限类")
    print("5. 使用会话保持认证状态")

if __name__ == '__main__':
    test_authentication_fix()
