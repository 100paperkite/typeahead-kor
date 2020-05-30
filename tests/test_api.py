from unittest.case import TestCase
from typeahead.app import app
from typeahead.index import SearchIndex


class TestAPI(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_info(self):
        answer = {
            "version": "test",
            "max_heap_size": 2,
            "max_prefix_size": 2,
        }
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        self.assertEqual(answer, response.json)

    def test_liveness(self):
        response = self.client.get("/healthcheck")
        self.assertEqual(200, response.status_code)

    def test_update(self):
        pass
