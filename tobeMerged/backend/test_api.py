#!/usr/bin/env python
"""
简单的API测试脚本
"""
import requests
import json

BASE_URL = 'http://localhost:8000'

def test_api():
    """测试API端点"""
    print("开始测试API...")
    
    # 测试学员API
    print("\n1. 测试学员API:")
    try:
        response = requests.get(f'{BASE_URL}/api/students/')
        print(f"学员列表: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"学员数量: {len(data.get('results', data))}")
    except Exception as e:
        print(f"学员API错误: {e}")
    
    # 测试试卷API
    print("\n2. 测试试卷API:")
    try:
        response = requests.get(f'{BASE_URL}/api/exams/')
        print(f"试卷列表: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"试卷数量: {len(data.get('results', data))}")
    except Exception as e:
        print(f"试卷API错误: {e}")
    
    # 测试试卷分配API
    print("\n3. 测试试卷分配API:")
    try:
        response = requests.get(f'{BASE_URL}/api/exam-assignments/')
        print(f"分配列表: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"分配数量: {len(data.get('results', data))}")
    except Exception as e:
        print(f"分配API错误: {e}")
    
    print("\nAPI测试完成!")

if __name__ == '__main__':
    test_api()
