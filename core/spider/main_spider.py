
# encoding: utf-8
# time: 2020/3/23 16:11

from tkinter.constants import FALSE
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import subprocess 

from time import sleep
from pyquery import PyQuery as pq

from datetime  import datetime


import threading
import re

import config

import common.net as net
import common.log as log

from common.db import dbCon

# self.browser:浏览器，将浏览器设置为谷歌驱动，
# 这里需要下载谷歌对应的驱动,使用火狐浏览器安装驱动后webdriver.Firefox()


class MainSpider():

    savePath = None
    baseUrl = 'https://danbooru.donmai.us/posts?tags=azur_lane'
    browser = None

    wait = None

    _isRun = False

    useTag = False

    needDown = False

    openBs = False
    totalPage = 1000

    dataTag="azur_lane"

    def __init__(self):
        pass

    def open(self):
        # 解决加载超时出错
        print("open")
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
            print("open："+str(e))

            return 0

    # 获取商品信息

    def getImgs(self):
        print("getImgs")
        try:

            self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.posts-container'))
            )
   
            items = self.browser.find_elements_by_class_name(
                'post-preview-link')

            # items = self.browser.find_elements_by_xpath(
            #     '//article[@data-file-url]')
            # items = self.browser.find_elements_by_xpath(
            #     '//article[@data-score]')
            for item in items:

                # if self.useTag:
                    # urlTag = item.find_element_by_tag_name(
                    #     'a')
                    # url = urlTag.get_attribute('href')
                    url = item.get_attribute('href')
                    self.openNewTag(url)
                    self.wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, '#post-info-size'))
                    )
                    tag = self.browser.find_element_by_id('post-info-size')
                    downUrl = tag.find_element_by_tag_name(
                        'a').get_attribute('href')
                    if self.needDown:
                       while net.download_from_url(downUrl, self.savePath) !=True:
                            print("TRY  :"+downUrl)

                    log.history(downUrl)
                    dbCon.insertData(downUrl,self.dataTag)
                    print(downUrl)
                    self.closeTab()
                    

                # else:
                #     downUrl = item.get_attribute('data-file-url')
                #     # downUrl = item.get_attribute('data-large-file-url')
                #     if self.needDown:
                #         net.download_from_url(downUrl, self.savePath)
                #     log.history(downUrl)
                #     dbCon.insertData(downUrl,self.dataTag)
                #     print(downUrl)

            # if not self.useTag:
            sleep(20)
            return True
        except Exception as e:
            if( self.browser.find_element_by_id('post-info-size')):
                self.closeTab()
            else:
                self.browser.refresh()
            print("getImg err:"+str(e))
            return False

    def nextPage(self):
        print("nextPage")
        try:

            log.lastUrl(self.browser.current_url)
            nextPage = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.paginator-next'))
            )

            nextPage.click()

        except Exception as e:
            self.browser.back()
            # self.browser.refresh()
            print("nextPage err:"+str(e))

    
    def openWebBrowser(self):
        cmd='chrome.exe '\
        '--remote-debugging-port=9222 '\
        '--user-data-dir="C:/selenium"'
        subprocess.run(cmd)

    def openPage(self):
        # cmd='chrome.exe '\
        # '--remote-debugging-port=9222 '\
        # '--user-data-dir="C:/selenium"'
        # subprocess.run(cmd)
        if self.browser == None:

            if self.openBs :
                chrome_options = Options()
                # chrome_options.add_argument('--disable-javascript') # 禁用javascript
                # chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])

                chrome_options.add_experimental_option('debuggerAddress','127.0.0.1:9222')

                self.browser = webdriver.Chrome(chrome_options=chrome_options)
            

            else:    
                chrome_options = Options()
                chrome_options.add_argument('--headless')
                self.browser = webdriver.Chrome(chrome_options=chrome_options)
            

            # self.browser = webdriver.Chrome(executable_path="C:/Users/Administrator/AppData/Local/Google/Chrome/Application/chrome.exe")
            # self.browser = webdriver.Firefox()

        
        self.open()


    def doSprider(self):
        # if self.browser == None:

        #     if self.openBs :
        #          self.browser = webdriver.Chrome()

        #     else:    
        #         chrome_options = Options()
        #         chrome_options.add_argument('--headless')
        #         self.browser = webdriver.Chrome(chrome_options=chrome_options)
            

        #     # self.browser = webdriver.Chrome(executable_path="C:/Users/Administrator/AppData/Local/Google/Chrome/Application/chrome.exe")
        #     # self.browser = webdriver.Firefox()
        
        # self.open()
        total = self.totalPage
        for i in range(0, total):
            try:
                if self.getImgs():
                    self.nextPage()
            except Exception as e:
                print("doSprider err:"+str(e))

    def start(self):
        print("start")
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
        self.browser.switch_to.window(self.browser.window_handles[1])

    def closeTab(self):
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])
