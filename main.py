import argparse
import os
import sys
from pathlib import Path

from mido_ import process_midi_file
from utils.torch_utils import smart_inference_mode
from convert import convert
from basic_pitch.inference import predict_and_save
import asyncio
from render import render_vextab_to_image
from basicPitch import custom_predict_and_save

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
AUDIO_EXTENSIONS = ('.wav', '.mp3', '.flac')

def handle_other_file(file_path):
    # 파일 경로에서 확장자를 추출
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    # 파일 확장자가 오디오 파일인 경우 MIDI 파일로 변환
    if ext in AUDIO_EXTENSIONS:
        print(f"Processing audio file: {file_path}")
        output_directory = os.getcwd()
        save_midi = True
        sonify_midi = False
        save_model_outputs = False
        save_notes = False

        # 기본 모델 경로를 사용하여 MIDI 파일을 생성하고 경로를 반환
        predict_and_save(
            [file_path],
            output_directory,
            save_midi,
            sonify_midi,
            save_model_outputs,
            save_notes
        )

        # 파일 이름 추적
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        expected_midi_file_name = f"{base_name}_basic_pitch.mid"
        midi_file_path = os.path.join(output_directory, expected_midi_file_name)

        print(f"MIDI file saved at: {midi_file_path}")
        return midi_file_path
    else:
        print(f"Unsupported file type: {file_path}")
        return None

@smart_inference_mode()
def run(
        source=ROOT / 'resources/music1.jpg',  # file/dir/URL/glob/screen/0(webcam)
):
    source = str(source)
    if source.lower().endswith(IMAGE_EXTENSIONS):
        # 이미지 파일인 경우 convert 함수 호출
        vextab_code = convert(source)
        output_image_path = "vextab_output.png"
        # asyncio 이벤트 루프를 사용하여 VexTab 코드를 이미지로 렌더링
        asyncio.get_event_loop().run_until_complete(render_vextab_to_image(vextab_code, output_image_path))
    else:
        midi_file_path = handle_other_file(source)
        if midi_file_path:
            vextab_code = process_midi_file(midi_file_path)
            output_image_path = "vextab_output.png"
            # asyncio 이벤트 루프를 사용하여 VexTab 코드를 이미지로 렌더링
            asyncio.get_event_loop().run_until_complete(render_vextab_to_image(vextab_code, output_image_path))

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default=ROOT / 'resources/music1.jpg', help='[your_music_sheet_image_file]')
    opt = parser.parse_args()
    return opt

def main(opt):
    run(**vars(opt))

if __name__ == '__main__':
    opt = parse_opt()
    main(opt)
