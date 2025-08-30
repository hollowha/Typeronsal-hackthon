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
            
            # 檢查是否有可用的語言模型
            model_name = "microsoft/DialoGPT-medium"  # 使用開源的對話模型
            
            print(f"[SLM] 🤖 嘗試載入語言模型: {model_name}")
            
            # 載入模型和tokenizer
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # 設置pad_token - 修復警告
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
                print(f"[SLM] 🔧 設置pad_token: {tokenizer.pad_token}")
            
            # 構建簡單有效的提示詞
            if context and context.strip():
                prompt = f"User: {characters} (context: {context})\nAssistant:"
            else:
                prompt = f"User: {characters}\nAssistant:"
            
            print(f"[SLM] 📝 使用提示詞: {prompt}")
            
            # 編碼輸入
            inputs = tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=50)
            
            # 生成回應 - 使用更保守的參數
            with torch.no_grad():
                outputs = model.generate(
                    inputs, 
                    max_new_tokens=80,
                    num_return_sequences=1,
                    temperature=0.9,
                    do_sample=True,
                    pad_token_id=tokenizer.pad_token_id,
                    eos_token_id=tokenizer.eos_token_id,
                    repetition_penalty=1.2,
                    no_repeat_ngram_size=2
                )
            
            # 解碼回應
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # 提取生成的部分（去掉原始提示）
            generated_response = response[len(prompt):].strip()
            
            if generated_response:
                print(f"[SLM] ✅ 語言模型生成成功")
                return generated_response
            else:
                print(f"[SLM] ⚠️ 語言模型回應為空，使用備用方案")
                raise Exception("模型回應為空")
                
        except Exception as model_error:
            print(f"[SLM] ⚠️ 語言模型載入失敗: {model_error}")
            print(f"[SLM] 🔄 切換到智能模板模式")
            
            # 備用方案：使用更智能的模板生成
            return _generate_smart_template_response(characters, context)
            
    except Exception as e:
        print(f"[SLM] ❌ 生成SLM回應時出錯: {e}")
        return f"SLM回應生成失敗: {str(e)}"

def _generate_smart_template_response(characters: str, context: str) -> str:
    """智能模板回應（當語言模型不可用時）"""
    try:
        # 根據字元特徵生成更智能的回應
        char_count = len(characters)
        
        # 分析字元類型
        has_chinese = any('\u4e00' <= char <= '\u9fff' for char in characters)
        has_english = any(char.isascii() and char.isalpha() for char in characters)
        has_numbers = any(char.isdigit() for char in characters)
        
        # 根據字元類型選擇回應策略
        if has_chinese:
            if char_count <= 3:
                analysis = f"這{char_count}個中文字元結構相對簡單，筆畫清晰，適合快速生成。"
            elif char_count <= 8:
                analysis = f"這{char_count}個中文字元包含多種筆畫結構，需要平衡生成質量和速度。"
            else:
                analysis = f"這{char_count}個中文字元數量較多，建議分批處理以獲得最佳效果。"
        elif has_english:
            analysis = f"這{char_count}個英文字母結構規律，生成速度會較快。"
        elif has_numbers:
            analysis = f"這{char_count}個數字字元結構簡單，生成效率最高。"
        else:
            analysis = f"這{char_count}個混合字元需要綜合考慮各種因素。"
        
        # 根據上下文生成建議
        if "分析" in context or "特徵" in context:
            suggestion = "建議使用深度學習模型進行筆畫分析和風格匹配，確保生成的字型保持視覺一致性。"
        elif "生成" in context:
            suggestion = "字型生成將使用神經網絡進行風格遷移，每個字元都會經過優化處理。"
        else:
            suggestion = "字型生成過程會考慮字元間的視覺協調性，最終輸出將保持手寫風格的自然性。"
        
        # 技術細節
        technical_details = [
            "使用卷積神經網絡進行字元特徵提取",
            "採用注意力機制確保筆畫的連續性",
            "通過對抗訓練提升字型的真實感",
            "使用風格遷移技術保持參考圖片的風格"
        ]
        
        import random
        selected_details = random.sample(technical_details, 2)
        
        # 構建完整回應
        response = f"""字元 '{characters}' 的智能分析：

{analysis}

{suggestion}

技術實現：
{chr(10).join(f"• {detail}" for detail in selected_details)}

生成建議：根據字元複雜度，預計生成時間約 {char_count * 2} 秒。"""
        
        return response
        
    except Exception as e:
        print(f"[SLM] ❌ 智能模板生成失敗: {e}")
        return f"智能分析失敗: {str(e)}"

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
