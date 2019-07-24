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
    def __init__(self, timeout):
        self.timeout = timeout
        self.page_source = ''
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
        self.browser.get(
            'https://www.microsoft.com/en-us/p/razer-synapse-for-xbox/9p3xv1vq92qc?activetab=pivot:overviewtab')
        cancel = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#email-newsletter-dialog > div.sfw-dialog > div.c-glyph.glyph-cancel')))
        cancel.click()
        signin = self.wait.until(EC.presence_of_element_located((By.ID, 'meControl')))
        signin.click()
        time.sleep(3)
        account = self.wait.until(EC.presence_of_element_located((By.ID, 'i0116')))
        account.send_keys('qinexpire@outlook.com')
        time.sleep(1)
        next = self.wait.until(EC.presence_of_element_located((By.ID, 'idSIButton9')))
        next.click()
        time.sleep(3)
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'i0118')))
        password.send_keys('liusha4439')
        time.sleep(1)
        login = self.wait.until(EC.presence_of_element_located((By.ID, 'idSIButton9')))
        login.click()
        time.sleep(3)
        reviews = self.wait.until(EC.presence_of_element_located((By.ID, 'pivot-tab-ReviewsTab')))
        reviews.click()

    def process_request(self, request, spider):
        result = ''
        result += self.browser.page_source
        while True:
            try:
                next = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                       '//div[@id="ReviewsList"]//button/span[contains(text(), "Next")]')))
                next.click()
                time.sleep(1)
                result += '--*--*--'
                result += self.browser.page_source
            except:
                break

        return HtmlResponse(url=request.url, body=result, request=request,
                            encoding='utf-8', status=200)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'))
