"""
SLM NPU FastAPI 路由
提供SLM字型生成的API端點
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from PIL import Image
import io
import base64
import sys
import os
import time
from typing import Optional

# 添加當前目錄到Python路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from slm_generator import create_slm_generator, SLMFontGenerator

router = APIRouter(prefix="/slm", tags=["SLM NPU"])

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

@router.post("/generate")
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

@router.post("/batch-generate")
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

@router.get("/status")
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

@router.post("/cleanup")
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

@router.get("/health")
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


