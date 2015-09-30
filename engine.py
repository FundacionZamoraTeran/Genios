import json
from random import shuffle

class MultipleChoiceQuizBase(object):
    #to store used questions
    used_questions = []
    #stores questions to ask
    questions = []

    def __init__(self, asset_file, dont_load=False):
        self.asset_file = asset_file
        if not dont_load:
            self.load_questions()

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

class SabioData(MultipleChoiceQuizBase):

    def __init__(self, dont_load=False):
        super(SabioData, self).__init__('sabio.json', dont_load)

#utils funtions
def load_json(file_name):
    contents = open("data/%s" % file_name, 'r').read()
    return json.loads(contents)



