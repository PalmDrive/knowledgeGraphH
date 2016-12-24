#coding:utf8
import logging

from knowledge.leancloud.leancloud_manager import LeanCloudManager
from knowledge.model.media import Media
from knowledge.model.entity import Entity

import knowledge.neo4j_methods as graph

class DataManager(object):
    def __init__(self):
        self.tasks = []
        self.sqlDB = LeanCloudManager()


    def get_media(self, source = None):
        total_data = []
        if not source:
            source = "Flipboard"

        result = self.sqlDB.batch_fetch_media_with_source(source)
        media_array = [Media().from_lc_object(obj) for obj in result]
        total_data.extend(media_array)

        logging.info("fetched :%d" % len(total_data))
        return total_data

    def find_nodes_from_mention(self, mention):
        nodes = []
        # TODO: reconcile mention to node in graph db
        return nodes

    def add_media_entity_mapping(self, media_id, entity_id, keyword, weight, source):
        #节点ID - 文章的ID - 关键词 - 关键词权重 - source
        self.sqlDB.add_media_entity_mapping(media_id, entity_id, keyword, weight, source)


    def save(self):
        self.sqlDB.save_objects()