#!/usr/bin/python
# coding: utf-8

__author__ = "Brokenwind"

import numpy
import re
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pandas import DataFrame,Series
# import Logger
sys.path.append("..")
from log import Logger
# set global charset
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class Baidu:
    def __init__(self):
        self._logger = Logger(__file__)
        # baidu search website
        self.baidu="https://www.baidu.com"
        self.browser = webdriver.Firefox()

    def __del__(self):
        self.browser.quit()

    def search(self,params,suffix):
        """search the keywords and return the first item link
        # Parameter:
        params:
        suffix:
        # Return:
        the link of the first item
        """
        # arrange the parameter to str
        paramstr = ""
        if isinstance(params,dict):
            for item in params.keys():
                paramstr = paramstr + str(item) + ":" + str(params[item]) + " "
        elif isinstance(params,list):
            for item in params:
                paramstr = paramstr + str(item) + " "
        elif isinstance(params,str):
            paramstr = params+" "
        else:
            self._logger.error("the parameter must be a dict, list or str")
        paramstr = paramstr + suffix
        # begin searching
        self.browser.get(self.baidu)
        searinput = self.browser.find_element_by_name("wd")
        searinput.send_keys(paramstr.decode())
        searinput.send_keys(Keys.RETURN)
        # get the first one from search result
        link = ""
        try:
            # get the first of result list
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='wrapper_wrapper']/div[@id='container']/div[@id='content_left']/div[@id='1']"))
            )
            first = self.browser.find_element_by_xpath("//div[@id='wrapper_wrapper']/div[@id='container']/div[@id='content_left']/div[@id='1']")
            # get first item of list
            firstlink = first.find_element_by_xpath("//h3/a")
            link = firstlink.get_attribute("href")
            self._logger.info("the title of the first item of list is: "+firstlink.text)
            # this is the visible link at the bottom of at every retult item
            firsturl = first.find_element_by_xpath("//p[@class=' op-bk-polysemy-move']/span[@class='c-showurl']")
            self._logger.info("the link of the first item of list is: "+firsturl.text)
        except Exception,e:
            self._logger.error("search: error happend when got the search result "+str(e.args))
            return None
        return link

    def baike(self,params):
        """extract information from baidu baike
        """
        suffix = " 百度百科"
        link = self.search(params,suffix)
        if not link:
            return None
        """
        if use the following statement:
        firstlink.click()
        the browser will open a new window to show information,but the self.browser is still keep the old url. So you can not get the new page information.
        """
        self.browser.get(link)
        # extract Baike contents,after entering the first item  
        result = {}        
        try:
            #print self.browser.current_url

            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "lemma-summary"))
            )
            # this tag contains all the information of the searching item
            content = self.browser.find_element_by_class_name("main-content")
            # get the real name,the name you are searching maybe is incorrect
            result["name"] = content.find_element_by_xpath("//dl/dd/h1").text
            self._logger.info("got the content div")
            # get summary of the searching item
            result["summary"] = content.find_element_by_class_name("lemma-summary").text
            self._logger.info("got the summary div")
            # left and right basic information
            basicLeft = content.find_element_by_class_name("basicInfo-left")
            basicRight = content.find_element_by_class_name("basicInfo-right")
            self._logger.info("got the basic left and right div")
            basics = {}
            # get left  basic info
            titles = basicLeft.find_elements_by_tag_name("dt")
            cons = basicLeft.find_elements_by_tag_name("dd")
            if len(titles) == len(cons):
                for i in range(0,len(titles)):
                    basics[titles[i].text] = cons[i].text
            else:
                self._logger.warn("Basic info left: the number of titles is not equal to the number of cons")
            # get right basic info
            titles = basicRight.find_elements_by_tag_name("dt")
            cons = basicRight.find_elements_by_tag_name("dd")
            if len(titles) == len(cons):
                for i in range(0,len(titles)):
                    basics[titles[i].text] = cons[i].text
            else:
                self._logger.warn("Basic info right: the number of titles is not equal to the number of cons")
            result["basic"] = basics

            # get the deatiled information
            detail = ""
            pictures = []
            descs = content.find_elements_by_xpath("//div[@class='para'] | //div[@class='para-title level-2']/h2 | //div[@class='para-title level-3']/h3")
            for item in descs:
                images = item.find_elements_by_tag_name("img")
                # if the tag contains img tag,we do not got it's text,but to get the image address
                if images:
                    for img in images:
                        pictures.append(img.get_attribute("src"))
                        self._logger.info("Detail: Get a new picture")
                else:
                    detail = detail + item.text + "\n"
            result["detail"] = detail
            result["pictures"] = pictures
        except Exception,e:
            self._logger.error("errors occurred when extracting Baike contents: "+str(e.args))
            return None
        return result

    def image(self,params,num=10,width=400,height=400):
        """Get images from baidu
        # Parameters:
        num: the number of pictures you want to get
        width: the minimal width of picture
        height: the minimal height of picture
        # Return:
        a list of map address
        """
        suffix = " 图片"
        link = self.search(params,suffix)
        if not link:
            return None
        self.browser.get(link)
        result = []
        try:
            pages = self.browser.find_elements_by_xpath("//div[@id='imgid']/div[@class='imgpage']/ul")
            #firstpage = self.browser.find_element_by_xpath("//div[@id='imgid']/div[@class='imgpage']/ul")
            self._logger.info("got image gallery,it is grabing...")
            for page in pages:
                for item in page.find_elements_by_tag_name("li"):
                    if len(result) >= num:
                        self._logger.info("finally,we got "+str(len(result))+" pictures")
                        return result
                    wid = int(item.get_attribute("data-width"))
                    hei = int(item.get_attribute("data-height"))
                    if wid >= width and hei >= height:
                        result.append(item.get_attribute("data-objurl"))
            self._logger.info("sorry,we did not grab enough "+str(num)+" pictures,just "+str(len(result))+" pictures")
            return result
        except Exception,e:
            self._logger.error("errors occurred when extracting images contents: "+str(e.args))

if __name__ == "__main__":
    search = Search()
    search.image("珏山旅游风景区",10)
