# coding=utf8

UNKNOWN_WORDS = [u'谁',u'什么',u'怎么',u'怎么样',u'为什么',u'哪个']

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
        return self.word['cont'] in UNKNOWN_WORDS

    def get_content(self):
        return self.word['cont']

    def get_id(self):
        return self.word['id']

    def parent_id(self):
        return self.word['parent']

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def get_arg(self):
        return self.word.get('arg')

    def is_verb(self):
        return self.word['pos'] == 'v'

def has_unknown_word(text):
    for w in UNKNOWN_WORDS:
        if w in text:
            return True
    return False