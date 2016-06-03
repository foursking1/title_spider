#-*- coding: utf-8 -*-
import scrapy
from items import TitleSpiderItem
import logging
from scrapy.utils.log import configure_logging
from scrapy.http.request import Request
import urllib

import time

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='./log/kdd.log',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)

class KddSpider(scrapy.Spider):
    name = 'kdd'
    start_urls = ['http://www.kdd.org/kdd2016/program/accepted-papers']

    def parse(self, response):
        links = response.selector.css("table.table a::attr(href)").extract()
        for index, link in enumerate(links):
            # pass
            # if index == 5:
            #     break
            time.sleep(1)
            yield Request(link, callback=self.down_load)
        #return Request()

    def down_load(self, response):
        filename = response.url.split('/')[-1] or response.url
        link = response.selector.css('section.bs-docs-section div a::attr(href)').extract()[2]
        print filename, link
        #path = "./pdf1/" + filename + '.pdf'
        #urllib.urlretrieve(link, filename=path)



