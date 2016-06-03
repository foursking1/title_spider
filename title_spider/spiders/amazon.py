#-*- coding: utf-8 -*-
import scrapy
from utils.common import UrlGenerator, UrlGenerator3, wait_for_page_load
from scrapy_webdriver.http import WebdriverRequest
from items import TitleSpiderItem
import logging
from scrapy.utils.log import configure_logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='./log/amazon.log',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    # url2 = UrlGenerator2("https://www.amazon.cn/s/ref=nb_sb_noss?__mk_zh_CN=亚马逊网站&field-keywords=%s", "./entity/entity_inc.txt")
    #
    # def start_requests(self):
    #     for title, url in self.url2:
    #         yield WebdriverRequest(url, callback=self.parse_first)

    url = UrlGenerator3("https://www.amazon.cn", "./entity/benchmark.txt")

    def start_requests(self):
        try:
            for title, url in self.url:
                yield WebdriverRequest(url, callback=self.parse_first, meta={'title': title})

        except Exception, e:
            self.logger.error(e)


    def parse_first(self, response):

        query = response.meta['title'].decode('utf-8')
        print query
        try:
            driver = response.webdriver
            driver.set_window_size(1920, 1080)

            # element = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, "input#twotabsearchtextbox"))
            # )

            #element = driver.find_element_by_css_selector("input#twotabsearchtextbox")
            #element.send_keys(query)
            #element.submit()

            # send_keys方法在PhantomJS下失效，只能这样了
            time.sleep(0.5)
            js = "document.getElementById('twotabsearchtextbox').value='%s'" % query
            driver.execute_script(js)
            time.sleep(0.5)
            driver.find_element_by_css_selector("input.nav-input").click()


            for i in range(5):

                # 非常重要，等待点击之后的刷新
                time.sleep(1)
                js = "window.scrollTo(100,10000)"
                driver.execute_script(js)


                # 等待一下dom才加载完毕， 所以这个步骤也许会失败吧
                # product = WebDriverWait(driver, 10).until(
                #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.s-access-detail-page"))
                # )

                product = response.webdriver.find_elements_by_css_selector("a.s-access-detail-page")
                #print product

                for e in product:
                    title = e.text.strip()
                    self.logger.info("query=%s, title=%s" % (query.encode('utf-8'), title.encode('utf-8')))
                    item = TitleSpiderItem()
                    item['title'] = title.encode('utf-8').replace(',', '')
                    item['query'] = query.encode('utf-8').replace(',', '')
                    yield item

                # 点击下一页
                self.logger.info("click")

                #make sure element is visible
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "span#pagnNextString"))
                )

                #with wait_for_page_load(driver):
                print driver.find_element_by_css_selector("span#pagnNextString")
                # 亚马逊在点击下一页是，由于是用ajax加载，所以wait函数的判断失效
                js = "document.getElementById('pagnNextLink').click()"
                driver.execute_script(js)
                #driver.find_element_by_css_selector("span#pagnNextString").click()


        except Exception, e:
            self.logger.error(e)