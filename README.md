# 🎵 타브 악보 변환 시스템

## 개요

우리의 프로젝트는 타브 악보 변환 시스템으로, YOLOv5를 사용한 악보 인식, basic-pitch를 통한 오디오 음정 감지, mido를 이용한 MIDI 파일 처리를 통해 시각적 및 음성 입력에서 정확하고 읽기 쉬운 타브 악보를 생성할 수 있는 애플리케이션입니다.

## 기능

- **악보 인식**: YOLOv5를 사용하여 악보를 인식하고 처리합니다.
- **오디오 음정 감지**: basic-pitch를 통해 정확한 음정 변환을 수행합니다.
- **MIDI 처리**: mido를 통합하여 MIDI 파일을 관리하고 대응되는 타브 악보를 생성합니다.

## 설치

```bash
pip install -r requirements.txt
```
## 실행
```bash
python main.py --source [your_music_sheet_image_file]
