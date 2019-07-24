# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
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
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options, executable_path=self.executable_path)
        self.wait = WebDriverWait(self.browser, self.timeout)
        self.page_source = ''
        self.index = 1

    def process_request(self, request, spider):
        try:
            self.browser.get(self.homepage)
            keyword = request.meta.get('keyword', None)
            self.search = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="search"]')))
            self.btnsearch = self.wait.until(EC.presence_of_element_located((By.ID, 'search-icon-legacy')))
            self.search.clear()
            self.search.send_keys(keyword)
            self.btnsearch.click()
            self.filter = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[@id="filter-menu"]/div[@id="container"]/ytd-toggle-button-renderer')))
            self.filter.click()
            time.sleep(0.5)
            self.datefilter = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                              '//div[@id="collapse-content"]/ytd-search-filter-group-renderer[1]/ytd-search-filter-renderer[2]//div[@id="label"]')))
            self.datefilter.click()
            while True:
                scrollDistance = 'var h=document.documentElement.scrollTop=%d' % (self.index * 800)
                self.index += 1
                self.browser.execute_script(scrollDistance)
                time.sleep(0.5)
                if self.page_source != self.browser.page_source:
                    self.page_source = self.browser.page_source
                else:
                    break
        except:
            return HtmlResponse(url=request.url, status=500, request=request)

        return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                            status=200)

    def __del__(self):
        self.browser.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   homepage=crawler.settings.get('HOME_PAGE'))
