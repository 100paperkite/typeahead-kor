from unittest.case import TestCase
from typeahead import app
from typeahead.index import SearchIndex
from os.path import abspath, dirname, join


class TestAPI(TestCase):
    def setUp(self) -> None:
        index_dir = join(dirname(__file__),"data")
        searchIndex = SearchIndex(2, 2)
        searchIndex.load(index_dir,"test")
        self.tester = app.test_client()

    def test_search(self):
        result = self.tester.get("/search/p")
        self.assertEqual(result,[(100, 'pi'), (88, 'project')])
