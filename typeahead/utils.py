import re
import glob
from os import listdir
from os.path import join, isdir
from collections import defaultdict


def get_newest_index_path(root):
    # get a newest version of index
    version_dirs = [version for version in listdir(root) if isdir(join(root, version))]
    assert version_dirs, f"There's no version folders under {root}"
    # get a latest file of the version
    version_files = [
        index for index in glob.glob(join(join(root, max(version_dirs)), '*.bin')) if "increment.bin" not in index
    ]
    return max(version_files)


def bytes2int(bytes):
    return int.from_bytes(bytes, byteorder="little")


def read_binary_index(f):
    index = defaultdict(list)
    while True:
        size = bytes2int(f.read(1))
        if not size:
            break
        prefix = f.read(size).decode('utf-8')
        index[prefix] = []  # for update [] increment
        for i in range(bytes2int(f.read(1))):
            size = bytes2int(f.read(1))
            word = f.read(size).decode('utf-8')
            index[prefix].append(word)

    return index


def write_binary_index(f, index):
    for prefix, word_list in index.items():
        write_binary_index_element(f, prefix, word_list)


def write_binary_index_element(f, prefix, word_list):
    encoded = prefix.encode('utf-8')
    f.write(bytes([len(encoded)]) + encoded + bytes([len(word_list)]))
    for word in word_list:
        encoded = word.encode('utf-8')
        f.write(bytes([len(encoded)]) + encoded)


# 유니코드 한글 시작 : 44032, 끝 : 55199
BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ',
                 'ㅣ']

# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
                 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']


def decompose_korean(test_keyword):
    result = list()
    for keyword in list(test_keyword):
        # 한글 여부 check 후 분리
        if re.match('[가-힣]', keyword) is not None:
            char_code = ord(keyword) - BASE_CODE
            char1 = int(char_code / CHOSUNG)
            result.append(CHOSUNG_LIST[char1])
            char2 = int((char_code - (CHOSUNG * char1)) / JUNGSUNG)
            result.append(JUNGSUNG_LIST[char2])
            char3 = int((char_code - (CHOSUNG * char1) - (JUNGSUNG * char2)))
            if char3 != 0:
                result.append(JONGSUNG_LIST[char3])
        else:
            result.append(keyword)

    return ''.join(result)
