#!/usr/bin/env python3
"""
测试 typersonal FastAPI 服务的基本功能
"""

import requests
import time
import sys
import os

def test_server_health():
    """测试服务器健康状态"""
    print("=" * 50)
    print("测试 FastAPI 服务器健康状态")
    print("=" * 50)
    
    try:
        # 测试根路径
        response = requests.get("http://localhost:8000/", timeout=10)
        if response.status_code == 200:
            print(f"✅ 根路径测试成功: {response.json()}")
        else:
            print(f"❌ 根路径测试失败: 状态码 {response.status_code}")
            return False
            
        # 测试用户列表
        response = requests.get("http://localhost:8000/users", timeout=10)
        if response.status_code == 200:
            print(f"✅ 用户列表测试成功: {response.json()}")
        else:
            print(f"❌ 用户列表测试失败: 状态码 {response.status_code}")
            return False
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保服务器正在运行")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_api_docs():
    """测试 API 文档是否可访问"""
    print("\n" + "=" * 50)
    print("测试 API 文档访问")
    print("=" * 50)
    
    try:
        # 测试 Swagger 文档
        response = requests.get("http://localhost:8000/docs", timeout=10)
        if response.status_code == 200:
            print("✅ Swagger 文档可访问")
        else:
            print(f"❌ Swagger 文档访问失败: 状态码 {response.status_code}")
            return False
            
        # 测试 ReDoc 文档
        response = requests.get("http://localhost:8000/redoc", timeout=10)
        if response.status_code == 200:
            print("✅ ReDoc 文档可访问")
        else:
            print(f"❌ ReDoc 文档访问失败: 状态码 {response.status_code}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ API 文档测试失败: {e}")
        return False

def main():
    """主函数"""
    print("开始测试 typersonal FastAPI 服务...\n")
    
    # 等待服务器启动
    print("等待服务器启动...")
    time.sleep(2)
    
    # 测试服务器健康状态
    health_ok = test_server_health()
    
    # 测试 API 文档
    docs_ok = test_api_docs()
    
    # 总结
    print("\n" + "=" * 50)
    print("测试结果总结")
    print("=" * 50)
    
    if health_ok and docs_ok:
        print("🎉 所有测试通过！FastAPI 服务运行正常！")
        print("\n服务信息:")
        print("  - 主服务: http://localhost:8000")
        print("  - API 文档: http://localhost:8000/docs")
        print("  - 交互式文档: http://localhost:8000/redoc")
        print("\n现在可以开始使用 AI 字体生成服务了！")
    else:
        print("❌ 部分测试失败，请检查服务器状态")
        if not health_ok:
            print("  - 服务器健康检查失败")
        if not docs_ok:
            print("  - API 文档访问失败")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()




