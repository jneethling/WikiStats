import wiki_stats_aggregator as wsa
from tornado.testing import AsyncHTTPTestCase
import json


class TestCountHandler(AsyncHTTPTestCase):
    def get_app(self):
        return wsa.make_app()

    def test_get(self):
        response = self.fetch("/totals")
        self.assertEqual(response.code, 200)
        try:
            json.loads(response.body)
        except ValueError:
            self.fail("Response is not valid json!")

