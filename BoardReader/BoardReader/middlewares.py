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
from selenium.webdriver.support.ui import Select
import time


class SeleniumMiddleware(object):
    def __init__(self, timeout):
        self.timeout = timeout
        self.keyword = ''
        self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_argument('--proxy-server=http://127.0.0.1:1087')
        # 在CentOS7环境下使用需加上下面参数
        #self.chrome_options.add_argument('--headless')
        #self.chrome_options.add_argument('--disable-gpu')
        #self.chrome_options.add_argument('--no-sandbox')
        if platform.platform().startswith('Windows'):
            self.executable_path = 'C:\Anaconda3\Scripts\chromedriver.exe'
        else:
            self.executable_path = '/usr/bin/chromedriver'
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options, executable_path=self.executable_path)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        # if语句用来爬取一级URL
        keyword = request.meta.get('keyword', None)
        if keyword is not None:
            if self.keyword != keyword:
                self.keyword = keyword
                self.browser.get(request.url)
                input = self.wait.until(EC.presence_of_element_located((By.ID, 'title-query')))
                input.send_keys(keyword)
                submit = self.wait.until(EC.presence_of_element_located((By.ID, 'title-submit')))
                submit.click()
                setting = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                          '#form-holder > form > div.searchFormBlock > div.mdl-grid.no-left-right-padding.search-input-holder > div > div > button.mdl-button.mdl-js-button.mdl-button--raised.titleButton.advancedButton')))
                setting.click()

                time.sleep(2)
                sdate = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="form-holder"]/form/div[2]/div/div[2]/select')))
                sdate.click()
                s = Select(sdate)
                s.select_by_value('1')
                time.sleep(1)
                sortby = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="form-holder"]/form/div[2]/div/div[5]/select')))
                sortby.click()
                ss = Select(sortby)
                ss.select_by_value('time_desc')
                time.sleep(3)

                result = ''
                result += self.browser.page_source
                while True:
                    try:
                        pagenext = self.browser.find_element_by_xpath(
                            '//div[@id="form-holder"]//a[contains(text(), "Next »")]')
                        pagenext.click()
                        time.sleep(3)
                        result += '--*--*--'
                        result += self.browser.page_source
                    except:
                        break
                return HtmlResponse(url=request.url, body=result, request=request, encoding='utf-8', status=200)

        # 以下操作用来爬取二级详情
        issuedescription = request.meta.get('issuedescription')
        url = request.meta.get('url')
        source = request.meta.get('source')
        forum = request.meta.get('forum')
        source_url = request.meta.get('source_url')
        if 'http://forum.notebookreview.com' in request.url:
            if issuedescription:
                self.browser.get(request.url)
                time.sleep(3)
                return HtmlResponse(url=request.url, body=self.browser.page_source,
                                    headers={'issuedescription': issuedescription,
                                             'source': source,
                                             'forum': forum,
                                             'source_url': source_url}, encoding='utf-8', status=200)

        return HtmlResponse(url=request.url, status=500, encoding='utf-8')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'))
