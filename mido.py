from mido import MidiFile
import numpy as np
np.set_printoptions(threshold=np.inf)

# MIDI 파일 로드
mid = MidiFile('bb_basic_pitch.mid')
mididict = []
output = []

# 모든 note_on/note_off 이벤트를 딕셔너리로 저장
for i in mid:
    if i.type in ('note_on', 'note_off', 'time_signature'):
        mididict.append(i.dict())

# 델타 시간을 절대 시간으로 변환
mem1 = 0
for i in mididict:
    time = i['time'] + mem1
    i['time'] = time
    mem1 = i['time']

# velocity가 0인 note_on을 note_off로 변경
    if i['type'] == 'note_on' and i['velocity'] == 0:
        i['type'] = 'note_off'

# 노트와 시간 정보를 리스트로 저장
    mem2 = []
    if i['type'] in ('note_on', 'note_off'):
        mem2.append(i['type'])
        mem2.append(i['note'])
        mem2.append(i['time'])
        mem2.append(i['channel'])
        output.append(mem2)

# 시간 서명 추가
    if i['type'] == 'time_signature':
        mem2.append(i['type'])
        mem2.append(i['numerator'])
        mem2.append(i['denominator'])
        mem2.append(i['time'])
        output.append(mem2)

# MIDI 데이터 정리
clean_midi = []
on_air = []
for i in range(len(output)):
    event_type, note, time, channel = output[i]
    if event_type == 'note_on':
        on_air.append({'note': note, 'time': time, 'index': i})
        clean_midi.append(output[i])
    elif event_type == 'note_off':
        dirty_found = False
        for entry in on_air:
            if entry['note'] == note:
                if entry['time'] == time:
                    for j in range(len(clean_midi)):
                        if clean_midi[j][0] == 'note_on' and clean_midi[j][1] == note and clean_midi[j][2] == time:
                            clean_midi.pop(j)
                            dirty_found = True
                            break
                if not dirty_found:
                    clean_midi.append(output[i])
                on_air.remove(entry)
                break

print(mid.ticks_per_beat)
print(len(output))
print(len(clean_midi))

