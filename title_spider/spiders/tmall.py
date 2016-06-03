#-*- coding: utf-8 -*-
import scrapy
from utils.common import UrlGenerator3, wait_for_page_load
from items import TitleSpiderItem
import logging
from scrapy.utils.log import configure_logging
from scrapy_webdriver.http import WebdriverRequest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback

import ipdb
#from scrapy.http.request import Request

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='./log/tmall.log',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)

class TmallSpider(scrapy.Spider):
    name = 'tmall'
    url = UrlGenerator3("https://www.tmall.com", "./entity/benchmark.txt")

    def start_requests(self):
        try:
            for title, url in self.url:
                yield WebdriverRequest(url, callback=self.parse_first, meta={'title': title})

        except Exception, e:
            self.logger.error(e)
            traceback.print_exc()


    def parse_first(self, response):


        # 编码问题trick
        query = response.meta['title'].decode('utf-8')
        print query
        try:
            driver = response.webdriver
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input#mq.s-combobox-input"))
            )

            #element = driver.find_element_by_css_selector("input#mq.s-combobox-input")
            element.send_keys(query)
            element.submit()

            #wait for refresh
            time.sleep(0.5)

            for i in range(5):
                #js = "window.scrollTo(100,10000)"
                #driver.execute_script(js)
                # 等待一下dom才加载完毕， 所以这个步骤也许会失败吧
                product = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p.productTitle a"))
                )
                #product = response.webdriver.find_elements_by_css_selector("p.productTitle a")

                for e in product:

                    title = e.text.strip()
                    self.logger.info("query=%s, title=%s" % (query.encode('utf-8'), title.encode('utf-8')))
                    item = TitleSpiderItem()
                    item['title'] = title.encode('utf-8').replace(',', '')
                    item['query'] = query.encode('utf-8').replace(',', '')
                    yield item

                # 点击下一页
                self.logger.info("click")
                with wait_for_page_load(driver):
                    driver.find_element_by_css_selector("a.ui-page-next").click()


        except Exception, e:
            self.logger.error(e)
            traceback.print_exc()



