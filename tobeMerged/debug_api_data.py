#!/usr/bin/env python3
"""
调试API数据格式
"""

import requests
import json

BASE_URL = 'http://localhost:8000'

def debug_api_data():
    """调试API数据格式"""
    
    print("=== 调试API数据格式 ===\n")
    
    # 1. 调试学员数据
    print("1. 调试学员数据...")
    try:
        response = requests.get(f"{BASE_URL}/api/students/")
        if response.status_code == 200:
            students = response.json()
            print(f"   数据类型: {type(students)}")
            print(f"   数据长度: {len(students)}")
            print(f"   数据内容: {students}")
            
            if len(students) > 0:
                first_student = students[0]
                print(f"   第一个学员类型: {type(first_student)}")
                print(f"   第一个学员内容: {first_student}")
                if isinstance(first_student, dict):
                    print(f"   第一个学员的键: {list(first_student.keys())}")
        else:
            print(f"   ❌ 失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 2. 调试试卷数据
    print("2. 调试试卷数据...")
    try:
        response = requests.get(f"{BASE_URL}/api/exams/")
        if response.status_code == 200:
            exams = response.json()
            print(f"   数据类型: {type(exams)}")
            print(f"   数据长度: {len(exams)}")
            print(f"   数据内容: {exams}")
            
            if len(exams) > 0:
                first_exam = exams[0]
                print(f"   第一个试卷类型: {type(first_exam)}")
                print(f"   第一个试卷内容: {first_exam}")
                if isinstance(first_exam, dict):
                    print(f"   第一个试卷的键: {list(first_exam.keys())}")
        else:
            print(f"   ❌ 失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 3. 调试分配数据
    print("3. 调试分配数据...")
    try:
        response = requests.get(f"{BASE_URL}/api/exam-assignments/")
        if response.status_code == 200:
            assignments = response.json()
            print(f"   数据类型: {type(assignments)}")
            print(f"   数据长度: {len(assignments)}")
            print(f"   数据内容: {assignments}")
            
            if len(assignments) > 0:
                first_assignment = assignments[0]
                print(f"   第一个分配类型: {type(first_assignment)}")
                print(f"   第一个分配内容: {first_assignment}")
                if isinstance(first_assignment, dict):
                    print(f"   第一个分配的键: {list(first_assignment.keys())}")
        else:
            print(f"   ❌ 失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print("\n=== 调试完成 ===")

if __name__ == '__main__':
    debug_api_data()
