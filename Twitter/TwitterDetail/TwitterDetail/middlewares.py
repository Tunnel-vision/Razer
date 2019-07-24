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
import platform


class SeleniumMiddleware(object):
    def __init__(self, timeout=None):
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
        self.browser.get('https://twitter.com/razer')
        account = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                  '#signin-dropdown > div.signin-dialog-body > form > div.LoginForm-input.LoginForm-username > input')))
        password = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                   '#signin-dropdown > div.signin-dialog-body > form > div.LoginForm-input.LoginForm-password > input')))
        login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                '#signin-dropdown > div.signin-dialog-body > form > input.EdgeButton.EdgeButton--primary.EdgeButton--medium.submit.js-submit')))
        account.clear()
        account.send_keys('qinexpire@gmail.com')
        time.sleep(1)
        password.clear()
        password.send_keys('liusha4439')
        time.sleep(0.5)
        login.click()

    def process_request(self, request, spider):
        scrollDistance = request.meta.get('scrollDistance', None)
        if scrollDistance:
            self.browser.execute_script(scrollDistance)
            time.sleep(1)
        else:
            self.browser.get(request.url)

        try:
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'))
