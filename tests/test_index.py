import time
from os.path import dirname, abspath, join
import unittest
from unittest.case import TestCase
from typeahead.index import SearchIndex


class TestIndex(TestCase):
    def setUp(self) -> None:
        self.testIndex = SearchIndex(2, 2)  # data_dir, max_heap_size, max_prefix_size

    def test_make_index(self):
        """
        Test if index can make its index according to max heap size & max prefix size
        """
        data_path = join(dirname(__file__), "data/test_count.txt")
        self.testIndex.make_index(data_path)
        """
        <test_count.txt>
        the 4507
        program 12
        project 88
        pi 100
        of 3731
        ㄴㅏ# 200
        ㅂㅣ#ㄴㅜ 88
        ㅂㅣ#ㅁㅣㄹ 12
        """
        answer = {'t': [(4507, 'the')],
                  'th': [(4507, 'the')],
                  'p': [(100, 'pi'), (88, 'project')],
                  'pr': [(88, 'project'), (12, 'program')],
                  'o': [(3731, 'of')], 'ㄴ': [(200, 'ㄴㅏ#')],
                  'ㄴㅏ': [(200, 'ㄴㅏ#')],
                  'ㅂ': [(88, 'ㅂㅣ#ㄴㅜ'), (12, 'ㅂㅣ#ㅁㅣㄹ')],
                  'ㅂㅣ': [(88, 'ㅂㅣ#ㄴㅜ'), (12, 'ㅂㅣ#ㅁㅣㄹ')],}

        self.assertEqual(answer, self.testIndex.index)

    def test_search(self):
        self.test_make_index()
        self.assertEqual(self.testIndex.search("p"), [(100, 'pi'), (88, 'project')])
        self.assertEqual(self.testIndex.search("k"), [])

    def test_binary(self):
        """
        Test if index can save & load its index in the binary format
        """
        self.test_make_index()

        version = "test"
        data_dir = join(dirname(__file__), "test")

        start_time = time.time()
        self.testIndex.save(data_dir, version)
        print("total time for saving binary: ", time.time() - start_time)

        testIndex = SearchIndex(2, 2)
        start_time = time.time()
        testIndex.load(data_dir, version)
        print("total time for loading binary: ", time.time() - start_time)

        self.assertEqual(self.testIndex.index, testIndex.index)


if __name__ == '__main__':
    unittest.main()
