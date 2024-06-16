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

    rec_list = fs.standardize_sharps(rec_list)
    note_list2 = fs.standardize_keysharps(note_list2)

    rec_list, note_list2 = fs.synchronize_sharps_and_keysharps(rec_list, note_list2)

    md.process_pitches(rec_list, pitch_list)
    md.update_notes(note_list2, note_list)
    final_list = md.merge_lists(rec_list, note_list2, pitch_list)

    sen = fs.convert_to_sentence(final_list)

    print("\n-Result-")

    print(sen)

    end = time.time()

    print(f"\ntotal time: {end - start:.1f} sec")

    return sen
