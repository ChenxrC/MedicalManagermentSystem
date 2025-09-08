#!/usr/bin/env python3
"""
测试修复后的问题创建功能
"""

import requests
import json

def test_question_creation():
    """测试问题创建功能"""
    base_url = "http://localhost:8000"
    
    print("🧪 测试修复后的问题创建功能...")
    print("=" * 50)
    
    try:
        # 1. 首先创建一个试卷
        print("1. 创建试卷...")
        exam_data = {
            'title': '测试试卷',
            'description': '用于测试问题创建功能的试卷'
        }
        
        exam_response = requests.post(f"{base_url}/api/exams/exams/", json=exam_data)
        
        if exam_response.status_code != 201:
            print(f"❌ 创建试卷失败: {exam_response.status_code}")
            print(f"错误信息: {exam_response.text}")
            return False
        
        exam_id = exam_response.json()['id']
        print(f"✅ 试卷创建成功，ID: {exam_id}")
        
        # 2. 创建不带图片的问题
        print("\n2. 创建不带图片的问题...")
        question_data = {
            'exam': exam_id,
            'text': '这是一个测试问题，不包含图片',
            'question_type': 'fill',
            'correct_answer': '测试答案',
            'points': 3
        }
        
        question_response = requests.post(f"{base_url}/api/exams/questions/", json=question_data)
        
        if question_response.status_code != 201:
            print(f"❌ 创建问题失败: {question_response.status_code}")
            print(f"错误信息: {question_response.text}")
            return False
        
        question_data_response = question_response.json()
        print(f"✅ 问题创建成功，ID: {question_data_response['id']}")
        
        # 3. 上传图片
        print("\n3. 上传图片...")
        test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xd7\xd4\xc2\x00\x00\x00\x00IEND\xaeB`\x82'
        
        files = {'image': ('test.png', test_image_data, 'image/png')}
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        
        upload_response = requests.post(f"{base_url}/api/exams/questions/upload_image/", files=files, headers=headers)
        
        if upload_response.status_code != 201:
            print(f"❌ 图片上传失败: {upload_response.status_code}")
            print(f"错误信息: {upload_response.text}")
            return False
        
        image_data = upload_response.json()
        image_path = image_data['image']
        print(f"✅ 图片上传成功，路径: {image_path}")
        
        # 4. 创建带图片的问题
        print("\n4. 创建带图片的问题...")
        question_with_image_data = {
            'exam': exam_id,
            'text': '这是一个测试问题，包含图片',
            'question_type': 'multiple',
            'correct_answer': '测试答案',
            'points': 5,
            'image': image_path  # 使用上传的图片路径
        }
        
        question_with_image_response = requests.post(f"{base_url}/api/exams/questions/", json=question_with_image_data)
        
        if question_with_image_response.status_code != 201:
            print(f"❌ 创建带图片问题失败: {question_with_image_response.status_code}")
            print(f"错误信息: {question_with_image_response.text}")
            return False
        
        question_with_image_data_response = question_with_image_response.json()
        print(f"✅ 带图片问题创建成功，ID: {question_with_image_data_response['id']}")
        print(f"图片URL: {question_with_image_data_response.get('image_url', '无')}")
        
        # 5. 验证问题列表
        print("\n5. 验证问题列表...")
        questions_response = requests.get(f"{base_url}/api/exams/questions/?exam={exam_id}")
        
        if questions_response.status_code == 200:
            questions = questions_response.json()
            print(f"✅ 获取问题列表成功，共 {len(questions)} 个问题")
            for i, question in enumerate(questions, 1):
                print(f"  问题{i}: {question['text']}")
                if question.get('image_url'):
                    print(f"    图片: {question['image_url']}")
        else:
            print(f"❌ 获取问题列表失败: {questions_response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return False

if __name__ == '__main__':
    print("🚀 开始测试修复后的问题创建功能...")
    print("=" * 60)
    
    success = test_question_creation()
    
    if success:
        print("\n🎉 测试通过！问题创建功能正常工作。")
    else:
        print("\n💥 测试失败，请检查后端配置。")
    
    print("\n📋 测试总结：")
    print("- 问题创建功能: " + ("✅ 成功" if success else "❌ 失败"))
