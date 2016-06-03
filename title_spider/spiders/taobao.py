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

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='./log/taobao.log',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)

class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    url = UrlGenerator3("https://www.taobao.com", "./entity/test_entity.txt")

    def start_requests(self):
        for title, url in self.url:
            yield WebdriverRequest(url, callback=self.parse_first, meta={'title': title})

    def parse_first(self, response):
        query = response.meta['title'].decode('utf-8')
        print query
        try:
            driver = response.webdriver
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.search-combobox-input"))
            )

            # element = driver.find_element_by_css_selector("input#mq.s-combobox-input")
            element.send_keys(query)
            element.submit()

            # wait for refresh
            time.sleep(0.5)

            for i in range(5):

                product = response.webdriver.find_elements_by_css_selector("div.title a")
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
                    driver.find_element_by_css_selector("div.mainsrp-pager a.J_Ajax").click()

        except Exception, e:
            self.logger.error(e)



