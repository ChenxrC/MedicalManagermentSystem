#!/usr/bin/env python3
"""
简单的考试API测试脚本
"""
import requests
import json

def test_exam_api():
    """测试考试API"""
    print("🔍 测试考试API")
    print("=" * 40)
    
    try:
        # 测试考试列表API
        response = requests.get("http://localhost:8000/api/exams/exams/", timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"数据类型: {type(data)}")
            print(f"数据长度: {len(data) if isinstance(data, list) else 'N/A'}")
            
            if isinstance(data, list):
                print("📋 考试数据:")
                for i, exam in enumerate(data[:3]):  # 只显示前3个
                    print(f"  {i+1}. ID: {exam.get('id')}, 标题: {exam.get('title')}")
                    print(f"     描述: {exam.get('description', '无')}")
                    print(f"     创建者: {exam.get('created_by', {}).get('username', '未知')}")
                    print(f"     题目数: {len(exam.get('questions', []))}")
                    print()
                
                if len(data) > 3:
                    print(f"  ... 还有 {len(data) - 3} 个考试")
            else:
                print(f"❌ 数据不是列表格式: {data}")
        else:
            print(f"❌ API返回错误: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器")
        print("请确保后端服务正在运行: cd backend && python manage.py runserver")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_exam_api()
