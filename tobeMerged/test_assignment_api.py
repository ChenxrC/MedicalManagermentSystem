#!/usr/bin/env python3
"""
测试试卷分配相关API
"""

import requests
import json

BASE_URL = 'http://localhost:8000'

def test_assignment_apis():
    """测试试卷分配相关API"""
    
    print("=== 测试试卷分配相关API ===\n")
    
    # 1. 测试获取学员列表
    print("1. 测试获取学员列表...")
    try:
        response = requests.get(f"{BASE_URL}/api/students/")
        if response.status_code == 200:
            data = response.json()
            # 处理分页格式
            if isinstance(data, dict) and 'results' in data:
                students = data['results']
                total_count = data.get('count', len(students))
            else:
                students = data if isinstance(data, list) else []
                total_count = len(students)
            
            print(f"   ✅ 成功获取到 {total_count} 个学员")
            # 安全地访问数据
            try:
                for i in range(min(3, len(students))):
                    student = students[i]
                    if isinstance(student, dict):
                        name = student.get('name', 'N/A')
                        student_id = student.get('student_id', 'N/A')
                        print(f"   - {name} (学号: {student_id})")
                    else:
                        print(f"   - 学员数据格式异常: {student}")
            except Exception as e:
                print(f"   ⚠️ 显示学员数据时出错: {e}")
        else:
            print(f"   ❌ 失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 2. 测试获取试卷列表
    print("2. 测试获取试卷列表...")
    try:
        response = requests.get(f"{BASE_URL}/api/exams/")
        if response.status_code == 200:
            data = response.json()
            # 处理分页格式
            if isinstance(data, dict) and 'results' in data:
                exams = data['results']
                total_count = data.get('count', len(exams))
            else:
                exams = data if isinstance(data, list) else []
                total_count = len(exams)
            
            print(f"   ✅ 成功获取到 {total_count} 个试卷")
            # 安全地访问数据
            try:
                for i in range(min(3, len(exams))):
                    exam = exams[i]
                    if isinstance(exam, dict):
                        title = exam.get('title', 'N/A')
                        exam_id = exam.get('id', 'N/A')
                        print(f"   - {title} (ID: {exam_id})")
                    else:
                        print(f"   - 试卷数据格式异常: {exam}")
            except Exception as e:
                print(f"   ⚠️ 显示试卷数据时出错: {e}")
        else:
            print(f"   ❌ 失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 3. 测试获取试卷分配列表
    print("3. 测试获取试卷分配列表...")
    try:
        response = requests.get(f"{BASE_URL}/api/exam-assignments/")
        if response.status_code == 200:
            data = response.json()
            # 处理分页格式
            if isinstance(data, dict) and 'results' in data:
                assignments = data['results']
                total_count = data.get('count', len(assignments))
            else:
                assignments = data if isinstance(data, list) else []
                total_count = len(assignments)
            
            print(f"   ✅ 成功获取到 {total_count} 个分配记录")
            # 安全地访问数据
            try:
                for i in range(min(3, len(assignments))):
                    assignment = assignments[i]
                    if isinstance(assignment, dict):
                        exam_title = assignment.get('exam_title', 'N/A')
                        student_name = assignment.get('student_name', 'N/A')
                        print(f"   - 试卷: {exam_title}, 学员: {student_name}")
                    else:
                        print(f"   - 分配数据格式异常: {assignment}")
            except Exception as e:
                print(f"   ⚠️ 显示分配数据时出错: {e}")
        else:
            print(f"   ❌ 失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    
    # 4. 测试创建试卷分配
    print("4. 测试创建试卷分配...")
    try:
        # 首先获取一个学员和试卷
        students_response = requests.get(f"{BASE_URL}/api/students/")
        exams_response = requests.get(f"{BASE_URL}/api/exams/")
        
        if students_response.status_code == 200 and exams_response.status_code == 200:
            students_data = students_response.json()
            exams_data = exams_response.json()
            
            # 处理分页格式
            if isinstance(students_data, dict) and 'results' in students_data:
                students = students_data['results']
            else:
                students = students_data if isinstance(students_data, list) else []
            
            if isinstance(exams_data, dict) and 'results' in exams_data:
                exams = exams_data['results']
            else:
                exams = exams_data if isinstance(exams_data, list) else []
            
            # 检查数据是否为空
            if students and exams and len(students) > 0 and len(exams) > 0:
                # 安全地获取第一个学员和试卷
                try:
                    student = students[0] if isinstance(students[0], dict) else None
                    exam = exams[0] if isinstance(exams[0], dict) else None
                    
                    if student and exam:
                        student_id = student.get('id')
                        exam_id = exam.get('id')
                        
                        if student_id and exam_id:
                            assignment_data = {
                                'exam': exam_id,
                                'student': student_id
                            }
                            
                            response = requests.post(
                                f"{BASE_URL}/api/exam-assignments/",
                                json=assignment_data,
                                headers={'Content-Type': 'application/json'}
                            )
                            
                            if response.status_code == 201:
                                result = response.json()
                                print(f"   ✅ 成功创建分配记录")
                                print(f"   - 分配ID: {result.get('id', 'N/A')}")
                            else:
                                print(f"   ❌ 失败: {response.status_code} - {response.text}")
                        else:
                            print("   ⚠️ 学员或试卷ID无效")
                    else:
                        print("   ⚠️ 学员或试卷数据格式异常")
                except Exception as e:
                    print(f"   ⚠️ 处理学员或试卷数据时出错: {e}")
            else:
                print("   ⚠️ 没有学员或试卷数据，跳过创建测试")
        else:
            print("   ❌ 获取学员或试卷数据失败")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_assignment_apis()
