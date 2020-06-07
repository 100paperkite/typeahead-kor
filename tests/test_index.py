import time
import shutil, tempfile
from os.path import dirname, join
from unittest.case import TestCase
from typeahead.index import SearchIndex


class TestIndex(TestCase):
    def setUp(self):
        self.count_path = join(dirname(__file__), "data/test_count.txt")
        self.test_dir = tempfile.mkdtemp()
        self.testIndex = SearchIndex()
        self.testIndex.make_index(self.count_path,
                                  max_prefix_size=2,
                                  max_heap_size=2)

    def test_make_correct_index(self):
        """
        Test if index can make its index according to max heap size & max prefix size
        """
        max_prefix_size = 2
        max_heap_size = 2
        content = {'t': ['the'],
                   'th': ['the'],
                   'p': ['pi', 'project'],
                   'pr': ['project', 'program'],
                   'o': ['of'], 'ㄴ': ['나'],
                   'ㅂ': ['비누', '비밀'],
                   'ㅂㅣ': ['비누', '비밀'],
                   'a': ['a형'], 'aㅎ': ['a형']}

        self.assertEqual(content, self.testIndex.index)
        self.assertEqual(max_prefix_size, self.testIndex.max_prefix_size)
        self.assertEqual(max_heap_size, self.testIndex.max_heap_size)

    def test_search(self):
        self.assertEqual(self.testIndex.search("p"), ['pi', 'project'])
        self.assertEqual(self.testIndex.search("k"), [])
        self.assertEqual(self.testIndex.search("ㄴ"), ['나'])
        self.assertEqual(self.testIndex.search("ㅂㅣ"), ['비누', '비밀'])

    def test_save_and_load(self):
        """
        Test if index can save & load its index in the binary format
        """
        self.testIndex.version = "test"

        index_path = join(self.test_dir, f"{self.testIndex.version}.bin")
        start_time = time.time()
        self.testIndex.save(index_path)
        print("total time for saving binary: ", time.time() - start_time)

        start_time = time.time()
        testIndex = SearchIndex()
        testIndex.load(index_path)
        print("total time for loading binary: ", time.time() - start_time)

        self.assertEqual(self.testIndex.info(), testIndex.info())
        self.assertEqual(self.testIndex.index, testIndex.index)

    def test_update(self):
        # remove words
        self.testIndex.update('p', [])
        self.assertEqual(self.testIndex.search('p'), [])

        # create new prefix
        self.testIndex.update('n', ['new', 'newest'])
        self.assertEqual(self.testIndex.search('n'), ['new', 'newest'])

        # overwrite word
        self.testIndex.update('pr', ['problem'])
        self.assertEqual(self.testIndex.search('pr')[0], 'problem')

    def test_delete(self):
        # '비' : ['비누', '비밀']
        self.testIndex.delete('ㅂㅣ', ['비누'])
        self.assertEqual(self.testIndex.search('ㅂㅣ'), ['비밀'])

        # check delete when words don't exist
        self.testIndex.delete('p', ['prove', 'please'])
        self.assertEqual(self.testIndex.search('p'), ['pi', 'project'])

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)
