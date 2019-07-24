# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse
import platform
import time


class SeleniumMiddleware(object):
    def __init__(self, timeout=None, homepage=None):
        self.timeout = timeout
        self.homepage = homepage
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
        self.driver.get(self.homepage)
        formele = self.wait.until(EC.presence_of_element_located((By.ID, 'login_form')))
        account = self.wait.until(EC.presence_of_element_located((By.ID, 'email')))
        psd = self.wait.until(EC.presence_of_element_located((By.ID, 'pass')))
        loginbtn = self.wait.until(EC.presence_of_element_located((By.ID, 'loginbutton')))
        account.clear()
        account.send_keys('13373649193')
        time.sleep(0.5)
        psd.clear()
        time.sleep(1)
        psd.send_keys('liusha4439')
        loginbtn.click()
        self.driver.get(self.homepage)
        self.page_source = ''
        self.num = 1

    def process_request(self, request, spider):
        scrollDistance = request.meta.get('scrollDistance')
        if scrollDistance:
            if scrollDistance == 'var h=document.documentElement.scrollTop=0':
                self.driver.get(request.url)
            self.driver.execute_script(scrollDistance)
        # 循环判断并模拟点击View More以加载并显示所隐藏的评论
        while True:
            try:
                if self.page_source != self.driver.page_source:
                    self.page_source = self.driver.page_source
                else:
                    break

                btnMore = self.driver.find_element_by_class_name('UFIPagerLink')
                btnMore.click()
                time.sleep(1)
            except:
                break

        return HtmlResponse(request.url, status=200, body=self.driver.page_source, request=request, encoding='utf-8')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
            homepage=crawler.settings.get('HOMEPAGE_URL')
        )
