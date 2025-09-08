#!/usr/bin/env python3
"""
测试提交答案API
"""

import requests
import json

BASE_URL = 'http://localhost:8000'

def test_submit_answers_api():
    """测试提交答案API"""
    
    print("=== 测试提交答案API ===\n")
    
    # 1. 首先获取学员信息
    print("1. 获取学员信息...")
    try:
        response = requests.get(f"{BASE_URL}/api/students/")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'results' in data:
                students = data['results']
                if students:
                    student = students[0]
                    print(f"   ✅ 获取到学员: {student['name']} (ID: {student['id']})")
                    student_id = student['id']
                else:
                    print("   ❌ 没有学员数据")
                    return
            else:
                print("   ❌ 学员数据格式错误")
                return
        else:
            print(f"   ❌ 获取学员信息失败: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return
    
    print()
    
    # 2. 获取考试信息
    print("2. 获取考试信息...")
    try:
        response = requests.get(f"{BASE_URL}/api/exams/")
        if response.status_code == 200:
            exams = response.json()
            if isinstance(exams, list) and exams:
                exam = exams[0]
                print(f"   ✅ 获取到考试: {exam['title']} (ID: {exam['id']})")
                exam_id = exam['id']
                
                # 获取考试题目
                if 'questions' in exam and exam['questions']:
                    questions = exam['questions']
                    print(f"   - 题目数量: {len(questions)}")
                    exam_id = exam['id']
                else:
                    print("   ⚠️ 考试没有题目")
                    return
            else:
                print("   ❌ 没有考试数据")
                return
        else:
            print(f"   ❌ 获取考试信息失败: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return
    
    print()
    
    # 3. 测试提交答案API
    print("3. 测试提交答案API...")
    try:
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
        
        print(f"   - 提交数据: {json.dumps(submit_data, ensure_ascii=False, indent=2)}")
        
        # 测试API路径
        api_url = f"{BASE_URL}/api/student-answers/submit_answers/"
        print(f"   - API路径: {api_url}")
        
        response = requests.post(
            api_url,
            json=submit_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   - 响应状态: {response.status_code}")
        print(f"   - 响应内容: {response.text}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ 提交成功")
            print(f"   - 得分: {result.get('score', 'N/A')}")
            print(f"   - 总题目数: {result.get('total_questions', 'N/A')}")
            print(f"   - 已答题目数: {result.get('answered_questions', 'N/A')}")
        elif response.status_code == 403:
            print(f"   ⚠️ 权限不足: {response.json().get('error', '未知错误')}")
        elif response.status_code == 400:
            print(f"   ⚠️ 请求错误: {response.json().get('error', '未知错误')}")
        else:
            print(f"   ❌ 提交失败: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 4. 测试错误的API路径
    print("4. 测试错误的API路径...")
    try:
        wrong_url = f"{BASE_URL}/api/exams/student-answers/submit_answers/"
        print(f"   - 错误路径: {wrong_url}")
        
        response = requests.post(
            wrong_url,
            json=submit_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   - 响应状态: {response.status_code}")
        
        if response.status_code == 404:
            print(f"   ✅ 正确返回404错误（路径不存在）")
        else:
            print(f"   ⚠️ 意外响应: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_submit_answers_api()
