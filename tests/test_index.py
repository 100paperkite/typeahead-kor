import time
from os.path import dirname, join
from unittest.case import TestCase
from typeahead.index import SearchIndex


class TestIndex(TestCase):
    def setUp(self):
        self.testIndex = SearchIndex(max_heap_size=2, max_prefix_size=2)
        data_path = join(dirname(__file__), "test_data/test_count.txt")
        self.testIndex.make_index(data_path)

    def test_make_correct_index(self):
        """
        Test if index can make its index according to max heap size & max prefix size

        <test_count.txt>
        the 4507
        program 12
        project 88
        pi 100
        of 3731
        나 200
        비누 88
        비밀 12
        a형 40
        """
        answer = {'t': [(4507, 'the')],
                  'th': [(4507, 'the')],
                  'p': [(100, 'pi'), (88, 'project')],
                  'pr': [(88, 'project'), (12, 'program')],
                  'o': [(3731, 'of')], 'ㄴ': [(200, '나')],
                  'ㅂ': [(88, '비누'), (12, '비밀')],
                  'ㅂㅣ': [(88, '비누'), (12, '비밀')],
                  'a':[(40,'a형')], 'aㅎ':[(40,'a형')]}

        self.assertEqual(answer, self.testIndex.index)

    def test_search(self):
        self.assertEqual(self.testIndex.search("p"), [(100, 'pi'), (88, 'project')])
        self.assertEqual(self.testIndex.search("k"), [])
        self.assertEqual(self.testIndex.search("ㄴ"), [(200, '나')])
        self.assertEqual(self.testIndex.search("비"), [(88, '비누'), (12, '비밀')])

    def test_binary(self):
        """
        Test if index can save & load its index in the binary format
        """
        version = "test"
        data_dir = join(dirname(__file__), "test_data")

        start_time = time.time()
        self.testIndex.save(data_dir, version)
        print("total time for saving binary: ", time.time() - start_time)

        testIndex = SearchIndex(2, 2)
        start_time = time.time()
        testIndex.load(data_dir, version)
        print("total time for loading binary: ", time.time() - start_time)

        self.assertEqual(self.testIndex.index, testIndex.index)

