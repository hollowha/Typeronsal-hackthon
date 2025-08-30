#!/usr/bin/env python3
"""
測試多重生成策略的效果
驗證語言模型回應為空機率的降低效果
"""

import requests
import json
import time
import statistics

def test_multiple_strategies():
    """測試多重生成策略的效果"""
    base_url = "http://localhost:8001"
    
    print("🧪 測試多重生成策略效果")
    print("=" * 60)
    print("🎯 目標：大幅降低語言模型回應為空的機率")
    print()
    
    # 測試案例 - 涵蓋不同類型的問題
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
        },
        {
            "message": "深度學習在字型生成中的應用",
            "context": "深度學習應用",
            "description": "深度學習應用"
        },
        {
            "message": "字型生成的未來發展趨勢",
            "context": "發展趨勢",
            "description": "未來趨勢"
        },
        {
            "message": "字型生成與傳統字體設計的區別",
            "context": "對比分析",
            "description": "對比分析"
        }
    ]
    
    results = []
    empty_responses = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 測試{i}/{total_tests}: {test_case['description']}")
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
                timeout=45  # 增加超時時間
            )
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('slm_response', '')
                response_length = len(ai_response)
                
                # 檢查是否為空回應
                if not ai_response or response_length < 10:
                    empty_responses += 1
                    status = "❌ 空回應"
                else:
                    status = "✅ 成功"
                
                print(f"{status} (耗時: {request_time:.1f}ms)")
                print(f"回應長度: {response_length} 字符")
                print(f"回應預覽: {ai_response[:100]}...")
                
                # 記錄結果
                results.append({
                    "test_id": i,
                    "description": test_case['description'],
                    "response_length": response_length,
                    "request_time": request_time,
                    "is_empty": response_length < 10,
                    "preview": ai_response[:100]
                })
                
                # 分析回應質量
                if response_length < 50:
                    print("⚠️  回應很短")
                elif response_length < 200:
                    print("✅ 回應長度適中")
                elif response_length < 500:
                    print("🎉 回應較長")
                else:
                    print("🚀 回應很長，優化效果顯著！")
                    
            else:
                print(f"❌ 失敗: {response.status_code} - {response.text}")
                empty_responses += 1
                
        except requests.exceptions.Timeout:
            print("⏰ 請求超時")
            empty_responses += 1
        except Exception as e:
            print(f"❌ 錯誤: {e}")
            empty_responses += 1
        
        # 添加延遲避免服務器壓力過大
        time.sleep(1.5)
    
    # 統計分析
    print("\n" + "=" * 60)
    print("📊 測試結果統計")
    print("=" * 60)
    
    successful_tests = [r for r in results if not r['is_empty']]
    empty_rate = (empty_responses / total_tests) * 100
    success_rate = 100 - empty_rate
    
    print(f"總測試數: {total_tests}")
    print(f"成功數: {len(successful_tests)}")
    print(f"空回應數: {empty_responses}")
    print(f"成功率: {success_rate:.1f}%")
    print(f"空回應率: {empty_rate:.1f}%")
    
    if successful_tests:
        response_lengths = [r['response_length'] for r in successful_tests]
        request_times = [r['request_time'] for r in successful_tests]
        
        print(f"\n📈 成功回應統計:")
        print(f"平均回應長度: {statistics.mean(response_lengths):.1f} 字符")
        print(f"最長回應: {max(response_lengths)} 字符")
        print(f"最短回應: {min(response_lengths)} 字符")
        print(f"平均請求時間: {statistics.mean(request_times):.1f}ms")
    
    # 評估優化效果
    print(f"\n🎯 優化效果評估:")
    if empty_rate < 10:
        print("🎉 優秀！空回應率低於10%，優化效果非常顯著")
    elif empty_rate < 25:
        print("✅ 良好！空回應率低於25%，優化效果明顯")
    elif empty_rate < 50:
        print("⚠️  一般！空回應率低於50%，有一定優化效果")
    else:
        print("❌ 需要進一步優化！空回應率仍然較高")
    
    return results, empty_rate

def test_strategy_fallback():
    """測試策略回退機制"""
    base_url = "http://localhost:8001"
    
    print("\n🔄 測試策略回退機制")
    print("=" * 60)
    
    # 測試一個複雜的問題，看看多重策略如何工作
    complex_test = {
        "message": "請詳細解釋字型生成中的神經網絡架構，包括卷積層、注意力機制和損失函數的設計原理",
        "context": "深度技術分析"
    }
    
    print(f"複雜問題測試:")
    print(f"問題: {complex_test['message']}")
    print(f"上下文: {complex_test['context']}")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{base_url}/slm-chat",
            data={
                "user_message": complex_test["message"],
                "context": complex_test["context"]
            },
            timeout=60
        )
        request_time = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('slm_response', '')
            response_length = len(ai_response)
            
            print(f"\n✅ 測試成功 (耗時: {request_time:.1f}ms)")
            print(f"回應長度: {response_length} 字符")
            print(f"回應預覽: {ai_response[:200]}...")
            
            if response_length > 300:
                print("🎉 複雜問題回應很長，多重策略工作良好！")
            else:
                print("⚠️  複雜問題回應較短，可能需要進一步優化")
        else:
            print(f"❌ 測試失敗: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 測試錯誤: {e}")

def generate_optimization_report(results, empty_rate):
    """生成優化報告"""
    print("\n📋 優化建議報告")
    print("=" * 60)
    
    if empty_rate > 30:
        print("🔴 高優先級優化建議:")
        print("• 檢查語言模型載入是否正常")
        print("• 驗證 transformers 和 torch 庫版本")
        print("• 考慮使用更大的預訓練模型")
        print("• 實現模型緩存機制")
    
    if empty_rate > 15:
        print("\n🟡 中優先級優化建議:")
        print("• 調整生成參數的溫度設置")
        print("• 優化提示詞工程")
        print("• 增加更多生成策略")
        print("• 實現回應質量檢查")
    
    if empty_rate < 15:
        print("\n🟢 當前優化效果良好:")
        print("• 多重生成策略工作正常")
        print("• 語言模型參數設置合理")
        print("• 智能模板回退機制有效")
    
    print(f"\n📊 具體數據:")
    print(f"• 目標空回應率: < 10%")
    print(f"• 當前空回應率: {empty_rate:.1f}%")
    print(f"• 改進空間: {max(0, empty_rate - 10):.1f}%")

if __name__ == "__main__":
    print("🚀 多重生成策略效果測試")
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
    results, empty_rate = test_multiple_strategies()
    test_strategy_fallback()
    generate_optimization_report(results, empty_rate)
    
    print("\n✨ 測試完成！")
    print("💡 如果空回應率仍然較高，請檢查:")
    print("   1. 語言模型是否正常載入")
    print("   2. 依賴庫版本是否兼容")
    print("   3. 服務器日誌中的錯誤信息")
