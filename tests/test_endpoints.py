from tornado.testing import AsyncHTTPTestCase
import json
from src.handlers import CustomHandler
from src import router
#import pytest

c_handler = CustomHandler()
c_handler.cursor.execute('''DELETE FROM stats''')
c_handler.db.commit()
c_handler.cursor.execute('''INSERT INTO stats(country_name, change_size) VALUES(?,?)''', ("United States", 3))
c_handler.db.commit()

class TestHandlers(AsyncHTTPTestCase):
    def get_app(self):
        #c_handler = CustomHandler()
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
        self.assertTrue(resp["Status"])
        self.assertIn("Message", resp)
        self.assertIn("Working in background", resp)
        self.assertIn("Records in session", resp)
        self.assertIn("DB size (bytes)", resp)
        self.assertIn("Modified", resp)

    def test_getTotals(self):
        response = self.fetch("/totals")
        self.assertEqual(response.code, 200)
        resp =json.loads(response.body)
        self.assertIn("United States", resp)
        self.assertEqual(resp["United States"], 3)

    def test_getCount(self):
        response = self.fetch("/counts")
        self.assertEqual(response.code, 200)
        resp = json.loads(response.body)
        self.assertIn("United States", resp)
        self.assertEqual(resp["United States"], 1)