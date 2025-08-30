# sample_init_fastapi.py

from types import SimpleNamespace
from sample import load_fontdiffuer_pipeline

def get_fastapi_args_and_pipe():
    args = SimpleNamespace(
        demo=True,
        ckpt_dir='ckpt',
        ttf_path='ttf/KaiXinSongA.ttf',
        device='cuda:0',
        character_input=True,
        content_character='體',
        num_inference_steps=15,
        guidance_scale=7.5,
        batch_size=1,
        seed=1234,
        version="V3",
        style_image_size=(128, 128),
        content_image_size=(128, 128),
        content_encoder_downsample_size=32,
        model_type="dpm",
        guidance_type="cfg",
        order=2,
        skip_type="time_uniform",
        method="dpmsolver++",
        correcting_x0_fn=None,
        t_start=0,
        t_end=999,
        save_image=False,
        save_image_dir=None,
        resolution=(128, 128),
        unet_channels=128,
        content_start_channel=64,
        style_start_channel=64,
        channel_attn=False,
        block_out_channels=[128, 256, 512]
    )
    pipe = load_fontdiffuer_pipeline(args)
    return args, pipe
