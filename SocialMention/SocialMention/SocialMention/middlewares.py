# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from selenium.webdriver.common.action_chains import ActionChains
import platform
from selenium.webdriver.support.ui import Select
import time


class SeleniumMiddleware(object):
    def __init__(self, timeout):
        self.timeout = timeout
        self.keyword = ''
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

    def process_request(self, request, spider):
        if self.keyword != request.meta.get('keyword', None):
            self.keyword = request.meta.get('keyword', None)
            self.browser.get(request.url)
            search = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#search > table > tbody > tr > td:nth-child(1) > input[type="text"]')))
            search.send_keys(self.keyword)
            dropdown = self.browser.find_element_by_id('target')
            dropdown.click()
            option = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#target > dd > ul > li:nth-child(3)')))
            option.click()
            btn = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#search > table > tbody > tr > td:nth-child(3) > input[type="submit"]')))
            btn.click()
            sortby = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#sort_show > div.show_results > form > select:nth-child(5)')))
            sortby.click()
            ssortby = Select(sortby)
            ssortby.select_by_value('date')
            time.sleep(1)
            date = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#sort_show > div.show_results > form > select:nth-child(6)')))
            date.click()
            sdate = Select(date)
            sdate.select_by_value('24h')
            time.sleep(3)

            result = ''
            result += self.browser.page_source
            while True:
                try:
                    time.sleep(1)
                    pagenext = self.browser.find_element_by_xpath(
                        '//div[@class="pagination"]//a/div[contains(text(), "Next »")]')
                    pagenext.click()
                    result += '--*--*--'
                    result += self.browser.page_source
                except:
                    break

            return HtmlResponse(url=request.url, body=result, request=request, encoding='utf-8', status=200)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'))