# MIDI 노트 번호를 노트 이름으로 변환
def midi_note_to_name(midi_note):
    if midi_note is None:
        return "Rest"
    else:
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = (midi_note // 12) - 1
        note_index = midi_note % 12
        note_name = note_names[note_index]
        return f"{note_name}{octave}"

# 지속 시간을 리듬 이름으로 변환
def duration_to_rhythmic_name(duration):
    rhythmic_names = {
        0.125: 'sixteen_note',
        0.25: 'eight_note',
        0.375: 'eight_note_dot',
        0.5: 'quarter_note',
        0.75: 'quarter_note_dot',
        1: 'half_note',
        1.5: 'half_note_dot',
        2: 'whole_note'
    }
    closest_duration = min(rhythmic_names.keys(), key=lambda x: abs(x - duration))
    return rhythmic_names[closest_duration]

# 쉬는 시간을 리듬 이름으로 변환
def rest_duration_to_rhythmic_name(rest_duration):
    if rest_duration is not None and rest_duration < 0.05:
        return ''
    if rest_duration is not None:
        rhythmic_names = {
            0.125: 'sixteen_rest',
            0.25: 'eight_rest',
            0.375: 'eight_rest_dot',
            0.5: 'quarter_rest',
            0.75: 'quarter_rest_dot',
            1: 'half_rest',
            1.5: 'half_rest_dot',
            2: 'whole_rest'
        }
        closest_duration = min(rhythmic_names.keys(), key=lambda x: abs(x - rest_duration))
        return rhythmic_names[closest_duration]
    else:
        return 'Unknown rest'

# 베이스 노트 추출
bass_notes = []
for i, event in enumerate(clean_midi[:-1]):
    event_type, note, time, channel = event
    if event_type == 'note_on':
        bass_notes.append({
            'note': note,
            'start_time': time,
            'end_time': None,
            'duration': None,
            'rhythmic_name': None
        })
        for j in range(i + 1, len(clean_midi)):
            if clean_midi[j][0] == 'note_off' and clean_midi[j][1] == note and clean_midi[j][3] == channel:
                end_time = clean_midi[j][2]
                duration = end_time - time
                rhythmic_name = duration_to_rhythmic_name(duration)
                bass_notes[-1]['end_time'] = end_time
                bass_notes[-1]['duration'] = duration
                bass_notes[-1]['rhythmic_name'] = rhythmic_name
                break

# 중복된 시작 시간 제거
bass_notes = [bass_notes[0]] + [bass_note for i, bass_note in enumerate(bass_notes[1:]) if bass_note['start_time'] != bass_notes[i]['start_time']]

# 쉬는 시간 계산
for i, bass_note in enumerate(bass_notes[:-1]):
    note = bass_note['note']
    next_note = bass_notes[i + 1]['note']
    current_start_time = bass_note['start_time']
    next_start_time = None
    rest_duration = None
    for j in range(i + 1, len(clean_midi)):
        if clean_midi[j][0] == 'note_on' and clean_midi[j][1] == next_note and clean_midi[j][3] == clean_midi[i][3]:
            candidate_next_start_time = clean_midi[j][2]
            if candidate_next_start_time > current_start_time:
                if next_start_time is None or candidate_next_start_time <= next_start_time:
                    next_start_time = candidate_next_start_time
    bass_note['next_start_time'] = next_start_time
    rest_duration = next_start_time - bass_note['end_time'] if next_start_time is not None else None
    bass_note['rest_duration'] = rest_duration

# 마지막 베이스 노트 처리
last_bass_note = bass_notes[-1]
last_bass_note['next_start_time'] = None
last_bass_note['rest_duration'] = None

# 출력 노트 준비
output_notes = []
for i, bass_note in enumerate(bass_notes[:-1]):
    rest_duration = bass_note['rest_duration']
    next_start_time = bass_notes[i + 1]['start_time']
    if rest_duration is not None and rest_duration != 0.0:
        note_name = midi_note_to_name(bass_note['note'])
        rhythmic_name = bass_note['rhythmic_name']
        output_notes.append([rhythmic_name, note_name])
        if next_start_time != bass_note['end_time']:
            rhythmic_name = rest_duration_to_rhythmic_name(rest_duration)
            if rhythmic_name != '':
                output_notes.append([rhythmic_name, 'B4'])

# 마지막 노트 처리
last_note = bass_notes[-1]
last_rest_duration = last_note['rest_duration']
if last_rest_duration is not None and last_rest_duration != 0.0:
    last_note_name = midi_note_to_name(last_note['note'])
    last_rhythmic_name = last_note['rhythmic_name']
    output_notes.append([last_rhythmic_name, last_note_name])
    if last_note['next_start_time'] is not None:
        rhythmic_name = rest_duration_to_rhythmic_name(last_rest_duration)
        if rhythmic_name != '':
            output_notes.append([rhythmic_name, 'B4'])

# 리스트를 20개 단위로 나누기
output_notes_chunked = [output_notes[i:i + 20] for i in range(0, len(output_notes), 20)]

# 각 리스트의 첫 번째에 ['gClef', 'none'] 추가
for chunk in output_notes_chunked:
    chunk.insert(0, ['gClef', 'none'])

# 첫 번째 리스트에는 ['gClef', 'none'] 다음에 ['four_four', 'none'] 추가
output_notes_chunked[0].insert(1, ['four_four', 'none'])

# 노트를 기타 프렛의 위치로 매핑하는 함수
def get_guitar(note):
    mapping = {
        'E4': ['0/1', '5/2', '9/3'],
        'F4': ['1/1', '6/2', '10/3'],
        'F#4': ['2/1', '7/2', '11/3'],
        'G4': ['3/1', '8/2', '12/3', '17/4', '22/5'],
        'G#4': ['4/1', '9/2', '13/3', '18/4'],
        'A4': ['5/1', '10/2', '14/3', '19/4'],
        'A#4': ['6/1', '11/2', '15/3', '20/4'],
        'B4': ['7/1', '12/2', '16/3', '21/4'],
        'C5': ['8/1', '13/2', '17/3', '22/4'],
        'C#5': ['9/1', '14/2', '18/3'],
        'D5': ['10/1', '15/2', '19/3'],
        'D#5': ['11/1', '16/2', '20/3'],
        'E5': ['12/1', '17/2', '21/3'],
        'F5': ['13/1', '18/2', '22/3'],
        'F#5': ['14/1', '19/2'],
        'G5': ['15/1', '20/2'],
        'G#5': ['16/1', '21/2'],
        'A5': ['17/1', '22/2'],
        'B3': ['0/2', '4/3', '9/4', '14/5', '19/6'],
        'C4': ['1/2', '5/3', '10/4', '15/5', '20/6'],
        'C#4': ['2/2', '6/3', '11/4', '16/5', '21/6'],
        'D4': ['3/2', '7/3', '12/4', '17/5', '22/6'],
        'D#4': ['4/2', '8/3', '13/4', '18/5'],
        'E4': ['4/2', '8/3', '13/4', '18/5'],
        'G3': ['0/3', '5/4', '10/5', '15/6'],
        'G#3': ['1/3', '6/4', '11/5', '16/6'],
        'A3': ['2/3', '7/4', '12/5', '17/6'],
        'A#3': ['3/3', '8/4', '13/5', '18/6'],
        'D3': ['0/4', '5/5', '10/6'],
        'D#3': ['1/4', '6/5', '11/6'],
        'E3': ['2/4', '7/5', '12/6'],
        'F3': ['3/4', '8/5', '13/6'],
        'F#3': ['4/4', '9/5', '14/6'],
        'A2': ['0/5', '5/6'],
        'A#2': ['1/5', '6/6'],
        'B2': ['2/5', '7/6'],
        'C3': ['3/5', '8/6'],
        'C#3': ['4/5', '9/6'],
        'E2': ['0/6'],
        'F2': ['1/6'],
        'F#2': ['2/6'],
        'G2': ['3/6'],
        'G#2': ['4/6']
    }
    positions = mapping.get(note, ["해당 문자열에 대한 숫자가 없습니다."])
    return min(positions, key=lambda x: int(x.split('/')[0]))

# 노트를 기타 프렛으로 매핑하여 변환
for chunk in output_notes_chunked:
    for i in range(len(chunk)):
        if len(chunk[i]) == 2 and chunk[i][1] != 'none':
            note_name = chunk[i][1]
            guitar_position = get_guitar(note_name)
            chunk[i][1] = guitar_position

# 결과 출력
for chunk in output_notes_chunked:
    print(chunk)

# 변환된 결과를 문장으로 변환하는 함수
def convert_to_sentence(mapped_result_list):
    complete_sentence = ""

    note_mapping = {
        'gClef': ('treble ', 0),
        'fClef': ('bass', 0),
        'four_four': ('time=4/4\nnotes', 0),
        'quarter_note': (' :q ', 0.25),
        'half_note': (' :h ', 0.5),
        'half_note_dot': (' :hd ', 0.75),
        'dot_half_note': (' :hd ', 0.75),
        'dot_half_note_dot': (' :hd ', 0.75),
        'quarter_note_dot': (' :qd ', 0.375),
        'dot_quarter_note_dot': (' :qd ', 0.375),
        'eight_note': (' :8 ', 0.125),
        'eight_note_dot': (' :8d ', 0.1875),
        'sixteen_note': (' :16 ', 0.0625),
        'sixteen_note_dot': (' :16d ', 0.09375),
        'whole_note': (' :w ', 1),
        'quarter_rest': (' :4 ##', 0.25),
        'half_rest': (' :2 ##', 0.5),
        'half_rest_dot': (' :2d ##', 0.75),
        'quarter_rest_dot': (' :4d ##', 0.375),
        'eight_rest': (' :8 ##', 0.125),
        'eight_rest_dot': (' :8d ##', 0.1875),
        'sixteen_rest': (' :16 ##', 0.0625),
        'sixteen_rest_dot': (' :16d ##', 0.09375),
        'whole_rest': (' :w ##', 1),
        'sharp': (' #', 0)
    }

    for result in mapped_result_list:
        sen = "\ntabstave notation=true clef="  # 각 리스트에 대해 새 탭스태브 시작
        current_time = 0  # 각 라인에 대한 현재 시간 초기화
        sharp_count = 0  # 각 라인에 대한 샤프 수 초기화
        four_four_found = False
        gclef_found = False

        for i, item in enumerate(result):
            action, value = note_mapping.get(item[0], ('', 0))

            if item[0] == 'sharp':
                sharp_count += 1
                continue  # 샤프 심볼 추가를 건너뜀

            if item[0] == 'gClef':
                gclef_found = True

            if item[0] == 'four_four':
                four_four_found = True
                if sharp_count == 1:
                    sen += " key=G "  # 샤프가 정확히 하나인 경우 key=G 추가
                    sharp_count = 0  # key=G 추가 후 샤프 수 초기화

            if current_time + value > 1:  # 마디 길이가 1을 초과하면 바 라인 추가
                sen += " |"
                current_time = 0

            if action:  # 문장에 액션 추가
                sen += action
                if item[0] not in ['gClef', 'fClef', 'four_four', 'quarter_rest']:
                    sen += item[1]  # 해당하는 경우 노트 상세 정보 추가

            current_time += value

        # gClef가 있지만 four_four가 없는 경우 확인
        if gclef_found and not four_four_found and sharp_count == 1:
            sen = sen.replace('clef=treble', 'clef=treble key=G\nnotes')
        elif gclef_found and not four_four_found:
            sen = sen.replace('clef=treble', 'clef=treble \nnotes')
        sen += " =|="
        complete_sentence += sen

    return complete_sentence

temp = convert_to_sentence(output_notes_chunked)

print(temp)
