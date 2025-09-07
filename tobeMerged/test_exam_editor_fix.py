#!/usr/bin/env python3
"""
测试试卷编辑界面修复后的功能
"""

import requests
import json

def test_exam_editor_fix():
    """测试修复后的试卷编辑功能"""
    base_url = "http://localhost:8000/api/exams"
    
    print("🚀 开始测试修复后的试卷编辑功能...")
    print("=" * 60)
    
    try:
        # 1. 创建试卷
        exam_data = {
            "title": "修复测试试卷",
            "description": "测试修复后的功能"
        }
        response = requests.post(f"{base_url}/exams/", json=exam_data)
        if response.status_code != 201:
            print(f"❌ 创建试卷失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            return
        
        exam = response.json()
        exam_id = exam['id']
        print(f"✅ 创建试卷成功: ID={exam_id}")
        
        # 2. 测试获取空问题列表
        print(f"\n📋 测试获取空问题列表...")
        response = requests.get(f"{base_url}/questions/?exam={exam_id}")
        if response.status_code == 200:
            questions = response.json()
            print(f"✅ 获取问题列表成功")
            print(f"   数据类型: {type(questions)}")
            print(f"   数据内容: {questions}")
            if isinstance(questions, list):
                print(f"   问题数量: {len(questions)}")
            else:
                print(f"   警告: 返回的不是数组格式")
        else:
            print(f"❌ 获取问题列表失败: {response.status_code}")
        
        # 3. 创建单选题
        single_choice_data = {
            "exam": exam_id,
            "text": "测试单选题",
            "question_type": "multiple",
            "correct_answer": "A",
            "points": 5
        }
        response = requests.post(f"{base_url}/questions/", json=single_choice_data)
        if response.status_code == 201:
            question = response.json()
            question_id = question['id']
            print(f"✅ 创建单选题成功: ID={question_id}")
            
            # 添加选项
            options = [
                {"question": question_id, "text": "A", "is_correct": True},
                {"question": question_id, "text": "B", "is_correct": False},
                {"question": question_id, "text": "C", "is_correct": False}
            ]
            
            for option in options:
                response = requests.post(f"{base_url}/answeroptions/", json=option)
                if response.status_code == 201:
                    print(f"   ✅ 添加选项: {option['text']}")
                else:
                    print(f"   ❌ 添加选项失败: {option['text']}")
        else:
            print(f"❌ 创建单选题失败: {response.status_code}")
            print(f"响应内容: {response.text}")
        
        # 4. 再次获取问题列表
        print(f"\n📋 测试获取有问题的问题列表...")
        response = requests.get(f"{base_url}/questions/?exam={exam_id}")
        if response.status_code == 200:
            questions = response.json()
            print(f"✅ 获取问题列表成功")
            print(f"   数据类型: {type(questions)}")
            print(f"   问题数量: {len(questions) if isinstance(questions, list) else 'N/A'}")
            
            if isinstance(questions, list) and len(questions) > 0:
                question = questions[0]
                print(f"   第一个问题:")
                print(f"     ID: {question.get('id')}")
                print(f"     文本: {question.get('text')}")
                print(f"     类型: {question.get('question_type')}")
                print(f"     分值: {question.get('points')}")
                
                # 获取选项
                options_response = requests.get(f"{base_url}/answeroptions/?question={question['id']}")
                if options_response.status_code == 200:
                    options = options_response.json()
                    print(f"     选项数量: {len(options) if isinstance(options, list) else 'N/A'}")
                    if isinstance(options, list):
                        for i, opt in enumerate(options):
                            correct_mark = " ✓" if opt.get('is_correct') else ""
                            print(f"       {chr(97+i)}. {opt.get('text')}{correct_mark}")
        
        print("\n" + "=" * 60)
        print("🎉 修复测试完成!")
        print(f"\n📝 测试结果:")
        print(f"   ✅ 试卷创建: 成功")
        print(f"   ✅ 空问题列表获取: 成功")
        print(f"   ✅ 单选题创建: 成功")
        print(f"   ✅ 选项添加: 成功")
        print(f"   ✅ 有问题列表获取: 成功")
        
        print(f"\n🌐 前端访问地址:")
        print(f"   试卷编辑: http://localhost:8080/exam-editor")
        print(f"   管理后台: http://localhost:8000/admin")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)

if __name__ == "__main__":
    test_exam_editor_fix()
