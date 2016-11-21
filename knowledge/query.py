# coding=utf8

import argparse
import ltp
import json
from neo4j.v1 import GraphDatabase

class Db(object):
    def find_entity(self, entity_name):
        pass

    def find_entity(self, from_entity, edge):
        pass

    def find_relation(self, relation_name):
        pass

    def find_relation(self, from_entity, to = None):
        pass

class Word(object):
    def __init__(self, dict):
        self.word = dict

    def is_subject(self):
        return self.word['relate'] == 'SBV'

    def is_relation(self):
        return self.word['relate'] == 'HED'

    def is_direct_object(self):
        return self.word['relate'] in ['VOB', 'FOB']

    def is_indirect_object(self):
        return self.word['relate'] == 'IOB'

    def is_unknown_word(self):
        return self.word['cont'] in ['谁','什么','怎么','怎么样','为什么']

    def get_content(self):
        return self.word['cont']


class Query(object):
    def lookup(self, text):
        api = ltp()
        self.analyze_query(api.call(text, 'all'))
        pass

    def analyze_query(self, response):
        body = json.loads(response)

        subj = None
        verb = None
        direct_obj = None
        indirect_obj = None

        for paragraph in body:
            for sentence in paragraph:
                for word in sentence:
                    w = Word(word)
                    if w.is_subject():
                        subj = w
                    elif w.is_relation():
                        verb = w
                    elif w.is_direct_object():
                        direct_obj= w
                    elif w.is_indirect_object():
                        indirect_obj = w

        db = Db()


        if subj.is_unknown_word():
            if verb:
                relations = db.find_relation(verb.get_content())
                for r in relations:
                    yield

    def is_unknown_word(self, word):
        return word in ['谁','什么','怎么','怎么样','为什么']

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'text', help='text')

    args = parser.parse_args()
    query = Query()
    print query.lookup(args.text)
