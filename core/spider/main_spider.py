
# encoding: utf-8
# time: 2020/3/23 16:11

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from pyquery import PyQuery as pq


import threading
import re

import config

import common.net as net
import common.log as log



# self.browser:浏览器，将浏览器设置为谷歌驱动，
# 这里需要下载谷歌对应的驱动,使用火狐浏览器安装驱动后webdriver.Firefox()


class MainSpider():

    savePath =None
    baseUrl = 'https://danbooru.donmai.us/posts?tags=azur_lane'
    browser = None

    wait = None

    _isRun = False

    useTag = True

    totalPage=1000

    def __init__(self):
        pass

    def open(self):
        # 解决加载超时出错
        try:
            self.browser.get(self.baseUrl)
            # 浏览器等待10秒
            self.wait = WebDriverWait(self.browser, 10)

            self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#content'))
            )

        # 超时出错时，重新执行search()程序
        except Exception as e:
            print(str(e))

            return 0

    # 获取商品信息

    def getImgs(self):

        try:

            self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#posts-container'))
            )

            # items = self.browser.find_elements_by_class_name(
            #     '#posts-container > article')

            items = self.browser.find_elements_by_xpath(
                '//article[@data-file-url]')

            for item in items:
                try:
                    if self.useTag:
                        urlTag = item.find_element_by_tag_name(
                            'a')
                        url = urlTag.get_attribute('href')
                        self.openNewTag(url)
                        self.wait.until(
                            EC.presence_of_element_located(
                                (By.CSS_SELECTOR, '#post-info-size'))
                        )
                        tag = self.browser.find_element_by_id('post-info-size')
                        downUrl = tag.find_element_by_tag_name(
                            'a').get_attribute('href')
                        net.downUrl(downUrl,self.savePath)
                        log.info(downUrl)
                        self.closeTab()

                    else:
                        downUrl = item.get_attribute('data-file-url')
                        net.downUrl(downUrl,self.savePath)
                        log.info(downUrl)
                except Exception as e:
                    print(str(e))

        except Exception as e:
            print(str(e))

    def nextPage(self):
        try:
            nextPage = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#paginator-next'))
            )

            nextPage.click()
        except Exception as e:
            print(str(e))

    def doSprider(self):
        if self.browser == None:
            self.browser = webdriver.Firefox()

        self.open()
        self.getImgs()
        total = self.totalPage
        for i in range(0, total):
            self.nextPage()
            self.getImgs()

    def start(self):
        if self._isRun:
            return
        self._isRun = True
        t = threading.Thread(target=self.doSprider)
        t.start()

    def stop(self):
        self._isRun = False

    def openNewTag(self, url):
        js = "window.open('"+url+"')"
        self.browser.execute_script(js)
        # self.wait = WebDriverWait(self.browser, 10)
        self.browser.switch_to.window(self.browser.window_handles[1])

    def closeTab(self):
        self.browser.close()
        # self.wait = WebDriverWait(self.browser, 10)
        self.browser.switch_to.window(self.browser.window_handles[0])
