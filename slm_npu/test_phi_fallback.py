#!/usr/bin/env python3
"""
測試 Phi-3-mini 備用功能
驗證當主要SLM生成為空時是否會自動切換到Phi-3-mini
"""

import requests
import json
import time

def test_phi_fallback():
    """測試Phi-3-mini備用功能"""
    base_url = "http://localhost:8001"
    
    print("🤖 測試 Phi-3-mini 備用功能")
    print("=" * 60)
    print("🎯 目標：當主要SLM生成為空時，自動切換到Phi-3-mini")
    print()
    
    # 測試案例
    test_cases = [
        {
            "message": "請分析字型生成技術",
            "context": "技術分析",
            "description": "技術分析測試"
        },
        {
            "message": "字型設計原理",
            "context": "設計原理",
            "description": "設計原理測試"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 測試{i}: {test_case['description']}")
        print("-" * 50)
        print(f"問題: {test_case['message']}")
        print(f"上下文: {test_case['context']}")
        
        try:
            # 發送請求
            start_time = time.time()
            response = requests.post(
                f"{base_url}/slm-chat",
                data={
                    "user_message": test_case['message'],
                    "context": test_case['context']
                },
                timeout=45
            )
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('slm_response', '')
                response_length = len(ai_response)
                
                print(f"✅ 成功 (耗時: {request_time:.1f}ms)")
                print(f"回應長度: {response_length} 字符")
                
                # 檢查回應內容
                if "Phi-3-mini" in ai_response or "phi" in ai_response.lower():
                    print("🎉 檢測到Phi-3-mini回應！")
                elif "Universal Blessing" in ai_response:
                    print("🌟 觸發了萬用祝福模式")
                else:
                    print("🤖 主要SLM模型正常工作")
                
                print("回應預覽: " + ai_response[:150] + "...")
                    
            else:
                print(f"❌ 失敗: {response.status_code} - {response.text}")
                
        except requests.exceptions.Timeout:
            print("⏰ 請求超時")
        except Exception as e:
            print(f"❌ 錯誤: {e}")
        
        # 添加延遲
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("✨ 測試完成！")

if __name__ == "__main__":
    print("🚀 Phi-3-mini 備用功能測試")
    print("=" * 60)
    
    # 檢查服務器狀態
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            print("✅ 服務器運行正常")
        else:
            print("❌ 服務器狀態異常")
            exit(1)
    except:
        print("❌ 無法連接到服務器，請確保服務器正在運行")
        exit(1)
    
    # 執行測試
    test_phi_fallback()
    
    print("\n🎯 測試總結:")
    print("• 如果看到Phi-3-mini相關日誌，說明備用機制正常")
    print("• 如果主要SLM正常工作，可能不會觸發備用機制")
    print("• 檢查服務器控制台輸出，查看模型切換日誌")
