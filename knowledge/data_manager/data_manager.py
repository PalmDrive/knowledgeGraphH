#coding:utf8

from knowledge.lean_cloud.leancloud_manager import LeanCloudManager
from knowledge.model.media import Media
from knowledge.model.entity import Entity
from knowledge.neo4j_methods import Neo4jManager

class DataManager(object):
    def __init__(self):
        self.tasks = []
        self.sqlDB = LeanCloudManager()
        self.graphDB = Neo4jManager()

    def get_media(self, source = None):
        total_data = []
        if not source:
            source = "Flipboard"

        result = self.sqlDB.batch_fetch_media_with_source(source)
        print "result :%d" % len(result)

        media_array = [Media().from_lc_object(obj) for obj in result]
        total_data.extend(media_array)

        return total_data

    def find_entities_from_mention(self, mention):
        results = self.graphDB.find_nodes_with_any_values_in_properties(label_zh=mention,
                                                                        label_en=mention,
                                                                        aliases_zh=mention,
                                                                        aliases_en=mention)
        # reconcile mention to node in graph db
        entities = [Entity().from_graph_node(node) for node in results]

        return entities

    def add_media_entity_mapping(self, media_id, entity_id, keyword, weight, source):
        #节点ID - 文章的ID - 关键词 - 关键词权重 - source
        self.sqlDB.add_media_entity_mapping(media_id, entity_id, keyword, weight, source)


    def save(self):
        self.sqlDB.save_objects()