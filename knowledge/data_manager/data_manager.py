#coding:utf8

from knowledge.lean_cloud.leancloud_manager import LeanCloudManager
from knowledge.model.media import Media
from knowledge.model.entity import Entity
from knowledge.model.media_entity import MediaEntity
from knowledge.neo4j_manager import Neo4jManager

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
        #文章的ID - 节点ID - 关键词 - 关键词权重 - source
        self.sqlDB.add_media_entity_mapping(media_id, entity_id, keyword, weight, source)

    def save(self):
        self.sqlDB.save_objects()

    # 通过Media的ID查询MediaEntity
    def find_media_mappings_from_media(self, media_id):
        media_entities = self.sqlDB.fetch_media_entities_from_media(media_id)
        return [MediaEntity().from_lc_object(obj) for obj in media_entities]

    def find_entity_neighbors(self, entity_id, max_distance):
        neighbors = self.graphDB.find_neighbor_nodes(entity_id, max_distance)
        return [(Entity().from_graph_node(n), d) for (n, d) in neighbors]

    def find_media_mappings_from_entity(self, entity_id):
        media_entities = self.sqlDB.fetch_media_entities_from_entity(entity_id)
        return [MediaEntity().from_lc_object(obj) for obj in media_entities]