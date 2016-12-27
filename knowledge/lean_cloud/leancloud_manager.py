#coding:utf8

import logging

import leancloud

from knowledge.config.config import CONFIG

CLASS_NAME_MEDIA = "Media"
CLASS_NAME_MEDIA_ENTITY = "MediaEntity"

class LeanCloudManager(object):

    def __init__(self):
        APP_ID = CONFIG.LEANCLOUD_APP_ID
        APP_KEY = CONFIG.LEANCLOUD_APP_KEY
        MASTER_KEY = CONFIG.LEANCLOUD_MASTER_KEY
        leancloud.init(APP_ID, APP_KEY, MASTER_KEY)
        self.media_entities_to_save = []

    def batch_fetch(self, query, limit = 0):

        # limit is used for debugging, it can prevent fetching too many media when testing

        offset = 0
        batch_size = 1000
        if limit > 0 and batch_size > limit:
            batch_size = limit
        result = []
        query.limit(batch_size)

        batch_result = query.find()
        result.extend(batch_result)

        while len(batch_result) == batch_size:
            offset += batch_size
            if limit > 0 and offset >= limit:
                break
            query.skip(offset)
            batch_result = query.find()
            result.extend(batch_result)

        return result

    def batch_save(self, objects):

        offset = 0
        batch_size = 1000

        count =  len(objects)
        while offset < count:
            leancloud.Object.save_all(objects[offset:offset+batch_size])
            offset += batch_size

    def batch_fetch_media_with_source(self, source):

        Media = leancloud.Object.extend(CLASS_NAME_MEDIA)
        query = Media.query.equal_to("source", source)
        limit = 0
        if CONFIG.ENV == 'development':
            limit = 4

        return self.batch_fetch(query, limit)

    def add_media_entity_mapping(self, media_id, entity_id, keyword, weight, source):

        Media = leancloud.Object.extend(CLASS_NAME_MEDIA)
        MediaEntity = leancloud.Object.extend(CLASS_NAME_MEDIA_ENTITY)
        media_entity = MediaEntity()
        media_entity.set('entityId', entity_id)
        media_entity.set('media', Media.create_without_data(media_id))
        media_entity.set('keyword', keyword)
        media_entity.set('weight', weight)
        media_entity.set('source', source)
        self.media_entities_to_save.append(media_entity)

    def save_objects(self):

        if len(self.media_entities_to_save):
            try:
                self.batch_save(self.media_entities_to_save)
                self.media_entities_to_save = []
            except leancloud.LeanCloudError as e:
                logging.info('error %s' % str(e))






