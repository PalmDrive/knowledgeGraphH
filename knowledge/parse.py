import argparse

import neo4j_methods as graph_db
from model.sentence import Sentence
from ltp import Ltp
from ltp import handle_request


class GraphBuilder(object):
    def __init__(self):
        self.ltp = Ltp()
        pass

    def parse(self, text):
        result = handle_request(self.ltp.call(text, "srl"))

        self.sentences = []

        for paragraphJson in result:
            for sentenceJson in paragraphJson:
                sentence = Sentence(sentenceJson)
                self.sentences.append(sentence)

    def parse_dp(self, text):
        self.parse(text)
        for sentence in self.sentences:
            sentence.init_parents()

    def parse_srl(self, text):
        self.parse(text)

    def extract_dp(self):
        # call neo4j
        subj = None
        verb = None
        direct_obj = None
        indirect_obj = None

        for sentence in self.sentences:
            for _, word in sentence.words_dict().items():
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

        yield subj, verb, direct_obj, indirect_obj

    def build_dp(self):

        subj, verb, direct_obj, indirect_obj = self.extract_dp()

        if subj:
            graph_db.create_entity({'name': subj.get_content()})

        if direct_obj:
            graph_db.create_entity({'name': direct_obj.get_content()})

        if indirect_obj:
            graph_db.create_entity({'name': indirect_obj.get_content()})

        if subj and direct_obj and verb:
            graph_db.create_edge(
                subj.get_content(),
                direct_obj.get_content(),
                {'name': verb.get_content()}
            )

            if indirect_obj:
                graph_db.set_edge(
                verb.get_content(), {'IO': indirect_obj.get_content()})

    def extract_srl(self):
        # call neo4j
        for sentence in self.sentences:
            for _, word in sentence.words_dict().items():
                if word.is_verb():
                    A0 = ""
                    A1 = ""
                    verb = word.get_content()
                    if word.get_arg():
                        for arg in word.get_arg():
                            print 'arg ' , arg
                            if 'A0' in arg.get('type'):
                                begin = arg.get('beg')
                                end = arg.get('end')
                                A0 = sentence.combined_words(begin, end)
                                print 'A0', A0

                            if 'A1' in arg.get('type'):
                                begin = arg.get('beg')
                                end = arg.get('end')
                                A1 = sentence.combined_words(begin, end)
                                print 'A1', A1

                        if len(A0) > 0 and len(A1) > 0:
                            yield A0, verb, A1

    def build_srl(self):
        results = self.extract_srl()
        for A0, verb, A1 in results:
            graph_db.create_entity({'name': A0})
            graph_db.create_entity({'name': A1})

            graph_db.create_edge(
                A0,
                A1,
                {'name': verb}
            )


if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    file = open('/Users/yonglin/playground/test1/input.txt', 'r')
    text = file.read()
    # parser = argparse.ArgumentParser()
    # parser.add_argument('text')
    # args = parser.parse_args()
    # text = args.text

    gb = GraphBuilder()
    gb.parse_srl(text)
    gb.build_srl()
