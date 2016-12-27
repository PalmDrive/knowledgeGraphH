# coding=utf8

class Media(object):

    def from_lc_object(self, lc_object):

        self.id = lc_object.id
        self.keywords = lc_object.get("keywords") if lc_object.get("keywords") != None else []
        self.source = lc_object.get("source")

        return self
