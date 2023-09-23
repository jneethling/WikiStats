from tornado.testing import AsyncHTTPTestCase
import json
import time
from src.handlers import CustomHandler
from src import router

class TestControls(AsyncHTTPTestCase):
    def get_app(self):
        c_handler = CustomHandler("./data/wiki_statsDB")
        return router.make_app(c_handler)

    def test_startstop(self):
        start_response = self.fetch("/start")
        self.assertEqual(start_response.code, 200)
        resp =json.loads(start_response.body)
        self.assertEqual(resp['message'], 'Function handler background work started')
        time.sleep(5)
        stop_response = self.fetch("/stop")
        self.assertEqual(stop_response.code, 200)
        resp =json.loads(stop_response.body)
        self.assertEqual(resp['message'], 'Function handler background work stopped')

    def test_ignorestart(self):
        self.fetch("/start")
        start_response = self.fetch("/start")
        self.assertEqual(start_response.code, 200)
        resp =json.loads(start_response.body)
        self.assertEqual(resp['message'], 'Function handler already working in background, ignoring request')
        self.fetch("/stop")