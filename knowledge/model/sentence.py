# coding=utf8
from word import Word

class Sentence(object):
    def __init__(self, sentenceJson = None):
        self.words = {}
        self.parse_from_json(sentenceJson)

    def set_words(self, words):
        self.words = words

    def parse_from_json(self, sentenceJson):
        for word in sentenceJson:
            w = Word(word)
            self.words[w.get_id()] = w

    def init_parents(self):
        for id, w in self.words.items():
            parent = self.words.get(w.parent_id())
            w.set_parent(parent)

    def words_array(self, fromIndex=None, toIndex=None):
        words = []
        for index in xrange(fromIndex, toIndex+1):
            words.append(self.words[index])
        return words

    def words_dict(self):
        return self.words

    def combined_words(self, fromIndex, toIndex):
        words = self.words_array(fromIndex, toIndex)
        return ''.join([w.get_content() for w in words])
