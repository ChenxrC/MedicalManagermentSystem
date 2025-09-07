#!/usr/bin/env python3
"""
测试学员考试API
"""

import requests
import json

BASE_URL = 'http://localhost:8000'

def test_student_exam_api():
    """测试学员考试API"""
    
    print("=== 测试学员考试API ===\n")
    
    # 1. 测试获取所有考试
    print("1. 测试获取所有考试...")
    try:
        response = requests.get(f"{BASE_URL}/api/exams/")
        if response.status_code == 200:
            exams = response.json()
            print(f"   ✅ 成功获取到 {len(exams)} 个考试")
            for exam in exams[:3]:
                print(f"   - {exam.get('title', 'N/A')} (ID: {exam.get('id', 'N/A')})")
        else:
            print(f"   ❌ 失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 2. 测试获取学员考试（假设学员ID为1）
    print("2. 测试获取学员考试...")
    try:
        response = requests.get(f"{BASE_URL}/api/exams/?student=1")
        if response.status_code == 200:
            student_exams = response.json()
            print(f"   ✅ 成功获取到 {len(student_exams)} 个学员考试")
            for exam in student_exams:
                print(f"   - {exam.get('title', 'N/A')} (状态: {'已完成' if exam.get('has_score') else '待完成'})")
        else:
            print(f"   ❌ 失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 3. 测试获取特定考试详情
    print("3. 测试获取考试详情...")
    try:
        response = requests.get(f"{BASE_URL}/api/exams/1/")
        if response.status_code == 200:
            exam = response.json()
            print(f"   ✅ 成功获取考试: {exam.get('title', 'N/A')}")
            print(f"   - 题目数量: {len(exam.get('questions', []))}")
            print(f"   - 描述: {exam.get('description', 'N/A')[:50]}...")
        else:
            print(f"   ❌ 失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 4. 测试获取学员特定考试详情
    print("4. 测试获取学员特定考试详情...")
    try:
        response = requests.get(f"{BASE_URL}/api/exams/1/for_student/?student=1")
        if response.status_code == 200:
            exam = response.json()
            print(f"   ✅ 成功获取学员考试: {exam.get('title', 'N/A')}")
        elif response.status_code == 403:
            print("   ⚠️ 权限不足 - 学员可能没有被分配这份考试")
        else:
            print(f"   ❌ 失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_student_exam_api()
