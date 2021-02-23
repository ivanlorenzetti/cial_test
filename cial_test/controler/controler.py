
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider


from cial_test.spiders.cialtest import CialTestSpider


import re
import logging
import os
from datetime import datetime, timezone, timedelta
import sys

from twisted.internet import reactor, defer

class Controler:

    def file_log(self):
        start_time = datetime.now()
        file_log = str(start_time).replace('.', '').replace(':', '').replace(' ','')
        file_log += '.log'
        return file_log

    def __init__(self, starting_urls):

        file_log = self.file_log()
        logging.basicConfig(filename='./log/'+file_log, level=logging.INFO)
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


        self.settings = Settings()
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'cial_test.settings'
        settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
        self.settings.setmodule(settings_module_path, priority='project')


        self.starting_urls = starting_urls

        logging.info(".....Log.....")

    def scrape(self):

        runner = CrawlerRunner(self.settings)
        configure_logging()

        @defer.inlineCallbacks
        def crawl(starting_urls):
            for starting_url in starting_urls:
                try:
                    yield runner.crawl(CialTestSpider, start_urls=[starting_url])

                except Exception as e:
                    logging.warning('Error %s' % str(e))
            reactor.stop()

        crawl(self.starting_urls)
        reactor.run()
