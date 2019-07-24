# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from scrapy.http import HtmlResponse
import platform


class SeleniumMiddleware(object):
    def __init__(self, timeout):
        self.timeout = timeout
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
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options, executable_path=self.executable_path)
        self.wait = WebDriverWait(self.browser, self.timeout)
        self.page_source = ''
        self.index = 1

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        self.browser.get(request.url)
        while True:
            scrollDistance = 'var h=document.documentElement.scrollTop=%d' % (self.index * 800)
            self.index += 1
            self.browser.execute_script(scrollDistance)
            time.sleep(1)
            if self.page_source != self.browser.page_source:
                self.page_source = self.browser.page_source
            else:
                break

        self.index = 1
        return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                            status=200)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'))
