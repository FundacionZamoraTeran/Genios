import json
import unittest
import os

from . import engine

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

    def test_empty_game_state(self):
        gs = engine.GameState()
        data = json.loads(gs.to_json())

        self.assertEquals(data['available_levels'], gs.available_levels)
        self.assertEquals(data['locked_levels'], gs.locked_levels)

    def test_game_state_init(self):
        gs = engine.GameState(available_levels = ['lol', 'foo', 'bar'], locked_levels=['castle'])
        data = json.loads(gs.to_json())

        self.assertEquals(data['available_levels'], gs.available_levels)
        self.assertEquals(data['locked_levels'], gs.locked_levels)

    def test_save_data(self):
        gs = engine.GameState(available_levels = ['lol', 'foo', 'bar'], locked_levels=['castle'])
        gs.save()

        self.assertTrue(os.path.exists('data/savegame.json'))

    def test_load_data(self):
        gs = engine.GameState(available_levels = ['lol', 'foo', 'bar'], locked_levels=['castle'])
        gs.save()

        self.assertTrue(os.path.exists('data/savegame.json'))
