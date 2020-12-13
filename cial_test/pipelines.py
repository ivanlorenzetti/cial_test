# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import logging
import json
from datetime import datetime, timezone, timedelta
import pymongo

from io import StringIO
import sys


class CialTestPipeline(object):

    def __init__(self):



        connection = pymongo.MongoClient('localhost', 27017)

        db = connection['cial_test']
        self.collection = db['cial']
        print(self.collection)

    def open_spider(self, spider):
        start_time = datetime.now()
        file_log = 'results'+str(start_time).replace('.', '').replace(':', '').replace(' ', '')
        file_log += '.log'
        self.file = open(file_log, 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        #resultados em arquivos txt
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)

        #resultados importados para MONGO
        print('insert mongo')
        #self.collection.insert(dict(item))

        return item

