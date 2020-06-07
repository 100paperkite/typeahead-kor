import os
import heapq
from os.path import join
from collections import defaultdict
from typeahead.utils import decompose_korean, bytes2int, read_binary_index, write_binary_index


class SearchIndex:
    def __init__(self):
        self.index = None
        self.version = None
        self.max_heap_size = None
        self.max_prefix_size = None

    def info(self):
        assert self.index, "Index is not loaded"
        return {
            "version": self.version,
            "max_heap_size": self.max_heap_size,
            "max_prefix_size": self.max_prefix_size,
        }

    def search(self, prefix):
        assert self.index, "Index is not loaded"
        return self.index[prefix]

    def update(self, prefix, word_list):
        assert self.index, "Index is not loaded"
        if word_list:
            self.index[prefix][:len(word_list)] = [word for word in word_list]
        else:
            self.index[prefix] = []

    def delete(self, prefix, word_list):
        assert self.index, "Index is not loaded"
        self.index[prefix] = [item for item in self.index[prefix] if item not in word_list]

    def save(self, output_path):
        assert self.index, "Index is not loaded"
        assert self.max_heap_size, "Max heap size is not defined"
        assert self.max_prefix_size, "Max prefix size is not defined"
        output_dir = os.path.split(output_path)[0]
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # write binary
        with open(output_path, 'wb') as f:
            # write header & content
            f.write(bytes([self.max_heap_size, self.max_prefix_size]))
            write_binary_index(f, self.index)

    def load(self, data_path):
        data_dir, self.version = os.path.split(data_path)
        self.version = ".".join(self.version.split('.')[:-1])

        # read binary
        with open(data_path, 'rb') as f:
            # read header
            max_heap_size, max_prefix_size = bytes2int(f.read(1)), bytes2int(f.read(1))
            self.max_heap_size = max_heap_size
            self.max_prefix_size = max_prefix_size
            self.index = read_binary_index(f)

        # check increment
        if os.path.isfile(join(data_dir, "increment.bin")):
            with open(join(data_dir, "increment.bin"), 'rb') as f:
                update = read_binary_index(f)
            for (prefix, words) in update.items():
                print(prefix, words)
                self.index[prefix] = words

    def make_index(self, input_path, max_heap_size, max_prefix_size):
        assert max_heap_size, "Max heap size must be specified"
        assert max_prefix_size, "Max prefix size must be specified"

        self.max_heap_size = max_heap_size
        self.max_prefix_size = max_prefix_size

        with open(input_path, 'r', encoding='utf-8-sig') as f:
            # calculate
            self.index = defaultdict(list)
            for line in f:
                word, count = tuple(line.split())
                count = int(count)
                origin_word = word[:]

                if len(word) >= 20:  # skip too long word
                    continue

                # Decompose if word contains Korean
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
            self.index[prefix] = [word for (count, word) in sorted(self.index[prefix], reverse=True)]

