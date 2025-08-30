"""
SLM NPU 獨立後端服務器
專門用於SLM字型生成，不依賴於現有的後端
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import base64
import sys
import os
import time
from typing import Optional
import uvicorn

# 添加當前目錄到Python路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from slm_generator import create_slm_generator, SLMFontGenerator

# 創建獨立的FastAPI應用
app = FastAPI(
    title="SLM NPU Font Generator",
    description="獨立的SLM NPU字型生成服務",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開發時允許全部來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局SLM生成器實例
slm_generator: Optional[SLMFontGenerator] = None

def get_slm_generator() -> SLMFontGenerator:
    """獲取或創建SLM生成器實例"""
    global slm_generator
    if slm_generator is None:
        # 檢查是否有真實的SLM模型
        model_path = "./models/slm_font_model.onnx"
        use_npu = os.path.exists(model_path)
        
        slm_generator = create_slm_generator(
            model_path=model_path if use_npu else None,
            use_npu=use_npu
        )
        
        print(f"🔧 SLM生成器已初始化: {'NPU模式' if use_npu else '模擬模式'}")
    
    return slm_generator

def _generate_slm_response(characters: str, context: str) -> str:
    """生成SLM回應（使用真正的語言模型）"""
    try:
        # 嘗試使用真正的語言模型
        try:
            from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
            import torch
            
            # 主要語言模型
            primary_model_name = "microsoft/DialoGPT-medium"
            # 備用 phi 模型
            backup_model_name = "microsoft/phi-2"  # 或其他 phi 開頭的模型
            
            print(f"[SLM] 🤖 嘗試載入主要語言模型: {primary_model_name}")
            
            # 嘗試載入主要模型
            try:
                tokenizer = AutoTokenizer.from_pretrained(primary_model_name)
                model = AutoModelForCausalLM.from_pretrained(primary_model_name)
                current_model = primary_model_name
                print(f"[SLM] ✅ 主要模型載入成功: {primary_model_name}")
            except Exception as primary_error:
                print(f"[SLM] ⚠️ 主要模型載入失敗: {primary_error}")
                print(f"[SLM] 🔄 嘗試載入備用 phi 模型: {backup_model_name}")
                
                try:
                    tokenizer = AutoTokenizer.from_pretrained(backup_model_name)
                    model = AutoModelForCausalLM.from_pretrained(backup_model_name)
                    current_model = backup_model_name
                    print(f"[SLM] ✅ 備用 phi 模型載入成功: {backup_model_name}")
                except Exception as backup_error:
                    print(f"[SLM] ❌ 備用 phi 模型也載入失敗: {backup_error}")
                    raise Exception(f"所有語言模型都載入失敗: {primary_error}, {backup_error}")
            
            # 設置pad_token - 修復警告
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
                print(f"[SLM] 🔧 設置pad_token: {tokenizer.pad_token}")
            
            # 構建更豐富的提示詞
            if context and context.strip():
                prompt = f"""User: 請詳細分析並回答關於「{characters}」的問題。上下文：{context}

請提供：
1. 詳細的技術分析
2. 實用的建議和解決方案
3. 相關的技術背景知識
4. 具體的實施步驟

Assistant:"""
            else:
                prompt = f"""User: 請詳細分析並回答關於「{characters}」的問題。

請提供：
1. 詳細的技術分析
2. 實用的建議和解決方案
3. 相關的技術背景知識
4. 具體的實施步驟

