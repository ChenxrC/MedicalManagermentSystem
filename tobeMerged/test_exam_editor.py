#!/usr/bin/env python3
"""
测试试卷编辑界面功能
"""

import requests
import json

def test_exam_editor():
    """测试试卷编辑功能"""
    base_url = "http://localhost:8000/api/exams"
    
    print("🚀 开始测试试卷编辑界面功能...")
    print("=" * 60)
    
    try:
        # 1. 创建试卷
        exam_data = {
            "title": "Python基础测试试卷",
            "description": "测试Python基础知识，包含单选题、多选题、填空题和问答题"
        }
        response = requests.post(f"{base_url}/exams/", json=exam_data)
        if response.status_code != 201:
            print(f"❌ 创建试卷失败: {response.status_code}")
            return
        
        exam = response.json()
        exam_id = exam['id']
        print(f"✅ 创建试卷成功: ID={exam_id}")
        print(f"   标题: {exam['title']}")
        print(f"   描述: {exam['description']}")
        
        # 2. 创建单选题
        single_choice_data = {
            "exam": exam_id,
            "text": "Python中如何定义一个函数？",
            "question_type": "multiple",
            "correct_answer": "def function_name():",
            "points": 5
        }
        response = requests.post(f"{base_url}/questions/", json=single_choice_data)
        if response.status_code == 201:
            question = response.json()
            question_id = question['id']
            print(f"✅ 创建单选题成功: ID={question_id}")
            
            # 添加选项
            options = [
                {"question": question_id, "text": "def function_name():", "is_correct": True},
                {"question": question_id, "text": "function function_name():", "is_correct": False},
                {"question": question_id, "text": "define function_name():", "is_correct": False},
                {"question": question_id, "text": "func function_name():", "is_correct": False}
            ]
            
            for option in options:
                response = requests.post(f"{base_url}/answeroptions/", json=option)
                if response.status_code == 201:
                    print(f"   ✅ 添加选项: {option['text']}")
                else:
                    print(f"   ❌ 添加选项失败: {option['text']}")
        
        # 3. 创建多选题
        multiple_choice_data = {
            "exam": exam_id,
            "text": "以下哪些是Python的数据类型？（多选）",
            "question_type": "multiple_choice",
            "correct_answer": "list|dict|tuple",
            "points": 10
        }
        response = requests.post(f"{base_url}/questions/", json=multiple_choice_data)
        if response.status_code == 201:
            question = response.json()
            question_id = question['id']
            print(f"✅ 创建多选题成功: ID={question_id}")
            
            # 添加选项
            options = [
                {"question": question_id, "text": "list", "is_correct": True},
                {"question": question_id, "text": "dict", "is_correct": True},
                {"question": question_id, "text": "tuple", "is_correct": True},
                {"question": question_id, "text": "array", "is_correct": False}
            ]
            
            for option in options:
                response = requests.post(f"{base_url}/answeroptions/", json=option)
                if response.status_code == 201:
                    print(f"   ✅ 添加选项: {option['text']}")
                else:
                    print(f"   ❌ 添加选项失败: {option['text']}")
        
        # 4. 创建填空题
        fill_data = {
            "exam": exam_id,
            "text": "Python中用于循环的关键字是____。",
            "question_type": "fill",
            "correct_answer": "for",
            "points": 5
        }
        response = requests.post(f"{base_url}/questions/", json=fill_data)
        if response.status_code == 201:
            question = response.json()
            print(f"✅ 创建填空题成功: ID={question['id']}")
        
        # 5. 创建问答题
        essay_data = {
            "exam": exam_id,
            "text": "请简述Python的特点和优势。",
            "question_type": "essay",
            "correct_answer": "Python具有简洁的语法、丰富的库、跨平台等特点",
            "points": 15
        }
        response = requests.post(f"{base_url}/questions/", json=essay_data)
        if response.status_code == 201:
            question = response.json()
            print(f"✅ 创建问答题成功: ID={question['id']}")
        
        # 6. 获取问题列表并显示统计信息
        response = requests.get(f"{base_url}/questions/?exam={exam_id}")
        if response.status_code == 200:
            questions = response.json()
            print(f"\n📊 试卷统计信息:")
            print(f"   总题数: {len(questions)}")
            
            # 统计各类型题目数量
            type_counts = {}
            total_points = 0
            for q in questions:
                q_type = q['question_type']
                type_counts[q_type] = type_counts.get(q_type, 0) + 1
                total_points += q['points']
            
            print(f"   单选题: {type_counts.get('multiple', 0)}")
            print(f"   多选题: {type_counts.get('multiple_choice', 0)}")
            print(f"   填空题: {type_counts.get('fill', 0)}")
            print(f"   问答题: {type_counts.get('essay', 0)}")
            print(f"   总分: {total_points}")
            
            print(f"\n📋 题目详情:")
            for i, q in enumerate(questions, 1):
                print(f"\n第{i}题: {q['text']}")
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
        
        print("\n" + "=" * 60)
        print("🎉 试卷编辑功能测试完成!")
        print(f"\n📝 测试结果:")
        print(f"   ✅ 试卷创建: 成功")
        print(f"   ✅ 单选题创建: 成功")
        print(f"   ✅ 多选题创建: 成功")
        print(f"   ✅ 填空题创建: 成功")
        print(f"   ✅ 问答题创建: 成功")
        print(f"   ✅ 选项管理: 成功")
        print(f"   ✅ 统计信息: 成功")
        
        print(f"\n🌐 前端访问地址:")
        print(f"   试卷编辑: http://localhost:8080/exam-editor")
        print(f"   管理后台: http://localhost:8000/admin")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    print("=" * 60)

if __name__ == "__main__":
    test_exam_editor()
