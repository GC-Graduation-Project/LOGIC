# main.py
import argparse
import os
import sys
from pathlib import Path
from utils.torch_utils import smart_inference_mode
from convert import convert
import asyncio
from render import render_vextab_to_image

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

def handle_other_file(file_path):
    # 이 함수는 이미지 파일이 아닌 경우에 호출됩니다.
    print(f"Handling non-image file: {file_path}")
    # 필요한 작업을 여기에 추가하십시오.

@smart_inference_mode()
def run(
        source=ROOT / 'resources/music.jpg',  # file/dir/URL/glob/screen/0(webcam)
):
    source = str(source)
    if source.lower().endswith(IMAGE_EXTENSIONS):
        # 이미지 파일인 경우 convert 함수 호출
        vextab_code = convert(source)
        output_image_path = "vextab_output.png"
        # asyncio 이벤트 루프를 사용하여 VexTab 코드를 이미지로 렌더링
        asyncio.get_event_loop().run_until_complete(render_vextab_to_image(vextab_code, output_image_path))
    else:
        handle_other_file(source)

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default=ROOT / 'resources/music.jpg', help='[your_music_sheet_image_file]')
    opt = parser.parse_args()
    return opt

def main(opt):
    run(**vars(opt))

if __name__ == '__main__':
    opt = parse_opt()
    main(opt)
