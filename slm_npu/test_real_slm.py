#!/usr/bin/env python3
"""
直接測試 SLM 功能 - 使用英文輸入
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from slm_server import _generate_slm_response

def test_slm():
    """直接測試SLM功能"""
    print("🧪 直接測試 SLM 功能 - 英文版")
    print("=" * 50)
    
    # 測試1: 簡單英文對話
    print("\n📝 測試1: 簡單英文對話")
    try:
        response = _generate_slm_response("Hello, how are you?", "greeting")
        print(f"✅ 回應: {response}")
    except Exception as e:
        print(f"❌ 錯誤: {e}")
    
    # 測試2: 字型相關英文
    print("\n📝 測試2: 字型相關英文")
    try:
        response = _generate_slm_response("Analyze font characteristics", "font generation")
        print(f"✅ 回應: {response}")
    except Exception as e:
        print(f"❌ 錯誤: {e}")
    
    # 測試3: 創意英文對話
    print("\n📝 測試3: 創意英文對話")
    try:
        response = _generate_slm_response("Write a short poem", "creative writing")
        print(f"✅ 回應: {response}")
    except Exception as e:
        print(f"❌ 錯誤: {e}")
    
    # 測試4: 技術問題
    print("\n📝 測試4: 技術問題")
    try:
        response = _generate_slm_response("What is machine learning?", "technology")
        print(f"✅ 回應: {response}")
    except Exception as e:
        print(f"❌ 錯誤: {e}")
    
    # 測試5: 幽默對話
    print("\n📝 測試5: 幽默對話")
    try:
        response = _generate_slm_response("Tell me a joke", "entertainment")
        print(f"✅ 回應: {response}")
    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    test_slm()
