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
        self.browser = webdriver.PhantomJS()
    def getProvinces(self):
        '''Get the information of link, area and the number of provinces.
        # Process:
            1): To get the source code of the entry point (http://scenic.cthy.com) with PhantomJS
            2): To find tag which contains the information of provinces
            3): Get link,area and number information of every province
        # Return: 
            The return value is a DataFrame contains the following attributes:
                index:  the specified number of a province which extract from link for further use
                link:   the relative web address of details
                area:   the name of province
        '''

        self.browser.get(self.base)
        entry = BeautifulSoup(self.browser.page_source)
        map = entry.find("map") 
        if map:
            protemp = []
            index = []
            # the pattern to extract number from link
            pattern = re.compile(r".*(\d\d)/")
            print ("got the the tag containing the information of provinces")
            for item in map.find_all("area"):
                mapattrs={}
                mapattrs["link"]=item.attrs["href"]
                mapattrs["area"]=item.attrs["alt"]
                number = re.findall(pattern,item.attrs["href"])
                if number:
                    index.append(number[0])
                else:
                    continue
                protemp.append(mapattrs)
        else:
            print ("sorry,did not get the map data")
            return None
        self.provinces = DataFrame(protemp,index=index)
        return self.provinces
    def searchScenic(self,num):
        """Extract scenics information of a spicified province.
        # Parameters:
        num: the number of a province which you want to grab scenic information
        # Return:
        
        """
        prefix = "/scenicSearch/"
        suffix = "-0-0-0-0-1.html"
        self.browser.get(self.base+prefix+str(num)+suffix)
        first = BeautifulSoup(self.browser.page_source)
        """ The content of tags:
        # the total records
        [<span class="f14 point">135</span>,
        # how many pages
        <span class="f14 point">14</span>,
        # the number of records of one page
        <span class="f14 point">10</span>]
        """
        tags = first.find(id="PagerList").select("li > span")
        if tags:
            pageCount = int(tags[1].string)
            #print self.provinces.ix[str(num)]+"\ntotal: "+tags[0].string+" records.\n"+"total "+tags[1].string+" pages"
            print "total: "+tags[0].string+" records.\n"+"total "+tags[1].string+" pages"
        else:
            return False
        """
        for i in range(1,pageCount+1):
            searchSeniceSpiPage(str(num),str(page))
        """
        self.searchSeniceSpiPage(str(num),str(1))
        return True

    def searchSeniceSpiPage(self,num,page):
        addr = "/scenicSearch/"+str(num)+"-0-0-0-0-"+str(page)+".html"
        self.browser.get(self.base+addr)
        page = BeautifulSoup(self.browser.page_source)
        sightTags = page.select("div.sightlist > div.sightshow > div.sightdetail > h4 > a") 
        if sightTags:
            for item in sightTags:
                print "got the link of "+item.string
                link = item.attrs["href"]
                print link
        else:
            return False
        return True
if __name__ == "__main__":
    grab = Grab()
    grab.searchScenic(33)
