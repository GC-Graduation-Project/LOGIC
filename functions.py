# functions.py
import cv2
import numpy as np

def weighted(value):
    standard = 10
    return int(value * (standard / 10))

def threshold(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    return image

def camera_threshold(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 10)
    return image

def get_guitar(note):
    mapping = {
        'E4': ['0/1', '5/2', '9/3'],
        'F4': ['1/1', '6/2', '10/3'],
        'F#4': ['2/1', '7/2', '11/3'],
        'G♭4': ['2/1', '7/2', '11/3'],
        'G4': ['3/1', '8/2', '12/3', '17/4', '22/5'],
        'G#4': ['4/1', '9/2', '13/3', '18/4'],
        'A♭4': ['4/1', '9/2', '13/3', '18/4'],
        'A4': ['5/1', '10/2', '14/3', '19/4'],
        'A#4': ['6/1', '11/2', '15/3', '20/4'],
        'B♭4': ['6/1', '11/2', '15/3', '20/4'],
        'B4': ['7/1', '12/2', '16/3', '21/4'],
        'C5': ['8/1', '13/2', '17/3', '22/4'],
        'C#5': ['9/1', '14/2', '18/3'],
        'D♭5': ['9/1', '14/2', '18/3'],
        'D5': ['10/1', '15/2', '19/3'],
        'D#5': ['11/1', '16/2', '20/3'],
        'E♭5': ['11/1', '16/2', '20/3'],
        'E5': ['12/1', '17/2', '21/3'],
        'F5': ['13/1', '18/2', '22/3'],
        'F#5': ['14/1', '19/2'],
        'G♭5': ['14/1', '19/2'],
        'G5': ['15/1', '20/2'],
        'G#5': ['16/1', '21/2'],
        'A♭5': ['16/1', '21/2'],
        'A5': ['17/1', '22/2'],
        'A#5': ['18/1'],
        'B♭5': ['18/1'],
        'B5': ['19/1'],
        'C6': ['20/1'],
        'C#6': ['21/1'],
        'D♭6': ['21/1'],
        'D6': ['22/1'],
        'B3': ['0/2', '4/3', '9/4', '14/5', '19/6'],
        'C4': ['1/2', '5/3', '10/4', '15/5', '20/6'],
        'C#4': ['2/2', '6/3', '11/4', '16/5', '21/6'],
        'D♭4': ['2/2', '6/3', '11/4', '16/5', '21/6'],
        'D4': ['3/2', '7/3', '12/4', '17/5', '22/6'],
        'D#4': ['4/2', '8/3', '13/4', '18/5'],
        'E♭4': ['4/2', '8/3', '13/4', '18/5'],
        'G3': ['0/3', '5/4', '10/5', '15/6'],
        'G#3': ['1/3', '6/4', '11/5', '16/6'],
        'A♭3': ['1/3', '6/4', '11/5', '16/6'],
        'A3': ['2/3', '7/4', '12/5', '17/6'],
        'A#3': ['3/3', '8/4', '13/5', '18/6'],
        'B♭3': ['3/3', '8/4', '13/5', '18/6'],
        'D3': ['0/4', '5/5', '10/6'],
        'D#3': ['1/4', '6/5', '11/6'],
        'E♭3': ['1/4', '6/5', '11/6'],
        'E3': ['2/4', '7/5', '12/6'],
        'F3': ['3/4', '8/5', '13/6'],
        'F#3': ['4/4', '9/5', '14/6'],
        'G♭3': ['4/4', '9/5', '14/6'],
        'A2': ['0/5', '5/6'],
        'A#2': ['1/5', '6/6'],
        'B♭2': ['1/5', '6/6'],
        'B2': ['2/5', '7/6'],
        'C3': ['3/5', '8/6'],
        'C#3': ['4/5', '9/6'],
        'D♭3': ['4/5', '9/6'],
        'E2': ['0/6'],
        'F2': ['1/6'],
        'F#2': ['2/6'],
        'G♭2': ['2/6'],
        'G2': ['3/6'],
        'G#2': ['4/6'],
        'A♭2': ['4/6']

    }
    return mapping.get(note, "해당 문자열에 대한 숫자가 없습니다.")

def get_bass_guitar(note):
    mapping = {
        'E2': ['0/4'],
        'F2': ['1/4'],
        'F#2': ['2/4'],
        'G♭2': ['2/4'],
        'G2': ['3/4'],
        'G#2': ['4/4'],
        'A♭2': ['4/4'],
        'A2': ['5/4', '0/3'],
        'A#2': ['6/4', '1/3'],
        'B♭2': ['6/4', '1/3'],
        'B2': ['7/4', '2/3'],
        'C3': ['8/4', '3/3'],
        'C#3': ['9/4', '4/3'],
        'D♭3': ['9/4', '4/3'],
        'D3': ['10/4', '5/3', '0/2'],
        'D#3': ['11/4', '6/3', '1/2'],
        'E♭3': ['11/4', '6/3', '1/2'],
        'E3': ['12/4', '7/3', '2/2'],
        'F3': ['13/4', '8/3', '3/2'],
        'F#3': ['14/4', '9/3', '4/2'],
        'G♭3': ['14/4', '9/3', '4/2'],
        'G3': ['15/4', '10/3', '5/2', '0/1'],
        'G#3': ['16/4', '11/3', '6/2', '1/1'],
        'A♭3': ['16/4', '11/3', '6/2', '1/1'],
        'A3': ['17/4', '12/3', '7/2', '2/1'],
        'A#3': ['18/4', '13/3', '8/2', '3/1'],
        'B♭3': ['18/4', '13/3', '8/2', '3/1'],
        'B3': ['19/4', '14/3', '9/2', '4/1'],
        'C4': ['20/4', '15/3', '10/2', '5/1'],
        'C#4': ['21/4', '16/3', '11/2', '6/1'],
        'D♭4': ['21/4', '16/3', '11/2', '6/1'],
        'D4': ['22/4', '17/3', '12/2', '7/1'],
        'D#4': ['18/3', '13/2', '8/1'],
        'E♭4': ['18/3', '13/2', '8/1'],
        'E4': ['19/3', '14/2', '9/1'],
        'F4': ['20/3', '15/2', '10/1'],
        'F#4': ['21/3', '16/2', '11/1'],
        'G♭4': ['21/3', '16/2', '11/1'],
        'G4': ['22/3', '17/2', '12/1'],
        'G#4': ['18/2', '13/1'],
        'A♭4': ['18/2', '13/1'],
        'A4': ['19/2', '14/1'],
        'A#4': ['20/2', '15/1'],
        'B♭4': ['20/2', '15/1'],
        'B4': ['21/2', '16/1'],
        'C5': ['22/2', '17/1'],
        'C#5': ['18/1'],
        'D♭5': ['18/1'],
        'D5': ['19/1'],
        'D#5': ['20/1'],
        'E♭5': ['20/1'],
        'E5': ['21/1'],
        'F5': ['22/1']
    }

    return mapping.get(note, [])



def mapping_notes(stav, notes):
    updated_notes_gclef = ['F4', 'E4', 'D4', 'C4', 'B3', 'A3', 'G3', 'F3', 'E3', 'D3', 'C3']
    updated_notes_fclef = ['F3', 'E3', 'D3', 'C3', 'B2', 'A2', 'G2', 'F2', 'E2', 'D2', 'C2']  # 낮은음자리표에 맞는 음 리스트
    updated_notes = []
    notes_list = []

    for note in notes:
        value, note_type = note[0], note[1]
        if note[1] == 'gClef':
            updated_notes = updated_notes_gclef
            continue
        elif note[1] == 'fClef':
            updated_notes = updated_notes_fclef
            continue
        # Find the closest distance in stav to this value in notes
        closest_distance = min(stav, key=lambda x: abs(x - value))
        # Find the corresponding note for this closest distance
        index = stav.index(closest_distance)
        note = updated_notes[index % len(updated_notes)]
        notes_list.append(note)
    print(notes_list)
    return notes_list




def add_dot(data):
    i = 0
    while i < len(data):
        if data[i][1] == 'augmentationDot':
            data[i-1][1] += '_dot'
            del data[i]
        else:
            i += 1
    return data




def calculate_efficient_positions(notes, mapping):
    """
    Calculate the most efficient positions to play a sequence of notes.

    :param notes: A list of notes to be played in order.
    :param mapping: The dictionary containing the fret/string positions for each note.
    :return: A list of positions for each note that minimizes the overall distance.
    """
    if not notes:
        return []

    # Start with all possible positions for the first note
    possible_positions = [[pos] for pos in mapping[notes[0]]]

    for note in notes[1:]:
        new_positions = []
        for pos_sequence in possible_positions:
            last_pos = pos_sequence[-1]
            last_fret, last_string = map(int, last_pos.split('/'))

            # Find the closest position for the current note
            shortest_distance = float('inf')
            best_position = None
            for pos in mapping[note]:
                fret, string = map(int, pos.split('/'))
                distance = ((fret - last_fret) ** 2 + (string - last_string) ** 2) ** 0.5
                if distance < shortest_distance:
                    shortest_distance = distance
                    best_position = pos

            new_positions.append(pos_sequence + [best_position])

        possible_positions = new_positions

    # Find the sequence with the shortest overall distance
    shortest_overall_distance = float('inf')
    best_sequence = None
    for pos_sequence in possible_positions:
        overall_distance = 0
        for i in range(len(pos_sequence) - 1):
            fret1, string1 = map(int, pos_sequence[i].split('/'))
            fret2, string2 = map(int, pos_sequence[i + 1].split('/'))
            overall_distance += ((fret1 - fret2) ** 2 + (string1 - string2) ** 2) ** 0.5

        if overall_distance < shortest_overall_distance:
            shortest_overall_distance = overall_distance
            best_sequence = pos_sequence

    return best_sequence

def modify_notes(notes, sharps=0, flats=0):
    # 샵과 플랫에 영향을 받는 음의 순서
    sharp_order = ['F', 'C', 'G', 'D', 'A', 'E', 'B']
    flat_order = ['B', 'E', 'A', 'D', 'G', 'C', 'F']

    # 샵이나 플랫에 따라 변경할 음들을 결정
    sharps_to_modify = sharp_order[:sharps]
    flats_to_modify = flat_order[:flats]

    # 리스트를 순회하며 음을 변경
    for i, note in enumerate(notes):
        note_base = note[0] # 음의 기본 문자

        if note_base in sharps_to_modify:
            # 샵(#) 추가
            notes[i] = note_base + '#' + note[1:]
        elif note_base in flats_to_modify:
            # 플랫(♭) 추가
            notes[i] = note_base + '♭' + note[1:]

    return notes

def update_notes(top_list, bottom_list, tolerance=15):
    updated_list = []

    for top_item in top_list:
        # 하단 리스트에서 x좌표가 ±tolerance 범위 내에 있는 가장 가까운 요소 찾기
        matching_bottom_item = min(bottom_list, key=lambda x: abs(x[-1] - top_item[-1]), default=None)

        # 일치하는 요소가 있고, 그 차이가 tolerance 이내이면 해당 요소의 가운데 값으로 변경
        if matching_bottom_item and abs(matching_bottom_item[-1] - top_item[-1]) <= tolerance:
            note_type = matching_bottom_item[1]
            # '_dot' 처리
            if '_dot' in top_item[1]:
                note_type += '_dot'
            top_item[1] = note_type
        else:
            # If top_item[1] is not None, check for 'Half' or 'Whole'
            if top_item[1] is not None:
                if 'Half' in top_item[1]:
                    top_item[1] = 'half_note'
                elif 'Whole' in top_item[1]:
                    top_item[1] = 'whole_note'
                elif 'keySharp' in top_item[1]:
                    top_item[1] = 'sharp'
                else:
                    top_item[1] = None
            else:
                top_item[1] = None

        # top_item[1]이 None이 아닌 경우에만 updated_list에 추가
        if top_item[1] is not None:
            updated_list.append(top_item)

    return updated_list


def count_sharps_flats(data_list):
    sharps = 0
    flats = 0

    for item in data_list:
        if len(item) >= 2:  # Check if the item has at least two elements
            if item[1] == 'sharp':
                sharps += 1
            elif item[1] == 'flat':
                flats += 1

    return sharps, flats


def merge_three_lists(list1, list2, list3):
    merged_list = []
    tolerance = 15

    # list1의 요소를 먼저 merged_list에 추가
    for item1 in list1:
        merged_list.append(item1)

    # list2의 각 요소를 비교하고 병합
    for item2 in list2:
        matched = False
        for i, item1 in enumerate(merged_list):
            if abs(item1[-1] - item2[-1]) <= tolerance:
                merged_list[i] = item2
                matched = True
                break
        if not matched:
            # 일치하는 요소가 없으면 적절한 위치에 삽입
            insert_index = next((i for i, item in enumerate(merged_list) if item[-1] > item2[-1]), len(merged_list))
            merged_list.insert(insert_index, item2)

    # x좌표 기준으로 오름차순 정렬
    merged_list.sort(key=lambda x: x[-1])

    # list3의 요소를 병합된 리스트의 뒤쪽부터 적용
    list3_index = len(list3) - 1
    merged_list_index = len(merged_list) - 1

    while list3_index >= 0 and merged_list_index >= 0:
        if merged_list[merged_list_index][1] is not None and '_rest' in merged_list[merged_list_index][1]:
            merged_list[merged_list_index][-1] = None
            merged_list_index -= 1  # '_rest'인 경우 list3_index는 감소시키지 않음
        else:
            merged_list[merged_list_index][-1] = list3[list3_index]
            list3_index -= 1
            merged_list_index -= 1

    # list3의 길이가 더 짧으면 나머지 부분을 None으로 채움
    for i in range(merged_list_index, -1, -1):
        merged_list[i][-1] = None

    # 최종 리스트에서 첫 번째 값을 제거
    final_list = [item[1:] for item in merged_list]

    return final_list



def convert_to_sentence(mapped_result_list):
    complete_sentence = ""

    note_mapping = {
        'gClef': ('treble ', 0),
        'fClef': ('bass', 0),
        'four_four': (' time=4/4\nnotes', 0),
        'quarter_note': (' :q ', 0.25),
        'half_note': (' :h ', 0.5),
        'half_note_dot': (' :hd ', 0.75),
        'dot_half_note': (' :hd ', 0.75),
        'dot_half_note_dot': (' :hd ', 0.75),
        'quarter_note_dot': (' :qd ', 0.375),
        'dot_quarter_note_dot': (' :qd ', 0.375),
        'eight_note': (' :8 ', 0.125),
        'whole_note': (' :w ', 1),
        'quarter_rest': (' :4 ##', 0.25),
        'sharp': (' #', 0)  # Adding sharp handling
    }

    for result in mapped_result_list:
        sen = "\ntabstave notation=true clef="  # Start a new tabstave for each list
        current_time = 0  # Initialize current time for each line
        sharp_count = 0  # Initialize sharp count for each line
        four_four_added = False  # Flag to check if 4/4 is added
        clef_added = False  # Flag to check if clef is added
        clef_type = ""

        for i, item in enumerate(result):
            action, value = note_mapping.get(item[0], ('', 0))

            if item[0] == 'sharp':
                sharp_count += 1
                continue  # Skip adding sharp symbol to the sentence

            if item[0] in ['gClef', 'fClef'] and not clef_added:
                clef_added = True
                clef_type = item[0]

            if item[0] == 'four_four' and not four_four_added:
                four_four_added = True
                if sharp_count == 1:
                    sen += " key=G "  # Add key=G if exactly one sharp
                    sharp_count = 0  # Reset sharp count after adding key=G
                elif sharp_count == 2:
                    sen += " key=D "  # Add key=D if exactly two sharps
                    sharp_count = 0  # Reset sharp count after adding key=D

            if current_time + value > 1:  # If the bar length exceeds 1, add a bar line
                sen += " |"
                current_time = 0

            if action:  # Add the action to the sentence
                sen += action
                if item[0] not in ['gClef', 'fClef', 'four_four', 'quarter_rest']:
                    sen += item[1]  # Add note detail if applicable

            current_time += value

        # Check for clef without four_four
        if clef_added and not four_four_added:
            if sharp_count == 1:
                if clef_type == 'gClef':
                    sen = sen.replace('clef=treble', 'clef=treble key=G\nnotes')
                elif clef_type == 'fClef':
                    sen = sen.replace('clef=bass', 'clef=bass key=G\nnotes')
            elif sharp_count == 2:
                if clef_type == 'gClef':
                    sen = sen.replace('clef=treble', 'clef=treble key=D\nnotes')
                elif clef_type == 'fClef':
                    sen = sen.replace('clef=bass', 'clef=bass key=D\nnotes')
            else:
                if clef_type == 'gClef':
                    sen = sen.replace('clef=treble', 'clef=treble \nnotes')
                elif clef_type == 'fClef':
                    sen = sen.replace('clef=bass', 'clef=bass \nnotes')
        elif clef_added and four_four_added:
            if sharp_count == 1:
                sen = sen.replace('\nnotes', ' key=G\nnotes')
            elif sharp_count == 2:
                sen = sen.replace('\nnotes', ' key=D\nnotes')
        sen += " =|="
        complete_sentence += sen

    return complete_sentence




def remove_notes(lst):
    # 비슷한 요소들 중 마지막 요소를 제외하고 리스트를 반환
    to_keep = []
    n = len(lst)
    for i in range(n):
        keep = True
        for j in range(i + 1, n):
            if abs(lst[i][-1] - lst[j][-1]) <= 3:
                keep = False
                break
        if keep:
            to_keep.append(lst[i])
    return to_keep

def standardize_sharps(rec_list):
    sharp_counts = [sum(1 for item in line if item[1] == 'sharp') for line in rec_list]
    max_sharps = max(sharp_counts)

    if max_sharps == 0:
        return rec_list

    max_sharp_index = sharp_counts.index(max_sharps)
    y_value = next(item[0] for item in rec_list[max_sharp_index] if item[1] == 'sharp')
    x_value = next(item[2] for item in rec_list[max_sharp_index] if item[1] == 'sharp')

    for i, line in enumerate(rec_list):
        current_sharps = sharp_counts[i]
        if current_sharps < max_sharps:
            difference = max_sharps - current_sharps
            for _ in range(difference):
                for idx, item in enumerate(line):
                    if item[1] == 'gClef':
                        line.insert(idx + 1, [y_value, 'sharp', x_value])
                        break

    return rec_list

def standardize_keysharps(note_list2):
    keysharp_counts = [sum(1 for item in line if item[1] == 'keySharp') for line in note_list2]
    max_keysharps = max(keysharp_counts)

    if max_keysharps == 0:
        return note_list2

    max_keysharp_index = keysharp_counts.index(max_keysharps)
    y_value = next(item[0] for item in note_list2[max_keysharp_index] if item[1] == 'keySharp')
    x_value = next(item[2] for item in note_list2[max_keysharp_index] if item[1] == 'keySharp')

    for i, line in enumerate(note_list2):
        current_keysharps = keysharp_counts[i]
        if current_keysharps < max_keysharps:
            difference = max_keysharps - current_keysharps
            for _ in range(difference):
                for idx, item in enumerate(line):
                    if item[1] == 'gClef':
                        line.insert(idx + 1, [y_value, 'keySharp', x_value])
                        break

    return note_list2



def synchronize_sharps_and_keysharps(rec_list, note_list2):
    """
    rec_list에서 각 줄의 'sharp' 개수와 note_list2에서 각 줄의 'keySharp' 개수를 센다.
    두 리스트 중 더 큰 값의 샵 개수를 바탕으로 더 적은 쪽의 샵 리스트를 수정한다.
    """
    for i in range(len(rec_list)):
        # 각 줄에서 sharp와 keySharp의 개수를 셈
        sharp_count = sum(1 for item in rec_list[i] if item[1] == 'sharp')
        keysharp_count = sum(1 for item in note_list2[i] if item[1] == 'keySharp')

        # 더 큰 값을 기준으로 설정
        max_count = max(sharp_count, keysharp_count)

        # rec_list의 sharp 개수가 부족할 경우 추가
        if sharp_count < max_count:
            difference = max_count - sharp_count
            y_value = next((item[0] for item in rec_list[i] if item[1] == 'sharp'), rec_list[i][0][0])
            x_value = next((item[2] for item in rec_list[i] if item[1] == 'sharp'), rec_list[i][0][2])
            for _ in range(difference):
                rec_list[i].insert(1, [y_value, 'sharp', x_value])  # gClef 뒤에 추가

        # note_list2의 keySharp 개수가 부족할 경우 추가
        if keysharp_count < max_count:
            difference = max_count - keysharp_count
            y_value = next((item[0] for item in note_list2[i] if item[1] == 'keySharp'), note_list2[i][0][0])
            x_value = next((item[2] for item in note_list2[i] if item[1] == 'keySharp'), note_list2[i][0][2])
            for _ in range(difference):
                note_list2[i].insert(1, [y_value, 'keySharp', x_value])  # gClef 뒤에 추가

    return rec_list, note_list2

