# coding=utf8

from knowledge.model.media import Media

class MediaEntity(object):

    def from_lc_object(self, lc_object):

        self.id = lc_object.id
        self.entity_id = lc_object.get("entityId")
        self.source = lc_object.get("source")
        self.media = Media().from_lc_object(lc_object.get("media"))
        self.weight = lc_object.get("weight")
        self.keyword = lc_object.get("keyword")

        return self
