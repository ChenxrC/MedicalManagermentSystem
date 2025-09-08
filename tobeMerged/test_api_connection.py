#!/usr/bin/env python3
"""
API连接测试脚本
"""
import requests
import json

def test_api_connection():
    """测试API连接"""
    base_url = "http://localhost:8000"
    
    print("🔍 测试API连接")
    print("=" * 50)
    
    # 1. 测试服务器是否运行
    try:
        response = requests.get(f"{base_url}/admin/", timeout=5)
        print(f"✅ 服务器连接成功 (状态码: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保Django服务器正在运行")
        print("   运行命令: cd backend && python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ 连接错误: {e}")
        return False
    
    # 2. 测试考试API端点
    try:
        response = requests.get(f"{base_url}/api/exams/exams/", timeout=10)
        print(f"✅ 考试API端点响应 (状态码: {response.status_code})")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 获取到 {len(data)} 个考试")
            if data:
                print("📋 考试列表:")
                for exam in data[:3]:  # 只显示前3个
                    print(f"   - ID: {exam.get('id')}, 标题: {exam.get('title')}")
                if len(data) > 3:
                    print(f"   ... 还有 {len(data) - 3} 个考试")
        else:
            print(f"❌ API返回错误状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API请求失败: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析失败: {e}")
        print(f"响应内容: {response.text}")
        return False
    
    # 3. 测试CORS配置
    try:
        headers = {
            'Origin': 'http://localhost:8080',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        response = requests.options(f"{base_url}/api/exams/exams/", headers=headers, timeout=5)
        print(f"✅ CORS预检请求成功 (状态码: {response.status_code})")
    except Exception as e:
        print(f"⚠️  CORS测试失败: {e}")
    
    print("=" * 50)
    print("✅ API连接测试完成")
    return True

def test_frontend_proxy():
    """测试前端代理配置"""
    print("\n🔍 测试前端代理配置")
    print("=" * 50)
    
    try:
        # 通过前端代理访问API
        response = requests.get("http://localhost:8080/api/exams/exams/", timeout=10)
        print(f"✅ 前端代理访问成功 (状态码: {response.status_code})")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 通过代理获取到 {len(data)} 个考试")
        else:
            print(f"❌ 代理访问失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到前端代理，请确保前端服务正在运行")
        print("   运行命令: cd frontend && npm run serve")
    except Exception as e:
        print(f"❌ 代理测试失败: {e}")

if __name__ == "__main__":
    print("🚀 开始API连接测试")
    
    # 测试直接API连接
    if test_api_connection():
        # 如果直接连接成功，测试前端代理
        test_frontend_proxy()
    
    print("\n📝 测试完成")
    print("\n💡 如果测试失败，请检查:")
    print("   1. 后端服务是否运行: cd backend && python manage.py runserver")
    print("   2. 前端服务是否运行: cd frontend && npm run serve")
    print("   3. 端口是否被占用: 8000(后端), 8080(前端)")
    print("   4. 防火墙设置是否阻止了连接")
