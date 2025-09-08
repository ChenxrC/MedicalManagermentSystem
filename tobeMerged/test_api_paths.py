#!/usr/bin/env python3
"""
测试API路径是否正确
"""

import requests
import json

BASE_URL = 'http://localhost:8000'

def test_api_paths():
    """测试API路径"""
    
    print("=== 测试API路径 ===\n")
    
    # 测试路径列表
    test_paths = [
        '/api/exams/',
        '/api/exams/1/',
        '/api/exams/?student=1',
        '/api/exams/1/for_student/?student=1',
        '/api/questions/',
        '/api/student-answers/',
        '/api/scores/',
    ]
    
    for path in test_paths:
        print(f"测试路径: {path}")
        try:
            response = requests.get(f"{BASE_URL}{path}", timeout=5)
            print(f"  状态码: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"  返回数据: 列表，共 {len(data)} 项")
                else:
                    print(f"  返回数据: {type(data).__name__}")
            elif response.status_code == 404:
                print("  ❌ 路径不存在")
            else:
                print(f"  ⚠️ 其他错误: {response.text[:100]}")
        except requests.exceptions.ConnectionError:
            print("  ❌ 连接失败 - 请确保后端服务器已启动")
        except Exception as e:
            print(f"  ❌ 错误: {e}")
        print()

if __name__ == '__main__':
    test_api_paths()
