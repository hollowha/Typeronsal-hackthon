#!/usr/bin/env python3
"""
強制測試 Phi-3-mini 備用功能
通過特殊請求強制觸發 phi 模型備用機制
"""

import requests
import json
import time

def test_phi_forced_fallback():
    """強制測試Phi-3-mini備用功能"""
    base_url = "http://localhost:8001"
    
    print("🚀 強制測試 Phi-3-mini 備用功能")
    print("=" * 60)
    print("🎯 目標：強制觸發 phi 模型備用機制，確保 Phi-3-mini 被使用")
    print()
    
    # 測試案例 - 設計用來觸發備用機制
    test_cases = [
        {
            "message": "請生成一個非常複雜的技術分析報告，包含大量專業術語、數學公式、代碼示例和詳細的技術架構說明，要求回應長度超過1000字元，並且包含多個層次的技術細節",
            "context": "深度技術分析",
            "description": "複雜請求測試 - 可能觸發主要模型失敗"
        },
        {
            "message": "請分析字型生成中的神經網絡架構，包括卷積層、注意力機制、損失函數、優化器選擇、正則化技術、數據增強方法、模型壓縮技術、量化方法、知識蒸餾、多任務學習、遷移學習等所有相關技術的詳細實現原理和代碼示例",
            "context": "深度學習技術",
            "description": "技術深度測試 - 可能觸發備用機制"
        },
        {
            "message": "請提供一個完整的字型生成系統的技術實現方案，包括前端界面設計、後端API架構、數據庫設計、緩存策略、負載均衡、微服務架構、容器化部署、CI/CD流程、監控告警、性能優化、安全防護、備份恢復等所有方面的詳細技術文檔",
            "context": "系統架構設計",
            "description": "系統架構測試 - 複雜度極高"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 測試{i}: {test_case['description']}")
        print("-" * 60)
        print(f"問題: {test_case['message'][:100]}...")
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
                timeout=60  # 增加超時時間
            )
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('slm_response', '')
                response_length = len(ai_response)
                
                print(f"✅ 成功 (耗時: {request_time:.1f}ms)")
                print(f"回應長度: {response_length} 字符")
                
                # 分析回應類型
                if "Phi-3-mini" in ai_response or "phi" in ai_response.lower():
                    print("🎉 成功觸發 Phi-3-mini 備用機制！")
                    print("🔍 回應包含 phi 模型標識")
                elif "Universal Blessing" in ai_response:
                    print("🌟 觸發了萬用祝福模式")
                    print("💡 這說明主要模型和 phi 模型都失敗了")
                else:
                    print("🤖 主要 SLM 模型正常工作")
                    print("💡 複雜請求沒有觸發備用機制")
                
                # 顯示回應預覽
                print(f"\n📄 回應預覽 (前200字符):")
                print("-" * 40)
                print(ai_response[:200] + "..." if len(ai_response) > 200 else ai_response)
                print("-" * 40)
                    
            else:
                print(f"❌ 失敗: {response.status_code} - {response.text}")
                
        except requests.exceptions.Timeout:
            print("⏰ 請求超時 - 這可能表示模型正在處理複雜請求")
        except Exception as e:
            print(f"❌ 錯誤: {e}")
        
        # 添加延遲
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print("✨ 強制測試完成！")

def test_phi_model_detection():
    """測試 phi 模型檢測功能"""
    base_url = "http://localhost:8001"
    
    print("\n🔍 測試 Phi 模型檢測功能")
    print("=" * 60)
    
    # 發送一個中等複雜度的請求
    test_message = "請解釋字型生成中的卷積神經網絡原理"
    
    print(f"測試請求: {test_message}")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{base_url}/slm-chat",
            data={
                "user_message": test_message,
                "context": "技術解釋"
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
            
            # 檢查是否包含 phi 相關內容
            phi_indicators = ["phi", "Phi-3-mini", "microsoft/phi"]
            has_phi_content = any(indicator.lower() in ai_response.lower() for indicator in phi_indicators)
            
            if has_phi_content:
                print("🎉 檢測到 Phi 模型內容！")
            else:
                print("🤖 未檢測到 Phi 模型內容")
                print("💡 這可能是正常的，因為主要模型工作正常")
                
        else:
            print(f"❌ 測試失敗: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 測試錯誤: {e}")

if __name__ == "__main__":
    print("🚀 強制測試 Phi-3-mini 備用功能")
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
    test_phi_forced_fallback()
    test_phi_model_detection()
    
    print("\n🎯 測試總結:")
    print("• 如果看到 '嘗試載入 phi 模型' 日誌，說明備用機制被觸發")
    print("• 如果看到 'Phi-3-mini' 相關內容，說明備用模型正常工作")
    print("• 檢查服務器控制台輸出，查看模型切換的詳細日誌")
    print("• 複雜請求更容易觸發備用機制")
