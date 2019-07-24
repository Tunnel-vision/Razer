# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from scrapy.http import HtmlResponse
from selenium.webdriver.common.action_chains import ActionChains
import platform
from lxml import etree


class SeleniumMiddleware(object):
    def __init__(self, timeout):
        self.timeout = timeout
        self.keyword = ''
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
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options, executable_path=self.executable_path)
        self.wait = WebDriverWait(self.browser, self.timeout)
        self.browser.get('http://forum.notebookreview.com/razer/')

    def process_request(self, request, spider):
        if self.keyword != request.meta.get('keyword', None):
            self.keyword = request.meta.get('keyword', None)
            self.browser.get(request.url)
            search = self.wait.until(EC.presence_of_element_located((By.ID, 'QuickSearchQuery')))
            ActionChains(self.browser).move_to_element(search).click()
            form = self.wait.until(EC.presence_of_element_located((By.ID, 'QuickSearch')))
            search.send_keys(self.keyword)
            searchdate = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchBar_date"]')))
            searchdate.click()
            calcurrent = self.wait.until(EC.presence_of_element_located((By.ID, 'calcurrent')))
            calcurrent.click()
            button = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="QuickSearch"]/form/div[2]/dl/dd/input')))
            button.click()
            result = ''
            result += self.browser.page_source
            while True:
                try:
                    pagenext = self.browser.find_element_by_xpath(
                        '//div[@class="PageNav"]//a[contains(text(), "Next")]')
                    pagenext.click()
                    result += '--*--*--'
                    result += self.browser.page_source
                except:
                    break

            return HtmlResponse(url=request.url, body=result, request=request, encoding='utf-8', status=200)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'))
