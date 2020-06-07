import os
from unittest.case import TestCase
from typeahead.app import app

"""
index = {'t': ['the'],
         'th': ['the'],
         'p': ['pi', 'project'],
         'pr': ['project', 'program'],
         'o': ['of'], 'ㄴ': ['나'],
         'ㅂ': ['비누', '비밀'],
         'ㅂㅣ': ['비누', '비밀'],
         'a': ['a형'], 'aㅎ': ['a형']}
"""


class TestAPI(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_1(self):
        answer = {
            "version": "0",
            "max_heap_size": 2,
            "max_prefix_size": 2,
        }

        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        self.assertEqual(answer, response.json)

    def test_2(self):
        response = self.client.get("/healthcheck")
        self.assertEqual(200, response.status_code)

    def test_3(self):
        response1 = self.client.get("/search/t")
        response2 = self.client.get("/search/aㅎ")
        self.assertEqual(["the"], response1.json)
        self.assertEqual(["a형"], response2.json)

    def test_4(self):
        response1 = self.client.post("/admin/index/p", json={"words": []})
        response2 = self.client.post("/admin/index/비", json={"words": ["비디오", "비빔면"]})
        print(response2.json)
        self.assertEqual(201, response1.status_code)
        self.assertEqual(201, response2.status_code)

    def test_5(self):
        response = self.client.delete("/admin/index/pr", json={"words": ["program"]})
        self.assertEqual(200, response.status_code)

    def test_6(self):
        response = self.client.post('/admin/index/reload')
        self.assertEqual(201, response.status_code)

    def test_7(self):
        self.assertEqual(self.client.get("/search/비").json, ["비디오","비빔면"])
        self.assertEqual(self.client.get("/search/pr").json, ["project"])
        self.assertEqual(self.client.get("/search/p").json, [])