Assistant:"""
            
            print(f"[SLM] 📝 使用提示詞: {prompt}")
            
            # 編碼輸入
            inputs = tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=100)
            
            # 多重生成策略 - 大幅降低空回應機率
            generated_responses = []
            
            # 策略1: 標準生成
            try:
                with torch.no_grad():
                    outputs = model.generate(
                        inputs, 
                        max_new_tokens=200,  # 從80增加到200
                        num_return_sequences=1,
                        temperature=0.8,  # 稍微降低溫度以獲得更連貫的回應
                        do_sample=True,
                        pad_token_id=tokenizer.pad_token_id,
                        eos_token_id=tokenizer.eos_token_id,
                        repetition_penalty=1.1,  # 降低重複懲罰
                        no_repeat_ngram_size=3,  # 增加n-gram大小
                        top_k=50,  # 添加top_k參數
                        top_p=0.9,  # 添加top_p參數
                        # 移除 length_penalty 以避免警告，因為我們沒有使用 beam search
                    )
                
                response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                generated_response = response[len(prompt):].strip()
                
                if generated_response and len(generated_response) > 10:
                    generated_responses.append(("標準生成", generated_response))
                    print(f"[SLM] ✅ 標準生成成功，回應長度: {len(generated_response)}")
                
            except Exception as e:
                print(f"[SLM] ⚠️ 標準生成失敗: {e}")
            
            # 策略2: 高溫度生成（增加多樣性）
            if not generated_responses:
                try:
                    with torch.no_grad():
                        outputs = model.generate(
                            inputs, 
                            max_new_tokens=150,
                            num_return_sequences=1,
                            temperature=1.2,  # 高溫度增加多樣性
                            do_sample=True,
                            pad_token_id=tokenizer.pad_token_id,
                            eos_token_id=tokenizer.eos_token_id,
                            repetition_penalty=1.0,  # 降低重複懲罰
                            no_repeat_ngram_size=2,
                            top_k=100,
                            top_p=0.95
                        )
                    
                    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                    generated_response = response[len(prompt):].strip()
                    
                    if generated_response and len(generated_response) > 10:
                        generated_responses.append(("高溫度生成", generated_response))
                        print(f"[SLM] ✅ 高溫度生成成功，回應長度: {len(generated_response)}")
                        
                except Exception as e:
                    print(f"[SLM] ⚠️ 高溫度生成失敗: {e}")
            
            # 策略3: 貪心搜索（確保有輸出）
            if not generated_responses:
                try:
                    with torch.no_grad():
                        outputs = model.generate(
                            inputs, 
                            max_new_tokens=100,
                            num_return_sequences=1,
                            do_sample=False,  # 貪心搜索
                            pad_token_id=tokenizer.pad_token_id,
                            eos_token_id=tokenizer.eos_token_id
                        )
                    
                    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                    generated_response = response[len(prompt):].strip()
                    
                    if generated_response and len(generated_response) > 10:
                        generated_responses.append(("貪心搜索", generated_response))
                        print(f"[SLM] ✅ 貪心搜索成功，回應長度: {len(generated_response)}")
                        
                except Exception as e:
                    print(f"[SLM] ⚠️ 貪心搜索失敗: {e}")
            
            # 策略4: 簡化提示詞重試
            if not generated_responses:
                try:
                    simple_prompt = f"User: 請回答關於「{characters}」的問題。\nAssistant:"
                    simple_inputs = tokenizer.encode(simple_prompt, return_tensors="pt", truncation=True, max_length=50)
                    
                    with torch.no_grad():
                        outputs = model.generate(
                            simple_inputs, 
                            max_new_tokens=80,
                            num_return_sequences=1,
                            temperature=0.9,
                            do_sample=True,
                            pad_token_id=tokenizer.pad_token_id,
                            eos_token_id=tokenizer.eos_token_id
                        )
                    
                    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                    generated_response = response[len(simple_prompt):].strip()
                    
                    if generated_response and len(generated_response) > 10:
                        generated_responses.append(("簡化提示詞", generated_response))
                        print(f"[SLM] ✅ 簡化提示詞生成成功，回應長度: {len(generated_response)}")
                        
                except Exception as e:
                    print(f"[SLM] ⚠️ 簡化提示詞生成失敗: {e}")
            
            # 選擇最佳回應
            if generated_responses:
                # 選擇最長的回應
                best_response = max(generated_responses, key=lambda x: len(x[1]))
                print(f"[SLM] 🎯 選擇最佳回應: {best_response[0]}, 長度: {len(best_response[1])}")
                
                # 檢查回應是否為空或過短
                if not best_response[1] or len(best_response[1].strip()) < 10:
                    print(f"[SLM] ⚠️ 主要模型回應為空，嘗試切換到 phi 模型")
                    return _try_phi_model_fallback(characters, context)
                
                return best_response[1]
            else:
                print(f"[SLM] ⚠️ 所有語言模型策略都失敗，嘗試 phi 模型備用")
                return _try_phi_model_fallback(characters, context)
                
        except Exception as model_error:
            print(f"[SLM] ⚠️ 語言模型載入失敗: {model_error}")
            print(f"[SLM] 🔄 嘗試 phi 模型備用")
            
            # 嘗試 phi 模型備用
            phi_response = _try_phi_model_fallback(characters, context)
            if phi_response:
                return phi_response
            
            # 如果 phi 模型也失敗，使用智能模板
            print(f"[SLM] 🔄 切換到智能模板模式")
            return _generate_smart_template_response(characters, context)
            
    except Exception as e:
        print(f"[SLM] ❌ 生成SLM回應時出錯: {e}")
        return f"SLM回應生成失敗: {str(e)}"

def _try_phi_model_fallback(characters: str, context: str) -> str:
    """嘗試使用 phi 模型作為備用"""
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        
        # 嘗試不同的 phi 模型
        phi_models = [
            "microsoft/Phi-3-mini",  # 主要的 phi 模型
            "microsoft/phi-2",        # 備用 phi-2
            "microsoft/phi-1_5"       # 備用 phi-1.5
        ]
        
        for phi_model in phi_models:
            try:
                print(f"[SLM] 🔄 嘗試載入 phi 模型: {phi_model}")
                
                tokenizer = AutoTokenizer.from_pretrained(phi_model)
                model = AutoModelForCausalLM.from_pretrained(phi_model)
                
                # 設置 pad_token
                if tokenizer.pad_token is None:
                    tokenizer.pad_token = tokenizer.eos_token
                
                # 構建適合 phi 模型的提示詞
                if context and context.strip():
                    prompt = f"User: 請分析「{characters}」並提供建議。上下文：{context}\n\nAssistant:"
                else:
                    prompt = f"User: 請分析「{characters}」並提供建議。\n\nAssistant:"
                
                print(f"[SLM] 📝 Phi 模型提示詞: {prompt}")
                
                # 編碼輸入
                inputs = tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=100)
                
                # 使用 phi 模型生成
                with torch.no_grad():
                    outputs = model.generate(
                        inputs,
                        max_new_tokens=150,
                        temperature=0.7,
                        do_sample=True,
                        pad_token_id=tokenizer.pad_token_id,
                        eos_token_id=tokenizer.eos_token_id,
                        repetition_penalty=1.1,
                        top_k=50,
                        top_p=0.9
                    )
                
                response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                generated_response = response[len(prompt):].strip()
                
                if generated_response and len(generated_response) > 10:
                    print(f"[SLM] ✅ Phi 模型生成成功: {phi_model}, 回應長度: {len(generated_response)}")
                    return generated_response
                else:
                    print(f"[SLM] ⚠️ Phi 模型回應為空: {phi_model}")
                    
            except Exception as phi_error:
                print(f"[SLM] ⚠️ Phi 模型 {phi_model} 載入失敗: {phi_error}")
                continue
        
        print(f"[SLM] ❌ 所有 phi 模型都失敗")
        return None
        
    except Exception as e:
        print(f"[SLM] ❌ Phi 模型備用失敗: {e}")
        return None

def _generate_smart_template_response(characters: str, context: str) -> str:
    """萬用祝福文字回應（當語言模型不可用時）"""
    try:
        import random
        import time
        
        # 獲取當前時間
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # 萬用祝福語句集合
        universal_blessings = [
            "🌟 May your journey be filled with joy, success, and endless possibilities! 🌟",
            "✨ Wishing you strength, wisdom, and happiness in all your endeavors! ✨",
            "🎉 May every step you take lead you closer to your dreams and aspirations! 🎉",
            "💫 Sending you positive energy and warm wishes for a wonderful day ahead! 💫",
            "🌈 May your path be illuminated with hope, love, and beautiful moments! 🌈",
            "🚀 Here's to new beginnings, exciting adventures, and amazing achievements! 🚀",
            "🎊 May your heart be filled with peace, your mind with clarity, and your soul with joy! 🎊",
            "⭐ Wishing you courage to face challenges and wisdom to overcome obstacles! ⭐",
            "🌺 May your life be a beautiful garden of happiness, love, and success! 🌺",
            "🎯 Sending you blessings for health, wealth, and all the good things in life! 🎯"
        ]
        
        # 根據字元內容選擇合適的祝福語
        char_count = len(characters)
        has_chinese = any('\u4e00' <= char <= '\u9fff' for char in characters)
        has_english = any(char.isascii() and char.isalpha() for char in characters)
        has_numbers = any(char.isdigit() for char in characters)
        
        # 選擇祝福語
        if has_chinese:
            selected_blessing = random.choice([
                "🌟 願你的字型創作之路充滿靈感與美好！🌟",
                "✨ 願每個字元都承載著你的夢想與希望！✨",
                "🎨 願你的藝術天賦綻放出最美麗的光芒！🎨"
            ])
        elif has_english:
            selected_blessing = random.choice([
                "🌟 May your typography journey be filled with creativity and beauty! 🌟",
                "✨ May each character carry your dreams and hopes! ✨",
                "🎨 May your artistic talent shine with the most beautiful light! 🎨"
            ])
        elif has_numbers:
            selected_blessing = random.choice([
                "🔢 May your numerical creations bring order and harmony! 🔢",
                "📊 May your data-driven designs inspire and enlighten! 📊",
                "⚡ May your digital innovations spark creativity! ⚡"
            ])
        else:
            selected_blessing = random.choice(universal_blessings)
        
        # 構建簡短的萬用祝福回應
        response = f"""🎉 **Universal Blessing** 🎉

