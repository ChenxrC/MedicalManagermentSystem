#!/usr/bin/env python3
"""
测试多选题功能
"""

import requests
import json

def test_multiple_choice():
    """测试多选题功能"""
    base_url = "http://localhost:8000/api/exams"
    
    print("🚀 开始测试多选题功能...")
    print("=" * 50)
    
    try:
        # 1. 创建试卷
        exam_data = {
            "title": "多选题测试试卷",
            "description": "测试多选题功能"
        }
        response = requests.post(f"{base_url}/exams/", json=exam_data)
        if response.status_code != 201:
            print(f"❌ 创建试卷失败: {response.status_code}")
            return
        
        exam = response.json()
        exam_id = exam['id']
        print(f"✅ 创建试卷成功: ID={exam_id}")
        
        # 2. 创建单选题
        single_choice_data = {
            "exam": exam_id,
            "text": "以下哪个是Python的数据类型？",
            "question_type": "multiple",
            "correct_answer": "list",
            "points": 5
        }
        response = requests.post(f"{base_url}/questions/", json=single_choice_data)
        if response.status_code == 201:
            question = response.json()
            question_id = question['id']
            print(f"✅ 创建单选题成功: ID={question_id}")
            
            # 添加选项
            options = [
                {"question": question_id, "text": "list", "is_correct": True},
                {"question": question_id, "text": "array", "is_correct": False},
                {"question": question_id, "text": "vector", "is_correct": False},
                {"question": question_id, "text": "tuple", "is_correct": False}
            ]
            
            for option in options:
                response = requests.post(f"{base_url}/answeroptions/", json=option)
                if response.status_code == 201:
                    print(f"✅ 添加选项成功: {option['text']}")
                else:
                    print(f"❌ 添加选项失败: {option['text']}")
        
        # 3. 创建多选题
        multiple_choice_data = {
            "exam": exam_id,
            "text": "以下哪些是Python的循环语句？（多选）",
            "question_type": "multiple_choice",
            "correct_answer": "for|while",
            "points": 10
        }
        response = requests.post(f"{base_url}/questions/", json=multiple_choice_data)
        if response.status_code == 201:
            question = response.json()
            question_id = question['id']
            print(f"✅ 创建多选题成功: ID={question_id}")
            
            # 添加选项
            options = [
                {"question": question_id, "text": "for", "is_correct": True},
                {"question": question_id, "text": "while", "is_correct": True},
                {"question": question_id, "text": "do-while", "is_correct": False},
                {"question": question_id, "text": "foreach", "is_correct": False}
            ]
            
            for option in options:
                response = requests.post(f"{base_url}/answeroptions/", json=option)
                if response.status_code == 201:
                    print(f"✅ 添加选项成功: {option['text']}")
                else:
                    print(f"❌ 添加选项失败: {option['text']}")
        
        # 4. 获取问题列表并显示选项
        response = requests.get(f"{base_url}/questions/?exam={exam_id}")
        if response.status_code == 200:
            questions = response.json()
            print(f"\n📋 试卷问题列表:")
            for i, q in enumerate(questions, 1):
                print(f"问题{i}: {q['text']}")
                print(f"  类型: {q['question_type']}")
                print(f"  分值: {q['points']}")
                print(f"  答案: {q['correct_answer']}")
                
                # 获取选项
                options_response = requests.get(f"{base_url}/answeroptions/?question={q['id']}")
                if options_response.status_code == 200:
                    options = options_response.json()
                    if options:
                        print("  选项:")
                        for j, opt in enumerate(options):
                            correct_mark = " ✓" if opt['is_correct'] else ""
                            print(f"    {chr(97+j)}. {opt['text']}{correct_mark}")
                print()
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    print("=" * 50)
    print("🎉 多选题功能测试完成!")

if __name__ == "__main__":
    test_multiple_choice()
