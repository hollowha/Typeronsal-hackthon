#!/usr/bin/env python3
"""
測試 Phi-3-mini 模型載入
驗證模型是否可以正常下載和載入
"""

def test_phi_model_loading():
    """測試 Phi-3-mini 模型載入"""
    print("🤖 測試 Phi-3-mini 模型載入")
    print("=" * 50)
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        
        print("✅ transformers 和 torch 庫載入成功")
        
        # 測試模型列表
        phi_models = [
            "microsoft/Phi-3-mini",
            "microsoft/phi-2", 
            "microsoft/phi-1_5"
        ]
        
        for phi_model in phi_models:
            print(f"\n🔄 嘗試載入模型: {phi_model}")
            try:
                print(f"📥 正在下載 tokenizer...")
                tokenizer = AutoTokenizer.from_pretrained(phi_model)
                print(f"✅ Tokenizer 載入成功")
                
                print(f"📥 正在下載模型...")
                model = AutoModelForCausalLM.from_pretrained(phi_model)
                print(f"✅ 模型載入成功")
                
                # 檢查模型參數
                param_count = sum(p.numel() for p in model.parameters())
                print(f"📊 模型參數數量: {param_count:,}")
                
                # 測試簡單推理
                print(f"🧪 測試簡單推理...")
                test_input = "Hello, how are you?"
                inputs = tokenizer(test_input, return_tensors="pt")
                
                with torch.no_grad():
                    outputs = model.generate(
                        inputs.input_ids, 
                        max_new_tokens=20,
                        do_sample=False
                    )
                
                response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                print(f"✅ 推理測試成功")
                print(f"📝 測試回應: {response}")
                
                print(f"🎉 模型 {phi_model} 完全可用！")
                break
                
            except Exception as e:
                print(f"❌ 模型 {phi_model} 載入失敗: {e}")
                continue
        
    except ImportError as e:
        print(f"❌ 庫導入失敗: {e}")
        print("請確保已安裝 transformers 和 torch")
    except Exception as e:
        print(f"❌ 測試失敗: {e}")

if __name__ == "__main__":
    test_phi_model_loading()
