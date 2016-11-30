#!/usr/bin/python

import numpy
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from pandas import DataFrame,Series

class Grab:
    def __init__(self):
        # the entry point of grabing 
        self.base="http://scenic.cthy.com"
        self.provinces = DataFrame()
    def getProvinces(self):
        '''Get the information of link, area and the number of provinces.
        # Process:
            1): To get the source code of the entry point (http://scenic.cthy.com) with PhantomJS
            2): To find tag which contains the information of provinces
            3): Get link,area and number information of every province
        # Return: 
            The return value is a DataFrame contains the following attributes:
                link: the relative web address of details
                area: the name of province
                num:  the specified number of a province for further use
        '''
        browser = webdriver.PhantomJS()
        browser.get(self.base)
        index = BeautifulSoup(browser.page_source)
        map = index.find("map") 
        if map:
            protemp = []
            # the pattern to extract number from link
            pattern = re.compile(r".*(\d\d)/")
            print ("got the the tag containing the information of provinces")
            for item in map.find_all("area"):
                mapattrs={}
                mapattrs["link"]=item.attrs["href"]
                mapattrs["area"]=item.attrs["alt"]
                number = re.findall(pattern,item.attrs["href"])
                if number:
                    mapattrs["num"]=number[0]
                else:
                    mapattrs["num"]="NULL"
                protemp.append(mapattrs)
        else:
            print ("sorry,did not get the map data")
            return None
        self.provinces = DataFrame(protemp)
        return self.provinces
        #browser.get(base+"/province-33/")
        #temp = BeautifulSoup(browser.page_source)
        #browser.get(base+temp.select("a[href^=/scenicSearch]")[0].attrs["href"])
if __name__ == "__main__":
    grab = Grab()
    grab.getProvinces()
