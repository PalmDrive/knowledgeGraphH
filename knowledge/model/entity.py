# coding=utf8

class Entity(object):
    def from_graph_node(self, node):
        self.id = node['id']
        self.labels_zh = node['labels_zh']
        self.labels_en = node['labels_en']
        self.description_en = node['description_en']
        self.description_zh = node['description_zh']
        return self

    def from_id(self, entity_id):
        self.id = entity_id