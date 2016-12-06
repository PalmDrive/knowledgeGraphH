# coding=utf8

import argparse
from ltp import Ltp
import json
import neo4j_methods as neo4j
from knowledge.model.word import Word

class Db(object):
    def find_from_entity(self, edge):
        return neo4j.find_from_entity(edge)
        # return 'from_entity <- ' + str(edge)

    def find_to_entity(self, edge):
        return neo4j.find_to_entity(edge)
        # return 'to_entity <- ' + str(edge)

    def find_relations(self, relation_name, from_entity_name=None, to_entity_name=None, **kwargs):
        return neo4j.find_edges(relation_name, from_entity_name, to_entity_name, **kwargs)
        # edge = {'relation' : 'relation_name ' + relation_name + str(kwargs.items()), 'IO':'abc'}
        # print edge
        # return [edge]



class Query(object):
    def lookup(self, text):
        api = Ltp()
        res = api.call(text, 'all')
        body = json.loads(res)
        ans = self.query(body)
        if len(ans) > 0:
            return ', '.join(ans)
        else:
            return u'我不知道'

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
                    entity = db.find_from_entity(relation)[0]
                    ans.append(entity['name'])
                elif direct_obj and direct_obj.is_unknown_word():
                    entity = db.find_to_entity(relation)[0]
                    ans.append(entity['name'])
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
