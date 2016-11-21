import argparse
from ltp import Ltp
from ltp import handle_request
from query import Word


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
        pass


if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    parser = argparse.ArgumentParser()
    parser.add_argument('text')
    args = parser.parse_args()
    gb = GraphBuilder()
    gb.parse(args.text)
