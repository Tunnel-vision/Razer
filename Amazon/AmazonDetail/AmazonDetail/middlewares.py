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
import platform
import random
import time


class UserAgentMiddleware(object):
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
            'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11']

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)


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

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        next = request.meta.get('NEXT', None)
        self.browser.get(request.url)
        try:
            if next is None:
                reviews = self.wait.until(EC.presence_of_element_located((By.ID, 'acrCustomerReviewLink')))
                reviews.click()
                detail_reviews = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#reviews-medley-footer > div.a-row.a-spacing-large > a')))
                detail_reviews.click()
                time.sleep(1.5)
        except:
            pass

        return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                            status=200)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'))
