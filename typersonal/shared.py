# shared/core.py
import random
from sample import sampling

def generate_image(character, sampling_step, reference_image, args, pipe):
    args.character_input = True
    args.content_character = character
    args.num_inference_steps = sampling_step
    args.guidance_scale = 7.5
    args.batch_size = 1
    args.seed = random.randint(0, 10000)
    args.version = "V3"

    result_img = sampling(args=args, pipe=pipe, content_image=None, style_image=reference_image)
    return result_img
