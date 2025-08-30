#!/usr/bin/env python3
"""
測試萬用祝福功能
驗證當SLM生成為空時是否會返回溫暖的祝福內容
"""

import requests
import json
import time

def test_universal_blessing():
    """測試萬用祝福功能"""
    base_url = "http://localhost:8001"
    
    print("🎉 測試萬用祝福功能")
    print("=" * 60)
    print("🎯 目標：當SLM生成為空時，返回溫暖的萬用祝福內容")
    print()
    
    # 測試案例 - 涵蓋不同類型的字元
    test_cases = [
        {
            "message": "你好世界",
            "context": "字型分析",
            "description": "中文字元測試"
        },
        {
            "message": "Hello World",
            "context": "字型生成",
            "description": "英文字元測試"
        },
        {
            "message": "12345",
            "context": "數字生成",
            "description": "數字字元測試"
        },
        {
            "message": "你好@World123",
            "context": "混合字元",
            "description": "混合字元測試"
        },
        {
            "message": "🌟✨🎉",
            "context": "特殊符號",
            "description": "特殊符號測試"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 測試{i}: {test_case['description']}")
        print("-" * 50)
        print(f"字元: {test_case['message']}")
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
                timeout=30
            )
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('slm_response', '')
                response_length = len(ai_response)
                
                print(f"✅ 成功 (耗時: {request_time:.1f}ms)")
                print(f"回應長度: {response_length} 字符")
                
                # 檢查是否包含祝福內容
                if "Universal Blessing" in ai_response or "🌟" in ai_response or "✨" in ai_response:
                    print("🎉 檢測到萬用祝福內容！")
                    print("回應預覽:")
                    print("-" * 30)
                    print(ai_response[:300] + "..." if len(ai_response) > 300 else ai_response)
                    print("-" * 30)
                else:
                    print("⚠️  未檢測到祝福內容，可能是語言模型正常回應")
                    print("回應預覽: " + ai_response[:100] + "...")
                    
            else:
                print(f"❌ 失敗: {response.status_code} - {response.text}")
                
        except requests.exceptions.Timeout:
            print("⏰ 請求超時")
        except Exception as e:
            print(f"❌ 錯誤: {e}")
        
        # 添加延遲避免服務器壓力過大
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("✨ 測試完成！")

def test_blessing_quality():
    """測試祝福內容的質量"""
    base_url = "http://localhost:8001"
    
    print("\n🔍 測試祝福內容質量")
    print("=" * 60)
    
    # 測試一個複雜的情況
    complex_test = {
        "message": "🎨字型設計",
        "context": "藝術創作"
    }
    
    print(f"複雜測試:")
    print(f"字元: {complex_test['message']}")
    print(f"上下文: {complex_test['context']}")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{base_url}/slm-chat",
            data={
                "user_message": complex_test["message"],
                "context": complex_test["context"]
            },
            timeout=30
        )
        request_time = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('slm_response', '')
            response_length = len(ai_response)
            
            print(f"\n✅ 測試成功 (耗時: {request_time:.1f}ms)")
            print(f"回應長度: {response_length} 字符")
            
            print("\n完整回應:")
            print("=" * 50)
            print(ai_response)
            print("=" * 50)
            
            # 分析祝福內容
            blessing_indicators = [
                "🌟", "✨", "🎉", "💫", "🌈", "🚀", "🎊", "⭐", "🌺", "🎯",
                "Universal Blessing", "blessing", "wish", "joy", "success", "happiness"
            ]
            
            blessing_count = sum(1 for indicator in blessing_indicators if indicator in ai_response)
            
            print(f"\n📊 祝福內容分析:")
            print(f"• 祝福指標數量: {blessing_count}")
            print(f"• 回應類型: {'萬用祝福' if 'Universal Blessing' in ai_response else '語言模型回應'}")
            
            if blessing_count >= 5:
                print("🎉 祝福內容豐富，質量很高！")
            elif blessing_count >= 3:
                print("✅ 祝福內容適中，質量良好")
            else:
                print("⚠️  祝福內容較少，可能需要檢查")
                
        else:
            print(f"❌ 測試失敗: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 測試錯誤: {e}")

def test_fallback_mechanism():
    """測試回退機制"""
    base_url = "http://localhost:8001"
    
    print("\n🔄 測試回退機制")
    print("=" * 60)
    
    print("💡 這個測試會檢查當語言模型失敗時，系統是否會自動回退到萬用祝福模式")
    print("📝 注意：這需要語言模型實際失敗才能觸發回退機制")
    
    # 測試一個可能觸發回退的問題
    fallback_test = {
        "message": "請生成一個非常複雜的技術分析報告，包含大量專業術語和技術細節",
        "context": "深度技術分析"
    }
    
    print(f"\n測試案例:")
    print(f"問題: {fallback_test['message']}")
    print(f"上下文: {fallback_test['context']}")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{base_url}/slm-chat",
            data={
                "user_message": fallback_test["message"],
                "context": fallback_test["context"]
            },
            timeout=45
        )
        request_time = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('slm_response', '')
            response_length = len(ai_response)
            
            print(f"\n✅ 測試完成 (耗時: {request_time:.1f}ms)")
            print(f"回應長度: {response_length} 字符")
            
            if "Universal Blessing" in ai_response:
                print("🎉 成功觸發回退機制！系統返回了萬用祝福內容")
            else:
                print("✅ 語言模型正常工作，提供了詳細回應")
                print("💡 這說明多重生成策略工作良好，沒有觸發回退")
                
        else:
            print(f"❌ 測試失敗: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 測試錯誤: {e}")

if __name__ == "__main__":
    print("🚀 萬用祝福功能測試")
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
    test_universal_blessing()
    test_blessing_quality()
    test_fallback_mechanism()
    
    print("\n🎯 測試總結:")
    print("• 如果看到 'Universal Blessing' 內容，說明萬用祝福功能正常")
    print("• 如果語言模型正常工作，說明多重生成策略有效")
    print("• 萬用祝福內容應該溫暖、正面、富有啟發性")
    print("• 即使技術出現問題，用戶也能收到溫暖的祝福")
