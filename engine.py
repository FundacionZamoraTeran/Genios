import os
import json


def load_json(file_name):
    contents = open("data/%s" % file_name, 'r').read()
    return json.loads(contents)
