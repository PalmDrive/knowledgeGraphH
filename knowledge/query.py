# coding=utf8

import argparse
from ltp import nlpAPI
import json

class Db(object):
    def find_from_entity(self, edge):
        return 'from_entity <- ' + str(edge)

    def find_to_entity(self, edge):
        return 'to_entity <- ' + str(edge)

    def find_relations(self, relation_name, **kwargs):
        edge = {'relation' : 'relation_name ' + relation_name + str(kwargs.items()), 'IO':'abc'}
        print edge
        return [edge]


class Word(object):
    def __init__(self, dict):
        self.word = dict
        self.parent = None

    def is_subject(self):
        return self.word['relate'] == 'SBV'

    def is_relation(self):
        return self.word['relate'] == 'HED'

    def is_direct_object(self):
        # print self.word
        # print 'parent : ' + str(self.parent_id())
        # print str(self.parent.id())
        return self.word['relate'] in ['VOB', 'FOB'] and self.parent and self.parent.is_relation()

    def is_indirect_object(self):
        return self.word['relate'] == 'IOB' \
               or \
                (
                   (self.word['relate'] == 'VOB' or self.word['relate'] == 'POB')
                    and self.parent
                    and self.parent.get_parent()
                    and self.parent.get_parent().is_relation()
                )

    def is_complement(self):
        return self.word['relate'] == 'CMP'

    def is_unknown_word(self):
        return self.word['cont'] in [u'谁',u'什么',u'怎么',u'怎么样',u'为什么',u'哪个']

    def get_content(self):
        return self.word['cont']

    def id(self):
        return self.word['id']

    def parent_id(self):
        return self.word['parent']

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent


class Query(object):
    def lookup(self, text):
        api = nlpAPI()
        res = api.call(text, 'all')
        body = json.loads(res)
        return ', '.join(self.query(body))

    def query(self, body):
        subj = None
        verb = None
        direct_obj = None
        indirect_obj = None

        words = {}
        for paragraph in body:
            for sentence in paragraph:
                for word in sentence:
                    w = Word(word)
                    words[w.id()] = w

        for id, w in words.items():
            parent = words.get(w.parent_id())
            # print id
            # print 'parent : ' + str(w.parent_id())
            # if parent:
            #     print str(parent.id())
            w.set_parent(parent)

        for id, w in words.items():
            if w.is_subject():
                subj = w
            elif w.is_relation():
                verb = w
            elif w.is_direct_object():
                direct_obj = w
            elif w.is_indirect_object():
                indirect_obj = w


        db = Db()

        ans = []
        if verb and not verb.is_unknown_word():
            from_entity_name = subj.get_content() if subj and not subj.is_unknown_word() else None
            to_entity_name = direct_obj.get_content() if direct_obj and not direct_obj.is_unknown_word() else None
            IO = indirect_obj.get_content() if indirect_obj and not indirect_obj.is_unknown_word() else None

            relations = db.find_relations(verb.get_content(), from_entity_name=from_entity_name, to_entity_name=to_entity_name,
                                          IO=IO)

            for relation in relations:
                if subj and subj.is_unknown_word():
                    ans.append(db.find_from_entity(relation))
                elif direct_obj and direct_obj.is_unknown_word():
                    ans.append(db.find_to_entity(relation))
                elif indirect_obj and indirect_obj.is_unknown_word():
                    ans.append(relation["IO"])

        return ans

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'text', help='text')

    args = parser.parse_args()
    query = Query()
    print query.lookup(args.text)
