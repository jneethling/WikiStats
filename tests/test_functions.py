import unittest
from src.handlers import CustomHandler

testInstance = CustomHandler()

class FunctionTests(unittest.TestCase):

    def testdbNotReady(self):
        self.assertFalse(testInstance.dbReady("/Bad_path"))
    
    def testdbReady(self):
        self.assertTrue(testInstance.dbReady("./data/wiki_statsDB"))