from sample import arg_parse, load_fontdiffuer_pipeline
import os

def init_args_and_pipe():
    args = arg_parse(ignore_cli=True)
    args.demo = True
    # ✅ 轉換為絕對路徑，避免路徑錯誤
    base_dir = os.path.abspath(os.path.dirname(__file__))  # typersonal/shared/
    args.ckpt_dir = os.path.join(base_dir, '..', 'ckpt')
    args.ttf_path = os.path.join(base_dir, '..', 'ttf', 'KaiXinSongA.ttf')
    args.device = 'cpu'
    return args, load_fontdiffuer_pipeline(args)
