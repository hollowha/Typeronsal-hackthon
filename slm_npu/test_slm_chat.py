#!/usr/bin/env python3
"""
測試 SLM 聊天功能
"""

import requests
import json

def test_slm_chat():
    """測試SLM聊天功能"""
    base_url = "http://localhost:8001"
    
    print("🧪 測試 SLM 聊天功能")
    print("=" * 50)
    
    # 測試1: 基本對話
    print("\n📝 測試1: 基本對話")
    try:
        response = requests.post(
            f"{base_url}/chat",
            data={
                "message": "你好，請介紹一下字型生成技術",
                "context": "字型生成"
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功: {result['ai_response'][:200]}...")
        else:
            print(f"❌ 失敗: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ 錯誤: {e}")
    
    # 測試2: 字型分析對話
    print("\n📝 測試2: 字型分析對話")
    try:
        response = requests.post(
            f"{base_url}/chat",
            data={
                "message": "分析一下'你好'這兩個字的特徵",
                "context": "字型分析"
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功: {result['ai_response'][:200]}...")
        else:
            print(f"❌ 失敗: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ 錯誤: {e}")
    
    # 測試3: 技術諮詢
    print("\n📝 測試3: 技術諮詢")
    try:
        response = requests.post(
            f"{base_url}/chat",
            data={
                "message": "什麼是神經網絡風格遷移？",
                "context": "技術諮詢"
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功: {result['ai_response'][:200]}...")
        else:
            print(f"❌ 失敗: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ 錯誤: {e}")

def test_server_status():
    """測試服務器狀態"""
    base_url = "http://localhost:8001"
    
    print("\n🔍 檢查服務器狀態")
    print("=" * 50)
    
    try:
        # 檢查根路徑
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 服務器運行正常")
            print(f"📋 可用端點: {list(result['endpoints'].keys())}")
        else:
            print(f"❌ 服務器狀態異常: {response.status_code}")
            
        # 檢查健康狀態
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            result = response.json()
            print(f"🏥 健康狀態: {result['status']}")
            print(f"🤖 模型狀態: {result['model_status']}")
        else:
            print(f"❌ 健康檢查失敗: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 狀態檢查錯誤: {e}")

if __name__ == "__main__":
    print("🚀 SLM 聊天功能測試")
    print("=" * 50)
    
    # 檢查服務器狀態
    test_server_status()
    
    # 測試聊天功能
    test_slm_chat()
    
    print("\n✨ 測試完成！")

