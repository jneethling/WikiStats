from tornado.testing import AsyncHTTPTestCase
import json
from handlers import CustomHandler
import router

class TestHandlers(AsyncHTTPTestCase):
    def get_app(self):
        c_handler = CustomHandler()
        return router.make_app(c_handler)

    def test_getPing(self):
        response = self.fetch("/ping")
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'pong')

    def test_getMemory(self):
        response = self.fetch("/memory")
        self.assertEqual(response.code, 200)
        self.assertIn("Memory use", json.loads(response.body))

    def test_getStatus(self):
        response = self.fetch("/status")
        self.assertEqual(response.code, 200)
        resp = json.loads(response.body)
        self.assertIn("Status", resp)
        self.assertIn("Message", resp)
        self.assertIn("Working in background", resp)
        self.assertIn("Records in session", resp)

    def test_getTotals(self):
        response = self.fetch("/totals")
        self.assertEqual(response.code, 200)
        try:
            json.loads(response.body)
        except ValueError:
            self.fail("Response is not valid json!")

    def test_getCount(self):
        response = self.fetch("/counts")
        self.assertEqual(response.code, 200)
        try:
            json.loads(response.body)
        except ValueError:
            self.fail("Response is not valid json!")