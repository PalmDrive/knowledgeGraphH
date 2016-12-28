#coding:utf8

import math

from knowledge.config.config import load_config
from knowledge.data_manager.data_manager import DataManager

max_distance = 3

def recommend_for_media(media_id):
    data_manager = DataManager()
    initial_media_entities = data_manager.find_media_mappings_from_media(media_id)

    candidates = {}
    for initial_media_entity in initial_media_entities:

        for distance in range(0, max_distance):

            # 找到与初始节点距离为d的节点
            neighbors = data_manager.find_entity_neighbors(initial_media_entity.entity_id, distance)
            for neighbor in neighbors:

                # 找出每个节点所关联的文章
                entity_media_mappings = data_manager.find_media_mappings_from_entity(neighbor.id)
                for entity_media in entity_media_mappings:

                    # 并且加和相关系数，被作为参数的文章除外
                    if entity_media.media.id != media_id:

                        coefficient = relevance_coefficient(initial_media_entity.weight, distance, entity_media.weight)

                        if entity_media.media.id in candidates:
                            candidates[entity_media.media.id] = candidates[entity_media.media.id] + coefficient
                        else:
                            candidates[entity_media.media.id] = coefficient



def relevance_coefficient(initial_weight, distance, keyword_weight, edge_weight = 1):
    return initial_weight * keyword_weight * edge_weight * math.exp(distance)

def main():

    load_config()
    recommend_for_media('5850c91b128fe1006b4d4d12')

if __name__ == "__main__":
    main()
