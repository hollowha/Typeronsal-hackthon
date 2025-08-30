"""
SLM NPU 功能測試腳本
測試字型生成、批量生成等功能
"""

import sys
import os
import time
from PIL import Image
import numpy as np

# 添加當前目錄到Python路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from slm_generator import create_slm_generator
from ort_qnn_htp_slm import SLMQNNHTPGenerator

def test_basic_slm():
    """測試基本SLM生成器"""
    print("🧪 測試基本SLM生成器")
    print("=" * 50)
    
    # 創建生成器
    generator = create_slm_generator(use_npu=False)  # 使用模擬模式
    
    # 創建測試圖片
    test_image = Image.new('RGB', (64, 64), color='white')
    
    # 測試單字生成
    print("📝 測試單字生成...")
    result = generator.generate_font("A", test_image, sampling_steps=10)
    if result:
        result.save("test_basic_slm_output.png")
        print("✅ 基本SLM測試成功！")
    else:
        print("❌ 基本SLM測試失敗")
    
    # 測試批量生成
    print("📝 測試批量生成...")
    chars = ["A", "B", "C"]
    results = generator.batch_generate_fonts(chars, test_image, sampling_steps=10)
    print(f"批量生成結果: {len(results)}/{len(chars)} 成功")
    
    # 獲取模型信息
    info = generator.get_model_info()
    print(f"模型信息: {info}")
    
    # 清理
    generator.cleanup()
    print()

def test_qnn_htp():
    """測試QNN HTP生成器"""
    print("🧪 測試QNN HTP生成器")
    print("=" * 50)
    
    # 創建QNN HTP生成器
    generator = SLMQNNHTPGenerator()
    
    # 創建測試圖片
    test_image = Image.new('RGB', (64, 64), color='white')
    
    # 測試生成
    print("📝 測試QNN HTP生成...")
    result = generator.generate_font("X", test_image, sampling_steps=15)
    if result:
        result.save("test_qnn_htp_output.png")
        print("✅ QNN HTP測試成功！")
    else:
        print("❌ QNN HTP測試失敗")
    
    # 獲取模型信息
    info = generator.get_model_info()
    print(f"模型信息: {info}")
    
    # 測試上下文二進制生成
    print("🔧 測試上下文二進制生成...")
    success = generator.generate_context_binary()
    if success:
        print("✅ 上下文二進制生成成功！")
    else:
        print("⚠️ 上下文二進制生成失敗（可能是模擬模式）")
    
    # 清理
    generator.cleanup()
    print()

def test_performance():
    """測試性能"""
    print("🧪 測試性能")
    print("=" * 50)
    
    # 創建生成器
    generator = create_slm_generator(use_npu=False)
    
    # 創建測試圖片
    test_image = Image.new('RGB', (64, 64), color='white')
    
    # 測試多次生成以測量性能
    chars = ["A", "B", "C", "D", "E"]
    total_time = 0
    successful_generations = 0
    
    print(f"📝 性能測試: 生成 {len(chars)} 個字元...")
    
    for char in chars:
        start_time = time.time()
        result = generator.generate_font(char, test_image, sampling_steps=10)
        end_time = time.time()
        
        if result:
            successful_generations += 1
            generation_time = (end_time - start_time) * 1000
            total_time += generation_time
            print(f"  {char}: {generation_time:.2f}ms")
        else:
            print(f"  {char}: 失敗")
    
    if successful_generations > 0:
        avg_time = total_time / successful_generations
        print(f"📊 性能統計:")
        print(f"  成功生成: {successful_generations}/{len(chars)}")
        print(f"  總耗時: {total_time:.2f}ms")
        print(f"  平均耗時: {avg_time:.2f}ms")
        print(f"  字元/秒: {1000/avg_time:.2f}")
    
    # 清理
    generator.cleanup()
    print()

def test_error_handling():
    """測試錯誤處理"""
    print("🧪 測試錯誤處理")
    print("=" * 50)
    
    # 創建生成器
    generator = create_slm_generator(use_npu=False)
    
    # 測試無效輸入
    print("📝 測試無效輸入...")
    
    # 空字元
    try:
        result = generator.generate_font("", Image.new('RGB', (64, 64)))
        print(f"  空字元測試: {'成功' if result else '失敗'}")
    except Exception as e:
        print(f"  空字元測試: 異常 - {e}")
    
    # 多字元
    try:
        result = generator.generate_font("AB", Image.new('RGB', (64, 64)))
        print(f"  多字元測試: {'成功' if result else '失敗'}")
    except Exception as e:
        print(f"  多字元測試: 異常 - {e}")
    
    # 無效圖片
    try:
        result = generator.generate_font("A", None)
        print(f"  無效圖片測試: {'成功' if result else '失敗'}")
    except Exception as e:
        print(f"  無效圖片測試: 異常 - {e}")
    
    # 清理
    generator.cleanup()
    print()

def main():
    """主測試函數"""
    print("🚀 SLM NPU 功能測試開始")
    print("=" * 60)
    
    try:
        # 執行各種測試
        test_basic_slm()
        test_qnn_htp()
        test_performance()
        test_error_handling()
        
        print("🎉 所有測試完成！")
        print("📁 檢查輸出文件:")
        print("  - test_basic_slm_output.png")
        print("  - test_qnn_htp_output.png")
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


