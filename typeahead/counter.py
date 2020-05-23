import re
from collections import Counter
from typeahead.convert_kor import convert


def preprocess_sentence(sentence):
    """
    split a sentence by white space & punctuation
    lowercase all tokens after removing (eng)
    only CHOSUNG (ex. ㅋㅋㅋㅋ) is removed (kor)

    param:
        sentence : sentence for tokenization
    """
    sentence = convert(sentence)
    return [tok.lower() for tok in re.split('[^a-zA-Z0-9ㄱ-ㅎㅏ-ㅣ#]+', sentence) if tok]

class WordCounter:
    def __init__(self):
        self.counter = Counter()

    def update(self, input_path):
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                self.counter.update(preprocess_sentence(line))

    def save(self, output_path):
        # write txt
        with open(output_path, 'w', encoding='utf-8') as f:
            for word, count in self.counter.items():
                f.write(word + " " + str(count) + '\n')