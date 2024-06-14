import cv2
import numpy as np
import functions as fs
import modules as md
import pitchDetection
import time


def convert(source):
    # source가 numpy.ndarray 인스턴스인지 확인합니다.
    if isinstance(source, np.ndarray):
        # source가 이미 numpy.ndarray 형태라면 바로 사용합니다.
        src = source
    else:
        # source가 numpy.ndarray가 아니라면, 파일 경로로 간주하고 이미지를 로드합니다.
        src = cv2.imread(source)

    final_list = []

    print("Converting start")
    start = time.time()

    image = md.deskew(src)
    image_0, subimages = md.remove_noise(image)

    normalized_images, stave_list = md.digital_preprocessing(image_0, subimages)

    first = time.time()
    print(f"\npreprocessing End {first - start:.1f} sec")

    rec_list, note_list, rest_list = md.beat_extraction(normalized_images)
    second = time.time()

    print(f"\nBeat Detection End {second - first:.1f} sec")

    clef_list = pitchDetection.detect1(cv2.cvtColor(cv2.bitwise_not(image_0), cv2.COLOR_GRAY2BGR))

    note_list2, pitch_list = md.pitch_extraction(stave_list, normalized_images, clef_list)

    third = time.time()
    print(f"\nPitch Detection End {third - second:.1f} sec")

    for i, (rec, pitches) in enumerate(zip(rec_list, pitch_list)):
        sharps, flats = fs.count_sharps_flats(rec)
        temp_dict = {}
        modified_pitches = fs.modify_notes(pitches, sharps, flats)
        for pit in modified_pitches:
            positions = fs.get_guitar(pit)
            temp_dict[pit] = positions
        modified_pitches = fs.calculate_efficient_positions(modified_pitches, temp_dict)
        pitch_list[i] = modified_pitches  # Update the pitch_list with modified pitches

    for note2, note1 in zip(note_list2, note_list):
        note2[1:] = fs.update_notes(note2[1:], note1)

    for list1, list2, list3 in zip(rec_list, note_list2, pitch_list):
        m_list = fs.merge_three_lists(list1, list2, list3)
        final_list.append(m_list)

    sen = fs.convert_to_sentence(final_list)

    print("\n-Result-")

    print(sen)

    end = time.time()

    print(f"\ntotal time: {end - start:.1f} sec")

    return sen