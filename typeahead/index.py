import json
import os
from os.path import join, dirname
import heapq
from collections import defaultdict
import struct


def read_binary_index(f, max_heap_size):
    index = defaultdict(list)
    while True:
        size = f.read(1)
        if not size:
            break
        prefix = f.read(ord(size)).decode()

        for i in range(max_heap_size):
            size = ord(f.read(1))
            if size == 0:
                break
            word, count = struct.unpack(f"<{size}sI", f.read(size + 4))
            index[prefix].append((count, word.decode()))

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

                if len(word) >= 50:  # skip too long word
                    continue
                for i in range(1, len(word[:self.max_prefix_size + 1])):
                    prefix = word[:i]
                    if len(self.index[prefix]) < self.max_heap_size:
                        heapq.heappush(self.index[prefix], (count, word))
                    else:
                        heapq.heappushpop(self.index[prefix], (count, word))
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
            f.write(struct.pack(f"<B{len(version)}s", len(version), version.encode()))
            f.write(struct.pack("<II", self.max_heap_size, self.max_prefix_size))

            # write index
            for prefix, word_list in self.index.items():
                f.write(struct.pack(f"<B{len(prefix)}s", len(prefix), prefix.encode()))
                for i, (count, word) in enumerate(word_list):
                    f.write(struct.pack(f"<B{len(word)}sI", len(word), word.encode(), count))
                if i + 1 != self.max_heap_size:
                    f.write(b"\0")

    def load(self, input_dir, version: str):
        assert version, "Index version must be specified"
        filename = f"{version}.bin"

        # read binary
        with open(join(input_dir, filename), 'rb') as f:
            # read header
            size = ord(f.read(1))
            version, max_heap_size, max_prefix_size = struct.unpack(f"<{size}sII", f.read(size + 8))
            version = version.decode()

            self.version = version
            self.max_heap_size = max_heap_size
            self.max_prefix_size = max_prefix_size

            # read index
            self.index = read_binary_index(f, self.max_heap_size)

        # check index to update manually
        if os.path.isfile(join(input_dir, "update.bin")):
            with open(join(input_dir, "update.bin"), 'rb') as f:
                update = read_binary_index(f, self.max_heap_size)
            for (prefix, words) in update.items():
                self.index[prefix] = words

    def search(self, prefix: str):
        assert self.index, "Index is not loaded"
        return self.index[prefix]
        # return [t[1] for t in self.index[prefix]] # words only


if __name__ == "__main__":
    searchIndex = SearchIndex(5, 5)
    searchIndex.make_index("../data/count/count_movie_rating.txt")
    searchIndex.save("../data/index", "test_kor")
    searchIndex.load("../data/index", "test_kor")
    print("Search start...")
    while True:
        prefix = input()
        print(searchIndex.search(prefix))
