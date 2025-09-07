#!/usr/bin/env python3
"""
考试系统功能测试脚本
"""

import requests
import json
import time

# 配置
BASE_URL = 'http://localhost:8000'
API_BASE = f'{BASE_URL}/api/exams'

def test_exam_system():
    """测试考试系统的主要功能"""
    
    print("=== 考试系统功能测试 ===\n")
    
    # 1. 测试获取考试列表
    print("1. 测试获取考试列表...")
    try:
        response = requests.get(f'{API_BASE}/exams/')
        if response.status_code == 200:
            exams = response.json()
            print(f"   成功获取到 {len(exams)} 个考试")
            for exam in exams[:3]:  # 只显示前3个
                print(f"   - {exam.get('title', 'N/A')} (ID: {exam.get('id', 'N/A')})")
        else:
            print(f"   失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print()
    
    # 2. 测试获取特定考试详情
    print("2. 测试获取考试详情...")
    try:
        response = requests.get(f'{API_BASE}/exams/1/')
        if response.status_code == 200:
            exam = response.json()
            print(f"   成功获取考试: {exam.get('title', 'N/A')}")
            print(f"   题目数量: {len(exam.get('questions', []))}")
            print(f"   描述: {exam.get('description', 'N/A')[:50]}...")
        else:
            print(f"   失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print()
    
    # 3. 测试学员考试列表
    print("3. 测试学员考试列表...")
    try:
        # 假设学员ID为1
        response = requests.get(f'{API_BASE}/exams/?student=1')
        if response.status_code == 200:
            student_exams = response.json()
            print(f"   学员考试数量: {len(student_exams)}")
            for exam in student_exams:
                print(f"   - {exam.get('title', 'N/A')} (状态: {'已完成' if exam.get('has_score') else '待完成'})")
        else:
            print(f"   失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print()
    
    # 4. 测试提交答案（模拟）
    print("4. 测试提交答案...")
    try:
        # 模拟答案数据
        mock_answers = {
            "exam_id": 1,
            "answers": [
                {
                    "question_id": 1,
                    "answer_text": "",
                    "selected_option": 1
                },
                {
                    "question_id": 2,
                    "answer_text": "测试答案",
                    "selected_option": None
                }
            ]
        }
        
        response = requests.post(f'{API_BASE}/student-answers/submit_answers/', 
                               json=mock_answers)
        
        if response.status_code in [201, 400, 403]:
            result = response.json()
            if response.status_code == 201:
                print(f"   提交成功: 得分 {result.get('score', 0)}分")
            else:
                print(f"   提交失败: {result.get('error', '未知错误')}")
        else:
            print(f"   失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print()
    
    # 5. 测试获取成绩
    print("5. 测试获取成绩...")
    try:
        response = requests.get(f'{API_BASE}/scores/')
        if response.status_code == 200:
            scores = response.json()
            print(f"   成绩记录数量: {len(scores)}")
            for score in scores[:3]:  # 只显示前3个
                print(f"   - 考试ID: {score.get('exam', 'N/A')}, 得分: {score.get('total_score', 0)}")
        else:
            print(f"   失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_exam_system()
