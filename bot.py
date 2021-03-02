import sys
import scrapy
import logging

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

import cial_test.settings as custom_settings
from cial_test.spiders.cialtest import CialTestSpider

if __name__ == "__main__":

	url_list = []
	for line in sys.stdin:
		line_stripped = line.strip()
		url_list.append(line_stripped)

	
	crawler_settings = Settings()
	crawler_settings.setmodule(custom_settings)

	process = CrawlerProcess(settings=crawler_settings)
	process.crawl(CialTestSpider, url_lst=url_list)
	process.start()
