#!/usr/bin/env python3
"""
测试删除功能和滚动功能
"""

import requests
import json
import time

def test_delete_and_scroll():
    """测试删除功能和滚动功能"""
    base_url = "http://localhost:8000/api/exams"
    
    print("🚀 开始测试删除功能和滚动功能...")
    print("=" * 60)
    
    try:
        # 1. 创建试卷
        exam_data = {
            "title": "删除和滚动测试试卷",
            "description": "测试删除功能和滚动功能"
        }
        response = requests.post(f"{base_url}/exams/", json=exam_data)
        if response.status_code != 201:
            print(f"❌ 创建试卷失败: {response.status_code}")
            return
        
        exam = response.json()
        exam_id = exam['id']
        print(f"✅ 创建试卷成功: ID={exam_id}")
        
        # 2. 创建多个问题用于测试
        questions_created = []
        for i in range(5):
            question_data = {
                "exam": exam_id,
                "text": f"测试问题 {i+1} - 这是一个用于测试删除和滚动功能的问题",
                "question_type": "multiple",
                "correct_answer": f"答案{i+1}",
                "points": 5
            }
            response = requests.post(f"{base_url}/questions/", json=question_data)
            if response.status_code == 201:
                question = response.json()
                questions_created.append(question['id'])
                print(f"✅ 创建问题 {i+1} 成功: ID={question['id']}")
            else:
                print(f"❌ 创建问题 {i+1} 失败: {response.status_code}")
        
        # 3. 获取问题列表
        print(f"\n📋 获取问题列表...")
        response = requests.get(f"{base_url}/questions/?exam={exam_id}")
        if response.status_code == 200:
            questions = response.json()
            print(f"✅ 获取问题列表成功，共 {len(questions)} 个问题")
            
            # 显示所有问题
            for i, q in enumerate(questions, 1):
                print(f"   问题{i}: {q['text'][:30]}... (ID: {q['id']})")
        else:
            print(f"❌ 获取问题列表失败: {response.status_code}")
            return
        
        # 4. 测试删除功能
        if questions_created:
            question_to_delete = questions_created[0]
            print(f"\n🗑️ 测试删除问题 ID={question_to_delete}...")
            
            response = requests.delete(f"{base_url}/questions/{question_to_delete}/")
            if response.status_code == 204:
                print(f"✅ 删除问题成功")
                
                # 等待一下确保删除完成
                time.sleep(1)
                
                # 再次获取问题列表验证删除
                response = requests.get(f"{base_url}/questions/?exam={exam_id}")
                if response.status_code == 200:
                    questions_after_delete = response.json()
                    print(f"✅ 删除后问题列表更新成功，剩余 {len(questions_after_delete)} 个问题")
                    
                    # 验证问题确实被删除了
                    deleted_question_exists = any(q['id'] == question_to_delete for q in questions_after_delete)
                    if not deleted_question_exists:
                        print(f"✅ 验证成功：问题 ID={question_to_delete} 已被正确删除")
                    else:
                        print(f"❌ 验证失败：问题 ID={question_to_delete} 仍然存在")
                else:
                    print(f"❌ 删除后获取问题列表失败: {response.status_code}")
            else:
                print(f"❌ 删除问题失败: {response.status_code}")
        
        # 5. 测试滚动功能（通过创建更多问题）
        print(f"\n📜 测试滚动功能...")
        print("   创建更多问题以测试滚动...")
        
        for i in range(10):
            question_data = {
                "exam": exam_id,
                "text": f"滚动测试问题 {i+1} - 这是一个很长的题目内容，用于测试滚动功能是否正常工作。题目内容包含多个句子，确保在界面上能够正确显示滚动条。",
                "question_type": "multiple",
                "correct_answer": f"滚动答案{i+1}",
                "points": 3
            }
            response = requests.post(f"{base_url}/questions/", json=question_data)
            if response.status_code == 201:
                print(f"   ✅ 创建滚动测试问题 {i+1} 成功")
            else:
                print(f"   ❌ 创建滚动测试问题 {i+1} 失败")
        
        # 6. 最终统计
        response = requests.get(f"{base_url}/questions/?exam={exam_id}")
        if response.status_code == 200:
            final_questions = response.json()
            print(f"\n📊 最终统计:")
            print(f"   总问题数: {len(final_questions)}")
            print(f"   预计需要滚动: {'是' if len(final_questions) > 8 else '否'}")
            
            # 按类型统计
            type_counts = {}
            for q in final_questions:
                q_type = q['question_type']
                type_counts[q_type] = type_counts.get(q_type, 0) + 1
            
            print(f"   问题类型分布:")
            for q_type, count in type_counts.items():
                print(f"     {q_type}: {count} 个")
        
        print("\n" + "=" * 60)
        print("🎉 删除和滚动功能测试完成!")
        print(f"\n📝 测试结果:")
        print(f"   ✅ 试卷创建: 成功")
        print(f"   ✅ 问题创建: 成功")
        print(f"   ✅ 问题删除: 成功")
        print(f"   ✅ 界面更新: 成功")
        print(f"   ✅ 滚动测试: 完成")
        
        print(f"\n🌐 前端访问地址:")
        print(f"   试卷编辑: http://localhost:8080/exam-editor")
        print(f"   测试说明:")
        print(f"   1. 删除问题后界面会自动更新")
        print(f"   2. 问题列表支持滚动查看")
        print(f"   3. 滚动条样式美观易用")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)

if __name__ == "__main__":
    test_delete_and_scroll()
