import argparse
from ltp import Ltp
from ltp import handle_request
import pprint


class GraphBuilder(object):
    def __init__(self):
        self.ltp = Ltp()
        pass

    def parse(self, text):
        self.result = handle_request(self.ltp.call(text, "all"))
        pp = pprint.PrettyPrinter(indent=2)





if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    parser = argparse.ArgumentParser()
    parser.add_argument('text')
    args = parser.parse_args()
    gb = GraphBuilder()
    gb.parse(args.text)
