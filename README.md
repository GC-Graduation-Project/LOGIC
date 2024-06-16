# 🎵 Tablature Convert App

> 가천대학교 소프트웨어학과 졸업작품 (2024)  
> 지도교수 : 최재영 교수님

## Introduction

Our project is a tablature conversion system that generates accurate and easy-to-read tablature from visual and audio inputs. It features sheet music recognition using YOLOv5, pitch detection using basic-pitch, and MIDI file processing using mido.

## Function

- **Sheet Music Recognition**: Recognizes and processes sheet music images using YOLOv5.
- **Audio Recognition**: Performs audio recognition using basic-pitch and mido.
- **Sheet Music Conversion**: Converts the recognized results into tablature using Vextab and outputs the results as images.

## **Application**
### **Front-End**
https://github.com/GC-Graduation-Project/FE
### Languages
<div>
<img src="https://img.shields.io/badge/Dart-0175C2?style=for-the-badge&logo=dart&logoColor=white">
</div>

### Frameworks
<div>
<img src="https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white">
</div>

![image 1](https://github.com/GC-Graduation-Project/LOGIC/assets/118448112/0df604f8-3950-4aca-8872-33827d102b4f)


<hr/>

### **Back-End**
https://github.com/GC-Graduation-Project/BE

### Languages
<div>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/Javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">
</div>

### Frameworks
<div>
<img src="https://img.shields.io/badge/Express-000000?style=for-the-badge&logo=express&logoColor=white">
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white">
</div>

### Deep Learning
<div>
<img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white">
<img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white">
<img src="https://img.shields.io/badge/yolo-00FFFF?style=for-the-badge&logo=yolo&logoColor=black">
</div>

![image](https://github.com/GC-Graduation-Project/LOGIC/assets/118448112/6dc40f52-e3e9-45f5-9ad5-1a40cb15852f)

## How it works
<img width="2101" alt="image" src="https://github.com/GC-Graduation-Project/LOGIC/assets/118448112/0b6af663-3fe5-46a3-9327-6205337f6049">


## Using Open Source

- Yolov5 ([https://github.com/ultralytics/yolov5](https://github.com/ultralytics/yolov5))
- mido ([https://github.com/mido/mido](https://github.com/mido/mido))
- basic-pitch ([https://github.com/spotify/basic-pitch](https://github.com/spotify/basic-pitch))
- vextab (https://github.com/0xfe/vextab)
- demucs (https://github.com/facebookresearch/demucs)

## Collaborators

| ID        | Name             | Email                | Role                |
|-----------|------------------|----------------------|----------------------|
| 201935075 | Yang-JunHyoung(양준형) | yangkun053@gachon.ac.kr | Sheet Recognition  |
| 201935113 | Lee-HanSeul(이한슬) | parks4754@gmail.com  | Music Recognition  |
| 201935125 | Jung-GyuWon(정규원) | kcc0520@gachon.ac.kr  | Sheet Recognition  |
| 202135563 | Lee-EunSeo(이은서) | silverl@gachon.ac.kr | Music Recognition  |

## Technology stack

- Python
- Pytorch
- OpenCV
- Basic Pitch
- Mido
- YOLOv5
- Pypeteer
- Demucs

## Installation

```bash
pip install -r requirements.txt
pip install pyppeteer // not work install pyppeteer in requirements.txt
```
## Launch
```bash
python main.py --source [your_music_sheet_image_or_audio_file]
```

## Usage
<br>
<details>
  <summary>Sheet Recognition</summary>

```bash
git pull https://github.com/GC-Graduation-Project/LOGIC.git
```

  ```python
  import cv2
  import numpy as np
  import functions as fs
  import modules as md
  import pitchDetection

  src = cv2.imread(source)
  image = md.deskew(src)
  image_0, subimages = md.remove_noise(image)
  normalized_images, stave_list = md.digital_preprocessing(image_0, subimages)
  rec_list, note_list, rest_list = md.beat_extraction(normalized_images)
  clef_list = pitchDetection.detect1(cv2.cvtColor(cv2.bitwise_not(image_0), cv2.COLOR_GRAY2BGR))
  note_list2, pitch_list = md.pitch_extraction(stave_list, normalized_images, clef_list)
  rec_list = fs.standardize_sharps(rec_list)
  note_list2 = fs.standardize_keysharps(note_list2)
  rec_list, note_list2 = fs.synchronize_sharps_and_keysharps(rec_list, note_list2)

  md.process_pitches(rec_list, pitch_list)
  md.update_notes(note_list2, note_list)
  final_list = md.merge_lists(rec_list, note_list2, pitch_list)

  sen = fs.convert_to_sentence(final_list)

```

- ```src = cv2.imread(source)``` : Image Load
- ```md.remove_noise(image)``` : Remove Noise. return Image(Remove Noise) and parsing image divide staff(보표)
- ```md.digital_preprocessing(image_0, subimages)``` : Standard staff distance. return normalize image list and each subImage staff List.
- ```md.beat_extraction(normalized_images)``` : Input Normalize Images and Using object Detect and Interference BeatDetection Model return recognition list, note list, rest list
- ```pitchDetection.detect1(cv2.cvtColor(cv2.bitwise_not(image_0), cv2.COLOR_GRAY2BGR))``` : return Clef List
- ```md.pitch_extraction(stave_list, normalized_images, clef_list)``` : Using stave_list, normalized images, clef list Interference Pitch Detection Model return note list, pitch list
- ```python
  rec_list = fs.standardize_sharps(rec_list)
  note_list2 = fs.standardize_keysharps(note_list2)
  rec_list, note_list2 = fs.synchronize_sharps_and_keysharps(rec_list, note_list2)
There are sharps that are caught and some that are missed, so we need to synchronize them. Therefore, we adjust the number of sharps in the rec and note2 lists to match. After that, we compare the two lists again to perform the final synchronization of the number of sharps.
- ```md.process_pitches(rec_list, pitch_list)``` : Input Beat Detection recognition list, Pitch Detection recognition list and update and merging thier list
- ```md.update_notes(note_list2, note_list)``` : Input Beat Detection note list, Pitch Detection note list and update and merging thier list
- ```md.merge_lists(rec_list, note_list2, pitch_list)``` : total final merging list
- ```fs.convert_to_sentence(final_list)``` : return Vextab Code

</details>
<br>
<details>
  <summary>Music Recognition</summary>

  ```python
  import os
  import numpy as np
  from basic_pitch.inference import predict_and_save
  from mido_ import process_midi_file
  from mido import MidiFile
  
  input_audio_path = "resources/{music_name}.mp3"
  output_directory = os.getcwd()
  save_midi = True
  predict_and_save([input_audio_path], output_directory, save_midi)

  expected_midi_file_name = f"{base_name}_basic_pitch.mid"
  midi_file_path = os.path.join(output_directory, expected_midi_file_name)
  
  mid = MidiFile(midi_file_path)
  mididict = (i.dict() for i in mid if i.type in ('note_on', 'note_off', 'time_signature'))
  output = [(i['type']),(i['note']),(i['time']),(i['channel'])]
  clean_midi = [output[i] for i in range(len(output)) if output[i][0] == 'note_on' or (output[i][0] == 'note_off' and not any(entry['note'] == output[i][1] and entry['time'] == output[i][2] for entry in on_air))]
  
  midi_note_to_name(midi_note)
  duration_to_rhythmic_name(duration)
  rest_duration_to_rhythmic_name(rest_duration)

  output_notes_chunked = ([rhythmic_name, note_name])
  temp = convert_to_sentence(output_notes_chunked)

```

- ```input_audio_path = "resources/{music_name}.mp3"``` : Load audio file
- ```output_directory = os.getcwd()``` : Select the output path
- ```save_midi = True``` : Set `True` to save midi
- ```predict_and_save([input_audio_path], output_directory, save_midi)``` : Detect `input_audio_path` and save midi to `output_directory`

- ```expected_midi_file_name = f"{base_name}_basic_pitch.mid"``` : Search saved midi file
- ```midi_file_path = os.path.join(output_directory, expected_midi_file_name)``` : Create file path in Python
  
- ```mid = MidiFile(midi_file_path)``` : Load midi file to mid
- ```mididict = (i.dict() for i in mid if i.type in ('note_on', 'note_off', 'time_signature'))``` : Store all note_on/note_off events in dictionary
- ```output = [(i['type']),(i['note']),(i['time']),(i['channel'])]``` : Store necessary information in output
- ```clean_midi = [output[i] for i in range(len(output)) if output[i][0] == 'note_on' or (output[i][0] == 'note_off' and not any(entry['note'] == output[i][1] and entry['time'] == output[i][2] for entry in on_air))]``` : Calculate and organize data based on note_on and note_off times
  
- ```midi_note_to_name(midi_note)``` : Convert MIDI note numbers to note names ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
- ```duration_to_rhythmic_name(duration)``` : Convert durations to rhythmic names {'sixteen_note','eight_note','eight_note_dot','quarter_note','quarter_note_dot','half_note','half_note_dot','whole_note'}
- ```rest_duration_to_rhythmic_name(rest_duration)``` : Convert rest durations to rhythmic names
{'sixteen_rest', 'eight_rest', 'eight_rest_dot', 'quarter_rest', 'quarter_rest_dot', 'half_rest', 'half_rest_dot', 'whole_rest'}

- ```output_notes_chunked = ([rhythmic_name, note_name])``` : Create list of tuples containing `rhythmic_name` and `note_name`
- ```temp = convert_to_sentence(output_notes_chunked)``` : return Vextab Code

</details>

<br>

## **Dataset**
- Pitch Detection Dataset https://universe.roboflow.com/gcu-hgo0g/pitch_de
- Beat Detection Dataset https://universe.roboflow.com/gachon-university-4zxlw/music-sheets


## **Modeling**

## **1. Model**
### **Yolo v5**
https://github.com/ultralytics/yolov5

## **2. Train**

![pitch](https://github.com/GC-Graduation-Project/LOGIC/assets/118448112/c92c129a-4de5-478a-b88c-804f6be9bfb3)


