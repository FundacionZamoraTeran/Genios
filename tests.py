import unittest
import engine

class MultipleChoiceQuizBaseTests(unittest.TestCase):
    '''Tests for MultipleChoiceQuizBase'''
    asset_file = 'sabio.json'

    def test_init(self):
        obj = engine.MultipleChoiceQuizBase(self.asset_file)
        self.assertNotEqual(len(obj.questions), 0)

        obj = engine.MultipleChoiceQuizBase(self.asset_file, dont_load=True)
        self.assertEqual(len(obj.questions), 0)

    def test_load_questions(self):
        '''test_load_questions: this might fail with small data'''
        obj = engine.MultipleChoiceQuizBase(self.asset_file, dont_load=True)
        obj.load_questions()
        questions = engine.load_json('sabio.json')

        self.assertNotEqual(obj.questions[0], questions[0])

    def test_get_random_question(self):
        obj = engine.MultipleChoiceQuizBase(self.asset_file)
        question_len = len(obj.questions)
        used_question_len = len(obj.used_questions)

        self.assertNotEqual(question_len, used_question_len)
        q = obj.get_random_question()
        self.assertTrue(q)
        self.assertEqual(len(obj.questions), question_len - 1)
        self.assertEqual(len(obj.used_questions), used_question_len + 1)

class EngineTests(unittest.TestCase):
    '''Utils testing'''

    def test_load_json(self):
        obj = engine.load_json('sabio.json')
        self.assertEquals(type(obj), list)
