#coding:utf8

from knowledge.config.config import load_config
from knowledge.data_manager.data_manager import DataManager


def map_media_to_entities():
    data_manager = DataManager()
    articles = data_manager.get_media()

    for article in articles:
        # 提取文章的关键词
        keywords = article.keywords
        print ','.join(keywords)

        for keyword in keywords:
            # 用关键词找到对应的节点ID
            entities = data_manager.find_entities_from_mention(keyword)

            # 建表（节点文章关系表，简称关系表） 文章的ID - 节点ID - 关键词 - 关键词权重 - source
            for entity in entities:
                data_manager.add_media_entity_mapping(article.id, entity.id, keyword, 1, article.source)

    data_manager.save()

def main():

    load_config()
    map_media_to_entities()

if __name__ == "__main__":
    main()
