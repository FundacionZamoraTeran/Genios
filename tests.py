import unittest
import engine

class EngineTests(unittest.TestCase):

    def test_load_json(self):
        obj = engine.load_json('sabio.json')
        self.assertEquals(type(obj), list)
