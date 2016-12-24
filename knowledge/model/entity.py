# coding=utf8

class Entity(object):
    def from_graph_node(self, node):
        self.id = node['id']
        self.label = node['name']
        return self
