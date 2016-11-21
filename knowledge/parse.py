import argparse
from ltp import Ltp
from ltp import handle_request
from query import Word
import neo4j_methods as neo4j

class GraphBuilder(object):
    def __init__(self):
        self.ltp = Ltp()
        pass

    def parse(self, text):
        result = handle_request(self.ltp.call(text, "all"))

        self.words = {}
        for paragraph in result:
            for sentence in paragraph:
                for word in sentence:
                    w = Word(word)
                    self.words[w.id()] = w

        for id, w in self.words.items():
            parent = self.words.get(w.parent_id())
            w.set_parent(parent)

    def build(self):
        # call neo4j
        subj = None
        verb = None
        direct_obj = None
        indirect_obj = None

        for _, word in self.words.items():
            if word.is_subject():
                subj = word
                continue

            if word.is_direct_object():
                direct_obj = word
                continue

            if word.is_indirect_object():
               indirect_obj = word

            if word.is_relation():
                verb = word

        if subj:
            neo4j.create_entity({'name': subj.get_content()})

        if direct_obj:
            neo4j.create_entity({'name': direct_obj.get_content()})

        if indirect_obj:
            neo4j.create_entity({'name': indirect_obj.get_content()})

        if subj and direct_obj and verb:

            neo4j.create_edge(
                subj.get_content(),
                direct_obj.get_content(),
                {'name': verb.get_content()}
            )

            if indirect_obj:
                neo4j.set_edge(
                verb.get_content(), {'IO': indirect_obj.get_content()})


if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    parser = argparse.ArgumentParser()
    parser.add_argument('text')
    args = parser.parse_args()
    gb = GraphBuilder()
    gb.parse(args.text)
    gb.build()
