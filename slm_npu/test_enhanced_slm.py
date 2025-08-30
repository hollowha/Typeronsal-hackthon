#!/usr/bin/env python3
"""
測試增強後的 SLM 回應長度
"""

import requests
import json
import time

def test_enhanced_slm_responses():
    """測試增強後的SLM回應長度"""
    base_url = "http://localhost:8001"
    
    print("🧪 測試增強後的 SLM 回應長度")
    print("=" * 60)
    
    # 測試案例列表
    test_cases = [
        {
            "message": "分析一下'你好世界'這四個字的特徵",
            "context": "字型分析",
            "description": "中文字元分析"
        },
        {
            "message": "什麼是神經網絡風格遷移？",
            "context": "技術諮詢",
            "description": "技術概念解釋"
        },
        {
            "message": "如何優化字型生成的質量？",
            "context": "性能優化",
            "description": "優化建議"
        },
        {
            "message": "字型生成需要哪些技術支持？",
            "context": "技術實現",
            "description": "技術架構"
        },
        {
            "message": "請介紹字型生成的完整流程",
            "context": "流程說明",
            "description": "完整流程"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 測試{i}: {test_case['description']}")
        print("-" * 40)
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
                timeout=30
            )
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('slm_response', '')
                response_length = len(ai_response)
                
                print(f"✅ 成功 (耗時: {request_time:.1f}ms)")
                print(f"回應長度: {response_length} 字符")
                print(f"回應預覽: {ai_response[:150]}...")
                
                # 分析回應質量
                if response_length < 100:
                    print("⚠️  回應較短，可能需要進一步優化")
                elif response_length < 300:
                    print("✅ 回應長度適中")
                else:
                    print("🎉 回應很長，優化效果明顯！")
                    
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

def test_response_quality():
    """測試回應質量"""
    base_url = "http://localhost:8001"
    
    print("\n🔍 測試回應質量指標")
    print("=" * 60)
    
    quality_test = {
        "message": "請詳細分析'人工智能'這四個字的字型特徵，並提供完整的技術實現方案",
        "context": "深度技術分析"
    }
    
    try:
        response = requests.post(
            f"{base_url}/slm-chat",
            data={
                "user_message": quality_test["message"],
                "context": quality_test["context"]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('slm_response', '')
            
            print(f"問題: {quality_test['message']}")
            print(f"回應長度: {len(ai_response)} 字符")
            print("\n完整回應:")
            print("-" * 40)
            print(ai_response)
            print("-" * 40)
            
            # 分析回應結構
            lines = ai_response.split('\n')
            bullet_points = [line for line in lines if '•' in line or '1.' in line or '2.' in line]
            technical_terms = ['神經網絡', 'CNN', 'GAN', '深度學習', '風格遷移', '特徵提取']
            
            print(f"\n📊 質量分析:")
            print(f"• 總行數: {len(lines)}")
            print(f"• 要點數量: {len(bullet_points)}")
            print(f"• 技術術語: {sum(1 for term in technical_terms if term in ai_response)}")
            
        else:
            print(f"❌ 質量測試失敗: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 質量測試錯誤: {e}")

if __name__ == "__main__":
    print("🚀 增強版 SLM 回應長度測試")
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
    test_enhanced_slm_responses()
    test_response_quality()
    
    print("\n🎯 測試總結:")
    print("• 如果回應長度明顯增加，說明優化成功")
    print("• 如果回應仍然較短，可能需要檢查語言模型載入")
    print("• 智能模板模式應該能提供較長的回應")
