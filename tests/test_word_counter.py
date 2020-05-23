import string
import unittest
from unittest.case import TestCase
from typeahead.counter import preprocess_sentence


class TestSplitSentence(TestCase):
    """
    Test if sentences split by punctuation & whitespace
    """
    def test_correct_split(self):
        """
        punctuation: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        whitespace : space, tab, linefeed, return, formfeed, and vertical tab
        """
        test_data = "WoRd".join(string.punctuation) + "WoRd".join(string.whitespace)
        answer = ["word"] * (len(string.punctuation) + len(string.whitespace) - 2)
        self.assertEqual(preprocess_sentence(test_data), answer)


if __name__ == '__main__':
    unittest.main()
