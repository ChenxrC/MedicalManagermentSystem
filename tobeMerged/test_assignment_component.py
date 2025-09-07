#!/usr/bin/env python3
"""
测试AssignmentManagement组件的数据加载
"""

import requests
import json

BASE_URL = 'http://localhost:8000'

def test_assignment_component_data():
    """测试AssignmentManagement组件需要的数据"""
    
    print("=== 测试AssignmentManagement组件数据 ===\n")
    
    # 1. 测试学员数据格式
    print("1. 测试学员数据格式...")
    try:
        response = requests.get(f"{BASE_URL}/api/students/")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'results' in data:
                students = data['results']
                print(f"   ✅ 学员数据格式正确，共 {len(students)} 个学员")
                if students:
                    student = students[0]
                    required_fields = ['id', 'name', 'student_id', 'department', 'grade']
                    missing_fields = [field for field in required_fields if field not in student]
                    if missing_fields:
                        print(f"   ⚠️ 学员数据缺少字段: {missing_fields}")
                    else:
                        print(f"   ✅ 学员数据字段完整")
                        print(f"   - 示例: {student['name']} ({student['student_id']}) - {student['department']} {student['grade']}")
            else:
                print(f"   ❌ 学员数据格式不正确")
        else:
            print(f"   ❌ 获取学员数据失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 2. 测试试卷数据格式
    print("2. 测试试卷数据格式...")
    try:
        response = requests.get(f"{BASE_URL}/api/exams/")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                exams = data
                print(f"   ✅ 试卷数据格式正确，共 {len(exams)} 个试卷")
                if exams:
                    exam = exams[0]
                    required_fields = ['id', 'title', 'is_active']
                    missing_fields = [field for field in required_fields if field not in exam]
                    if missing_fields:
                        print(f"   ⚠️ 试卷数据缺少字段: {missing_fields}")
                    else:
                        print(f"   ✅ 试卷数据字段完整")
                        print(f"   - 示例: {exam['title']} (ID: {exam['id']}, 状态: {'启用' if exam['is_active'] else '禁用'})")
            else:
                print(f"   ❌ 试卷数据格式不正确")
        else:
            print(f"   ❌ 获取试卷数据失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 3. 测试分配数据格式
    print("3. 测试分配数据格式...")
    try:
        response = requests.get(f"{BASE_URL}/api/exam-assignments/")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'results' in data:
                assignments = data['results']
                print(f"   ✅ 分配数据格式正确，共 {len(assignments)} 个分配记录")
                if assignments:
                    assignment = assignments[0]
                    required_fields = ['id', 'exam_title', 'student_name', 'student_id', 'assigned_at', 'is_active']
                    missing_fields = [field for field in required_fields if field not in assignment]
                    if missing_fields:
                        print(f"   ⚠️ 分配数据缺少字段: {missing_fields}")
                    else:
                        print(f"   ✅ 分配数据字段完整")
                        print(f"   - 示例: {assignment['student_name']} -> {assignment['exam_title']} (状态: {'有效' if assignment['is_active'] else '已移除'})")
            else:
                print(f"   ❌ 分配数据格式不正确")
        else:
            print(f"   ❌ 获取分配数据失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 4. 测试创建分配功能
    print("4. 测试创建分配功能...")
    try:
        # 获取第一个学员和试卷
        students_response = requests.get(f"{BASE_URL}/api/students/")
        exams_response = requests.get(f"{BASE_URL}/api/exams/")
        
        if students_response.status_code == 200 and exams_response.status_code == 200:
            students_data = students_response.json()
            exams_data = exams_response.json()
            
            if isinstance(students_data, dict) and 'results' in students_data:
                students = students_data['results']
            else:
                students = students_data if isinstance(students_data, list) else []
            
            if isinstance(exams_data, list):
                exams = exams_data
            else:
                exams = []
            
            if students and exams:
                student = students[0]
                exam = exams[0]
                
                assignment_data = {
                    'exam': exam['id'],
                    'student': student['id'],
                    'assigned_by': 1
                }
                
                response = requests.post(
                    f"{BASE_URL}/api/exam-assignments/",
                    json=assignment_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 201:
                    result = response.json()
                    print(f"   ✅ 创建分配成功")
                    print(f"   - 分配ID: {result.get('id', 'N/A')}")
                    print(f"   - 学员: {student['name']}")
                    print(f"   - 试卷: {exam['title']}")
                else:
                    print(f"   ❌ 创建分配失败: {response.status_code} - {response.text}")
            else:
                print("   ⚠️ 没有学员或试卷数据，跳过创建测试")
        else:
            print("   ❌ 获取学员或试卷数据失败")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_assignment_component_data()
