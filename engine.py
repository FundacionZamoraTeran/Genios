import json
from random import shuffle


class GameState(object):
    '''simple class to store game data'''
    FILE_NAME =  'data/savegame.json'
    default_data = {
                    'available_levels': ['cloud'],
                    'locked_levels': ['book', 'feather', 'lamp'],
                   }

    def __init__(self, *args, **kwargs):
        if kwargs.get('load'):
            pass
        else:
            self.available_levels = kwargs.get('available_levels', self.default_data['available_levels'])
            self.locked_levels = kwargs.get('locked_levels', self.default_data['locked_levels'])

    def to_json(self):
        data = {}
        data['available_levels'] = self.available_levels
        data['locked_levels'] = self.locked_levels
        return json.dumps(data)

    def save(self):
        f = open(self.FILE_NAME, 'w')
        f.write(self.to_json())
        f.close()

    def load(self):
        try:
            f = open(self.FILE_NAME, 'r')
            data = json.loads(f.read())
            f.close()
            j
            self.available_levels = data.get('available_levels', self.default_data['available_levels'])
            self.locked_levels = data.get('locked_levels', self.default_data['locked_levels'])
        except:
            data = self.default_data

game_state_singleton = GameState()

def get_game_state(self):
    global game_state_singleton
    return game_state_singleton


class MultipleChoiceQuizBase(object):
    #to store used questions
    used_questions = []
    #stores questions to ask
    questions = []

    def __init__(self, asset_file, dont_load=False, game_state={}):
        self.asset_file = asset_file
        if not dont_load:
            self.load_questions()

        self.max_lives = 3
        self.current_lives = self.max_lives
        self.score = 0
        self.game_state = GameState(**game_state)

    def win(self):
        self.score += 1

    def loss(self):
        self.current_lives -= 1

    def game_over(self):
        return self.current_lives < 1

    def has_won(self):
        return len(self.questions) == 0

    def load_questions(self):
        self.questions = load_json(self.asset_file)
        #randomizing the list
        shuffle(self.questions)
        self.used_questions = []

    def get_random_question(self):
        if len(self.questions) == 0:
            #reload questions because there is no content!
            self.load_questions()

        question = self.questions.pop(0)
        self.used_questions.append(question)
        return question

    def read_file(self, path, use_sugar=False):
        pass

    def write_file(self, path, use_sugar=False):
        '''this should be called when the user gain a new level'''
        pass

class SabioData(MultipleChoiceQuizBase):

    def __init__(self, dont_load=False):
        super(SabioData, self).__init__('sabio.json', dont_load)

class PoetaData(MultipleChoiceQuizBase):

    def __init__(self, dont_load=False):
        super(PoetaData, self).__init__('poeta.json', dont_load)

class CuenteroData(MultipleChoiceQuizBase):

    def __init__(self, dont_load=False):
        super(CuenteroData, self).__init__('cuentero.json', dont_load)

class GenioData(MultipleChoiceQuizBase):

    def __init__(self, dont_load=False):
        super(GenioData, self).__init__('genio.json', dont_load)


#utils funtions
def load_json(file_name):
    contents = open("data/%s" % file_name, 'r').read()
    return json.loads(contents)



