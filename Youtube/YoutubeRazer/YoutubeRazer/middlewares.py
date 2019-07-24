# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from scrapy.http import HtmlResponse
import platform


class SeleniumMiddleware(object):
    def __init__(self, timeout, homepage):
        self.timeout = timeout
        self.homepage = homepage
        self.chrome_options = webdriver.ChromeOptions()
        # 在CentOS7环境下使用需加上下面参数
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--disable-gpu')
        # self.chrome_options.add_argument('--no-sandbox')
        # self.chrome_options.add_argument('--proxy-server=http://127.0.0.1:1087')
        if platform.platform().startswith('Windows'):
            self.executable_path = 'C:\Anaconda3\Scripts\chromedriver.exe'
        else:
            self.executable_path = '/usr/bin/chromedriver'
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options, executable_path=self.executable_path)
        self.driver.get(self.homepage)

    def process_request(self, request, spider):
        try:
            scrollDistance = request.meta.get('scrollDistance')
            if scrollDistance:
                self.driver.execute_script(scrollDistance)
            return HtmlResponse(request.url, status=200, body=self.driver.page_source, request=request,
                                encoding='utf-8')
        except TimeoutException:
            return HtmlResponse(request.url, status=500, request=request, encoding='utf-8')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
            homepage=crawler.settings.get('HOMEPAGE_URL')
        )