{selected_blessing}

💫 May your day be filled with joy and creativity! 💫

---
🌟 *Generated with love and care* 🌟"""
        
        return response
        
    except Exception as e:
        print(f"[SLM] ❌ 萬用祝福生成失敗: {e}")
        return f"""🎉 **Universal Blessing** 🎉

🔤 Characters: {characters}
📊 Count: {len(characters)}

🌟 May your day be filled with joy and creativity! 🌟
✨ Wishing you success in all your endeavors! ✨
💫 Sending you positive energy and warm wishes! 💫

---
💝 *Even in technical difficulties, we send you our best wishes!* 💝"""

@app.get("/")
async def root():
    """根路徑 - 服務狀態檢查"""
    return {
        "service": "SLM NPU Font Generator",
        "status": "running",
        "timestamp": time.time(),
        "endpoints": {
            "health": "/health",
            "status": "/status",
            "generate": "/generate",
            "batch_generate": "/batch-generate",
            "chat": "/slm-chat",
            "cleanup": "/cleanup"
        }
    }

@app.post("/generate")
async def slm_generate_font(
    character: str = Form(...),
    reference_image: UploadFile = File(...),
    sampling_steps: int = Form(20),
    style_strength: float = Form(0.8)
):
    """
    使用SLM NPU生成字型
    
    Args:
        character: 要生成的字元
        reference_image: 參考風格圖片
        sampling_steps: 採樣步數 (1-50)
        style_strength: 風格強度 (0.0-1.0)
    """
    try:
        print(f"[SLM] 開始生成字型: {character}")
        print(f"[SLM] 參數: steps={sampling_steps}, strength={style_strength}")
        
        # 驗證參數
        if not character or len(character) != 1:
            raise HTTPException(status_code=400, detail="字元必須是單個字符")
        
        if sampling_steps < 1 or sampling_steps > 50:
            raise HTTPException(status_code=400, detail="採樣步數必須在1-50之間")
        
        if style_strength < 0.0 or style_strength > 1.0:
            raise HTTPException(status_code=400, detail="風格強度必須在0.0-1.0之間")
        
        # 讀取並處理圖片
        image_data = await reference_image.read()
        image = Image.open(io.BytesIO(image_data))
        
        # 檢查圖片格式
        if image.mode == 'RGBA':
            print("[SLM] 偵測到RGBA，轉換成RGB")
            image = image.convert('RGB')
        
        print(f"[SLM] 上傳圖片大小: {image.size}, 模式: {image.mode}")
        
        # 獲取SLM生成器
        generator = get_slm_generator()
        
        # 生成字型
        start_time = time.time()
        result_img = generator.generate_font(
            character=character,
            reference_image=image,
            sampling_steps=sampling_steps,
            style_strength=style_strength
        )
        generation_time = (time.time() - start_time) * 1000
        
        if result_img is None:
            raise HTTPException(status_code=500, detail="字型生成失敗")
        
        # 轉換為base64
        buf = io.BytesIO()
        result_img.save(buf, format="PNG")
        base64_img = base64.b64encode(buf.getvalue()).decode()
        
        print(f"[SLM] ✅ 字型生成完成: {character}")
        print(f"[SLM] 生成時間: {generation_time:.2f}ms")
        print(f"[SLM] Base64預覽: {base64_img[:50]}...")
        
        return {
            "success": True,
            "character": character,
            "image": f"data:image/png;base64,{base64_img}",
            "generation_time_ms": round(generation_time, 2),
            "model_info": generator.get_model_info()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[SLM] ❌ 字型生成錯誤: {e}")
        raise HTTPException(status_code=500, detail=f"字型生成失敗: {str(e)}")

@app.post("/batch-generate")
async def slm_batch_generate_fonts(
    characters: str = Form(...),
    reference_image: UploadFile = File(...),
    sampling_steps: int = Form(20),
    style_strength: float = Form(0.8)
):
    """
    批量生成字型
    
    Args:
        characters: 要生成的字元字符串
        reference_image: 參考風格圖片
        sampling_steps: 採樣步數
        style_strength: 風格強度
    """
    try:
        if not characters:
            raise HTTPException(status_code=400, detail="字元不能為空")
        
        # 去重並過濾
        char_list = list(set(characters.strip()))
        char_list = [c for c in char_list if c.strip()]
        
        if len(char_list) > 20:
            raise HTTPException(status_code=400, detail="一次最多生成20個字元")
        
        print(f"[SLM] 開始批量生成字型: {char_list}")
        
        # 讀取圖片
        image_data = await reference_image.read()
        image = Image.open(io.BytesIO(image_data))
        
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        # 獲取生成器
        generator = get_slm_generator()
        
        # 批量生成
        start_time = time.time()
        results = generator.batch_generate_fonts(
            characters=char_list,
            reference_image=image,
            sampling_steps=sampling_steps,
            style_strength=style_strength
        )
        total_time = (time.time() - start_time) * 1000
        
        # 轉換結果
        font_images = {}
        for char, img in results.items():
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            base64_img = base64.b64encode(buf.getvalue()).decode()
            font_images[char] = f"data:image/png;base64,{base64_img}"
        
        print(f"[SLM] ✅ 批量生成完成: {len(results)}/{len(char_list)} 成功")
        print(f"[SLM] 總耗時: {total_time:.2f}ms")
        
        return {
            "success": True,
            "total_characters": len(char_list),
            "successful_characters": len(results),
            "failed_characters": list(set(char_list) - set(results.keys())),
            "font_images": font_images,
            "total_time_ms": round(total_time, 2),
            "model_info": generator.get_model_info()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[SLM] ❌ 批量生成錯誤: {e}")
        raise HTTPException(status_code=500, detail=f"批量生成失敗: {str(e)}")

@app.get("/status")
async def get_slm_status():
    """獲取SLM生成器狀態"""
    try:
        generator = get_slm_generator()
        status = generator.get_model_info()
        
        return {
            "success": True,
            "status": status,
            "timestamp": time.time()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": time.time()
        }

@app.post("/cleanup")
async def cleanup_slm():
    """清理SLM生成器資源"""
    try:
        global slm_generator
        if slm_generator:
            slm_generator.cleanup()
            slm_generator = None
        
        return {
            "success": True,
            "message": "SLM生成器已清理"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/slm-chat")
async def slm_chat(
    message: str = Form(None, alias="user_message"),
    characters: str = Form(None),
    context: str = Form("")
):
    """
    SLM AI 對話端點
    
    Args:
        message: 用戶訊息
        context: 上下文信息（可選）
    """
    try:
        # 處理前端發送的字段
        actual_message = message or characters or "請分析字元特徵"
        print(f"[SLM] 💬 收到對話請求: {actual_message}")
        print(f"[SLM] 📝 上下文: {context}")
        
        # 使用真正的SLM功能生成回應
        ai_response = _generate_slm_response(actual_message, context)
        
        print(f"[SLM] 🤖 AI回應: {ai_response[:100]}...")
        
        return {
            "success": True,
            "user_message": actual_message,
            "slm_response": ai_response,
            "context": context,
            "timestamp": time.time()
        }
        
    except Exception as e:
        print(f"[SLM] ❌ 對話生成錯誤: {e}")
        raise HTTPException(status_code=500, detail=f"對話生成失敗: {str(e)}")

@app.get("/health")
async def slm_health_check():
    """SLM健康檢查"""
    try:
        generator = get_slm_generator()
        status = generator.get_model_info()
        
        is_healthy = status.get("status") in ["active", "qnn_htp_active"]
        
        return {
            "service": "SLM NPU Font Generator",
            "status": "healthy" if is_healthy else "degraded",
            "model_status": status.get("status", "unknown"),
            "timestamp": time.time()
        }
        
    except Exception as e:
        return {
            "service": "SLM NPU Font Generator",
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }

if __name__ == "__main__":
    print("🚀 啟動SLM NPU獨立後端服務...")
    print("📍 服務地址: http://localhost:8001")
    print("🔧 健康檢查: http://localhost:8001/health")
    print("📚 API文檔: http://localhost:8001/docs")
    
    # 啟動服務器，使用8001端口避免與現有後端衝突
    uvicorn.run(
        "slm_server:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
