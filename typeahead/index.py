import re
import os
from os.path import join
import heapq
from collections import defaultdict
from typeahead.convert_kor import decompose_korean


def bytes2int(bytes):
    return int.from_bytes(bytes, byteorder="little")


def _read_binary_index(f):
    index = defaultdict(list)
    while True:
        size = bytes2int(f.read(1))
        if not size:
            break
        prefix = f.read(size).decode()
        for i in range(bytes2int(f.read(1))):
            size, count = bytes2int(f.read(1)), bytes2int(f.read(4))
            word = f.read(size).decode()
            index[prefix].append((count, word))

    return index


class SearchIndex:
    def __init__(self, max_heap_size, max_prefix_size):
        self.version = None
        self.index = None
        self.max_heap_size = max_heap_size
        self.max_prefix_size = max_prefix_size

    def info(self):
        assert self.index, "Index is not loaded"
        return {
            "version": self.version,
            "max_heap_size": self.max_heap_size,
            "max_prefix_size": self.max_prefix_size,
        }

    def make_index(self, input_path):
        with open(input_path, 'r', encoding='utf-8-sig') as f:
            # calculate
            self.index = defaultdict(list)
            for line in f:
                word, count = tuple(line.split())
                count = int(count)
                origin_word = word[:]

                if len(word) >= 20:  # skip too long word
                    continue

                for c in list(word):
                    if ord(c) >= 255:
                        word = decompose_korean(word)
                        break

                for i in range(1, len(word[:self.max_prefix_size + 1])):
                    prefix = word[:i]

                    if len(self.index[prefix]) < self.max_heap_size:
                        heapq.heappush(self.index[prefix], (count, origin_word))
                    else:
                        heapq.heappushpop(self.index[prefix], (count, origin_word))

        # sort
        for prefix in self.index.keys():
            self.index[prefix].sort(key=lambda x: x[0], reverse=True)

    def save(self, output_dir, version: str):
        assert self.index, "Index is not loaded"
        assert version, "Index version must be specified"
        filename = f"{version}.bin"

        # write binary
        with open(join(output_dir, filename), 'wb') as f:
            # write header
            encoded = version.encode()
            f.write(bytes([len(encoded)]) + encoded)
            f.write(bytes([self.max_heap_size, self.max_prefix_size]))

            # write index
            for prefix, word_list in self.index.items():
                encoded = prefix.encode()
                f.write(bytes([len(encoded)]) + encoded + bytes([len(word_list)]))
                for i, (count, word) in enumerate(word_list):
                    encoded = word.encode()
                    f.write(bytes([len(encoded)]) + count.to_bytes(4, byteorder="little") + encoded)

    def load(self, input_dir, filename: str):
        assert filename, "Index name must be specified"
        filename = f"{filename}.bin"
        # read binary
        with open(join(input_dir, filename), 'rb') as f:
            # read header
            size = bytes2int(f.read(1))
            version = f.read(size).decode()
            max_heap_size, max_prefix_size = bytes2int(f.read(1)), bytes2int(f.read(1))

            self.version = version
            self.max_heap_size = max_heap_size
            self.max_prefix_size = max_prefix_size

            # read index
            self.index = _read_binary_index(f)

        # check index to update manually
        if os.path.isfile(join(input_dir, "update.bin")):
            with open(join(input_dir, "update.bin"), 'rb') as f:
                update = _read_binary_index(f)
            for (prefix, words) in update.items():
                self.index[prefix] = words

    def search(self, prefix: str):
        assert self.index, "Index is not loaded"
        return self.index[decompose_korean(prefix)]
        # return [t[1] for t in self.index[prefix]] # words only
