from fastapi import APIRouter, UploadFile, File, Form
from PIL import Image
import io, base64
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'typersonal')))

from shared.initializer import init_args_and_pipe
from shared.core import generate_image, blend_styles_latent

router = APIRouter()

args, pipe = init_args_and_pipe()


@router.post("/ai/generate")
async def ai_generate(
    character: str = Form(...),
    sampling_step: int = Form(...),
    reference_image: UploadFile = File(...)
):
    print(f"[generate] 字: {character}, Sampling Step: {sampling_step}")
    image = Image.open(io.BytesIO(await reference_image.read()))
    print(f"[generate] 上傳圖片大小: {image.size}, 模式: {image.mode}")

    # 🔥 新增：自動將 RGBA 轉成 RGB
    if image.mode == 'RGBA':
        print("[generate] 偵測到 RGBA，轉換成 RGB")
        image = image.convert('RGB')

    result_img = generate_image(character, sampling_step, image, args, pipe)

    buf = io.BytesIO()
    result_img.save(buf, format="PNG")
    base64_img = base64.b64encode(buf.getvalue()).decode()
    print(f"[generate] Base64 回傳預覽: {base64_img[:50]}... (共 {len(base64_img)} 字)")

    return {"image": f"data:image/png;base64,{base64_img}"}


@router.post("/ai/blend")
async def ai_blend(
    character: str = Form(...),
    style_option: str = Form(...),
    alpha: float = Form(...),
    thickness: float = Form(...),
    image_a: UploadFile = File(...)
):
    print(f"[blend] 字: {character}, 風格: {style_option}, alpha: {alpha}, thickness: {thickness}")
    image = Image.open(io.BytesIO(await image_a.read()))
    print(f"[blend] 上傳 image_a 大小: {image.size}, 模式: {image.mode}")

    # 🔥 新增：自動將 RGBA 轉成 RGB
    if image.mode == 'RGBA':
        print("[blend] 偵測到 RGBA，轉換成 RGB")
        image = image.convert('RGB')

    result_img = blend_styles_latent(character, image, style_option, alpha, thickness, args, pipe)

    if result_img is None:
        print("[blend] ❌ 無法處理，回傳 None")
        return {"error": "字元無法處理，請確認輸入。"}

    buf = io.BytesIO()
    result_img.save(buf, format="PNG")
    base64_img = base64.b64encode(buf.getvalue()).decode()
    print(f"[blend] ✅ Base64 回傳預覽: {base64_img[:50]}... (共 {len(base64_img)} 字)")

    return {"image": f"data:image/png;base64,{base64_img}"}
