#!/usr/bin/env python3
"""
測試 Phi-2 模型載入
"""

def test_phi2():
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        
        print("🔄 測試 Phi-2 模型載入...")
        
        # 載入 tokenizer
        print("📥 載入 tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")
        
        # 設置 pad_token
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            print("✅ 設置 pad_token")
        
        # 載入模型
        print("📥 載入模型...")
        model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2")
        
        # 測試生成
        print("🧪 測試生成...")
        prompt = "User: 請分析「你好」並提供建議。\n\nAssistant:"
        inputs = tokenizer(prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_new_tokens=50,
                temperature=0.7,
                do_sample=True,
                repetition_penalty=1.1,
                top_k=50,
                top_p=0.9
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"✅ 測試成功！")
        print(f"📝 回應: {response}")
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    test_phi2()
