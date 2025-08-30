# typersonal/shared/core.py

import os
import torch
import numpy as np
from PIL import Image
import torchvision.transforms as T
import cv2
from src.dpm_solver.dpm_solver_pytorch import NoiseScheduleVP, model_wrapper, DPM_Solver
from utils import ttf2im, load_ttf, is_char_in_font
from sample import sampling


cached_image = {}

# 修正風格資料夾路徑
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# typersonal/shared/core.py
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
STYLE_DIRS = {
    "書法風": os.path.join(BASE_DIR, "font_ref_imgs"),
    "簡約現代": os.path.join(BASE_DIR, "modern_minimal"),
    "潑墨風": os.path.join(BASE_DIR, "ink_style"),
    "潮流街頭": os.path.join(BASE_DIR, "street_trend"),
    "可愛手繪": os.path.join(BASE_DIR, "cute_handdrawn")
}

def generate_image(character, sampling_step, style_image, args, pipe):
    args.character_input = True
    args.content_character = character
    args.num_inference_steps = sampling_step
    args.seed = 42  # 可改為 random

    font = load_ttf(args.ttf_path)
    if not is_char_in_font(args.ttf_path, character):
        raise ValueError("Character not in TTF font")

    content_image = ttf2im(font, character)

    return sampling(
        args=args,
        pipe=pipe,
        content_image=content_image,
        style_image=style_image
    )


def sampling_with_latent(args, pipe, content_image, style_latent, thickness=0.0):
    with torch.no_grad():
        content_image = content_image.to(pipe.model.device)
        style_latent = style_latent.to(pipe.model.device)

        def forward_with_latent(x, t):
            content_feat, content_res = pipe.model.content_encoder(content_image)
            content_res.append(content_feat)
            style_feat = style_latent
            style_hidden = style_feat.permute(0, 2, 3, 1).reshape(style_feat.shape[0], -1, style_feat.shape[1])
            style_content_feat, style_content_res = pipe.model.content_encoder(content_image)
            style_content_res.append(style_content_feat)
            output = pipe.model.unet(
                x, t,
                [style_feat, content_res, style_hidden, style_content_res],
                args.content_encoder_downsample_size
            )[0]
            return output

        noise_schedule = NoiseScheduleVP(schedule='discrete', betas=pipe.train_scheduler_betas)
        model_fn = model_wrapper(
            model=forward_with_latent,
            noise_schedule=noise_schedule,
            model_type=pipe.model_type,
            guidance_type=pipe.guidance_type,
            condition=None,
            unconditional_condition=None,
            guidance_scale=pipe.guidance_scale
        )
        dpm_solver = DPM_Solver(
            model_fn=model_fn,
            noise_schedule=noise_schedule,
            algorithm_type=args.algorithm_type,
            correcting_x0_fn=args.correcting_x0_fn
        )
        x_T = torch.randn((1, 3, args.content_image_size[0], args.content_image_size[1])).to(pipe.model.device)
        x_sample = dpm_solver.sample(
            x=x_T,
            steps=args.num_inference_steps,
            order=args.order,
            skip_type=args.skip_type,
            method=args.method,
        )
        x_sample = (x_sample / 2 + 0.5).clamp(0, 1).cpu().permute(0, 2, 3, 1).numpy()
        image = (x_sample[0] * 255).astype(np.uint8)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        kernel = np.ones((3, 3), np.uint8)
        if thickness < 0:
            gray = cv2.dilate(gray, kernel, iterations=int(-thickness))
        elif thickness > 0:
            gray = cv2.erode(gray, kernel, iterations=int(thickness))
        return Image.fromarray(cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB))


def blend_styles_latent(character, image_a, style_option, alpha, thickness, args, pipe):
    print(f"[blend] 字: {character}, 風格: {style_option}, alpha: {alpha}, thickness: {thickness}")
    print(f"[blend] 上傳 image_a 大小: {image_a.size}, 模式: {image_a.mode}")

    if not isinstance(character, str) or len(character) != 1:
        print("[blend] ❌ 字元格式錯誤")
        return None

    style_folder = STYLE_DIRS.get(style_option)
    if not style_folder:
        print("[blend] ❌ 無效風格選項")
        return None

    unicode_str = str(ord(character))
    path = os.path.join(style_folder, f"{unicode_str}.png")
    print(f"[blend] 嘗試載入 style B 圖片: {path}")
    if not os.path.exists(path):
        print(f"[blend] ❌ 找不到 style B 圖片: {path}")
        return None

    image_b = Image.open(path).convert("RGB")
    cache_key = (character, style_option, round(alpha, 2))
    if cache_key in cached_image:
        print("[blend] 使用快取圖像")
        image = np.array(cached_image[cache_key])
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        kernel = np.ones((3, 3), np.uint8)
        if thickness > 0:
            gray = cv2.erode(gray, kernel, iterations=int(thickness))
        elif thickness < 0:
            gray = cv2.dilate(gray, kernel, iterations=int(-thickness))
        return Image.fromarray(cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB))

    tf = T.Compose([
        T.Resize((128, 128)),
        T.ToTensor(),
        T.Normalize([0.5], [0.5])
    ])
    image_a_tensor = tf(image_a).unsqueeze(0).to(pipe.model.device)
    image_b_tensor = tf(image_b).unsqueeze(0).to(pipe.model.device)

    with torch.no_grad():
        latent_a, _, _ = pipe.model.style_encoder(image_a_tensor)
        latent_b, _, _ = pipe.model.style_encoder(image_b_tensor)
    fused_latent = (1 - alpha) * latent_a + alpha * latent_b

    if not is_char_in_font(font_path=args.ttf_path, char=character):
        print("[blend] ❌ 該字不在 TTF 字型內")
        return None

    font = load_ttf(ttf_path=args.ttf_path)
    content_image = ttf2im(font=font, char=character)
    content_tf = T.Compose([
        T.Resize(args.content_image_size, interpolation=T.InterpolationMode.BILINEAR),
        T.ToTensor(),
        T.Normalize([0.5], [0.5])
    ])
    content_tensor = content_tf(content_image)[None, :].to(pipe.model.device)

    image = sampling_with_latent(args, pipe, content_tensor, fused_latent, thickness=0)
    cached_image[cache_key] = image
    image_np = np.array(image)
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    kernel = np.ones((3, 3), np.uint8)
    if thickness > 0:
        gray = cv2.erode(gray, kernel, iterations=int(thickness))
    elif thickness < 0:
        gray = cv2.dilate(gray, kernel, iterations=int(-thickness))
    return Image.fromarray(cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB))
