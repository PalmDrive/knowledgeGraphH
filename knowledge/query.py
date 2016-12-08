# coding=utf8

import argparse
import neo4j_methods as neo4j
from model.word import has_unknown_word
from parse import GraphBuilder

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
        ans = self.query(text)
        if len(ans) > 0:
            return ', '.join(ans)
        else:
            return u'我不知道'

    def query(self, text):
        return self.query_srl(text)

    def query_srl(self, text):
        db = Db()
        ans = []

        gb = GraphBuilder()
        gb.parse_srl(text)
        results = gb.extract_srl()

        for A0, verb, A1 in results:
            if verb and not has_unknown_word(verb):
                from_entity_name = A0 if not has_unknown_word(A0) else None
                to_entity_name = A1 if not has_unknown_word(A1) else None

                print 'from ', from_entity_name, 'rel ', verb, 'to ', to_entity_name
                relations = db.find_relations(verb, from_entity_name=from_entity_name,
                                              to_entity_name=to_entity_name)

                for relation in relations:
                    if A0 and has_unknown_word(A0):
                        from_name = relation['from_name']
                        ans.append(from_name )
                    elif A1 and has_unknown_word(A1):
                        to_name = relation['to_name']
                        ans.append(to_name)

        return ans

    def query_dp(self, text):
        db = Db()
        ans = []
        gb = GraphBuilder()
        gb.parse_dp(text)
        results = gb.extract_srl()

        for subj, verb, direct_obj, indirect_obj in results:

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
