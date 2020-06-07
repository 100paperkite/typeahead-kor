import string
import unittest
from unittest.case import TestCase
from typeahead.word_counter import preprocess_sentence


class TestSplitSentence(TestCase):
    """
    Test if sentences split by punctuation & whitespace
    """
    def test_correct_split(self):
        test_data1 = "WoRd".join(string.punctuation) + "WoRd".join(string.whitespace)
        test_data2 = "가나 다라 마바사ㅋㅋ!!"

        answer1 = ["word"] * (len(string.punctuation) + len(string.whitespace) - 2)
        answer2 = ["가나", "다라", "마바사"]
        self.assertEqual(preprocess_sentence(test_data1), answer1)
        self.assertEqual(preprocess_sentence(test_data2),answer2)

