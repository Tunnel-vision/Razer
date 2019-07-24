# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from scrapy.http import HtmlResponse
from lxml import etree
import platform
import time, datetime


class InstagramMiddleware(object):
    def __init__(self, timeout=None):
        self.timeout = timeout
        self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_argument('--proxy-server=http://127.0.0.1:1087')
        # 在CentOS7环境下使用需加上下面参数
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--disable-gpu')
        # self.chrome_options.add_argument('--no-sandbox')
        if platform.platform().startswith('Windows'):
            self.executable_path = 'C:\Anaconda3\Scripts\chromedriver.exe'
        else:
            self.executable_path = '/usr/bin/chromedriver'
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options, executable_path=self.executable_path)
        self.wait = WebDriverWait(self.driver, self.timeout)

    def process_request(self, request, spider):
        try:
            self.driver.get(request.url)
            start_time = datetime.datetime.now()
            while True:
                try:
                    end_time = datetime.datetime.now()
                    seconds = (end_time - start_time).seconds
                    if seconds > (4 * 60):
                        break
                    html = etree.HTML(self.driver.page_source)
                    loadMore = self.driver.find_element_by_class_name('lnrre')
                    loadMore.click()
                    time.sleep(1)
                except:
                    break
            return HtmlResponse(request.url, status=200, body=self.driver.page_source, request=request,
                                encoding='utf-8')
        except TimeoutException:
            return HtmlResponse(request.url, status=500, request=request)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            timeout=crawler.settings.get('SELENIUM_TIMEOUT')
        )
