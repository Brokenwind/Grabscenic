#!/usr/bin/python

import numpy
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from pandas import DataFrame,Series
from scenic import Scenic
from tables import Tables
import sys
sys.path.append("..")
from log import Logger

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class Grab:
    def __init__(self):
        self._logger = Logger(__file__)
        # the entry point of grabing 
        self.base="http://scenic.cthy.com"
        self.provinces = DataFrame()
        self.browser = webdriver.PhantomJS()
        self.tabopera = Tables();
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
            self._logger.info("got the the tag containing the information of provinces")
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
            self._logger.info("sorry,did not get the map data")
            return None
        self.provinces = DataFrame(protemp,index=index)
        #for item in self.provinces.keys():
        for item in self.provinces.index:
            self.searchScenic(item)
        #return self.provinces

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
        palist = first.find(id="PagerList")
        if palist:
            tags = palist.select("li > span")
        else:
            return False
        if tags and len(tags) >= 2:
            pageCount = int(tags[1].string)
            self._logger.info("total: "+tags[0].string+" records. "+"total "+tags[1].string+" pages")
        else:
            return False

        for i in range(1,pageCount+1):
            self.searchSeniceSpiPage(str(num),str(i))
        return True

    def searchSeniceSpiPage(self,num,page):
        """Search scenics information from a specified page of a specified province
        # Parameters:
        num:  the number of a province which you want to grab scenic information
        page: where now you want to extract scenic information from
        # Return:
        """
        addr = "/scenicSearch/"+str(num)+"-0-0-0-0-"+str(page)+".html"
        self.browser.get(self.base+addr)
        page = BeautifulSoup(self.browser.page_source)
        sightTags = page.select("div.sightlist > div.sightshow > div.sightdetail > h4 > a") 
        link = ""
        if sightTags:
            for item in sightTags:
                self._logger.info("got the link of "+item.string)
                link = item.attrs["href"]
                self.extractScenicInfor(link)
        else:
            return False
        return True

    def extractScenicInfor(self,link):
        """Extract a scenic information with the given scenic address
        # Parameters:
        link:  the address where you can get detailed information of scenic

        # Return:
        """
        self.tabopera.insertData(self.extractScenicAbout(link))

    def extractScenicAbout(self,link):
        """Extract the information of introduction,geographic postion,type,quality,class 
        # Parameters:
        link:  the address where you can get detailed information of scenic

        # Return:
        the return value is a dict which has fowllowing attrs:
        province: 
        city:
        types:
        level:
        fits:
        description:
        images:
        """
        scenic = Scenic()
        # got the symbol picture and the name of scenic at index page
        self.browser.get(link)
        first = BeautifulSoup(self.browser.page_source)
        symbol = first.select("div.sightfocuspic > img")
        if symbol:
            scenic.symbol = symbol[0].attrs["src"] and self.base+symbol[0].attrs["src"] or ""
        scename = first.select("div.sightprofile > h4")
        if scename:
            scenic.name = scename[0].string

        # if canot get the scenic name,it means the pages is wrong
        else:
            self._logger.error("Cannot got the scenic name. Is the page is wrong,please check it")
            return None
        # get detailed information about scenic at about page
        addr = link+"about.html"
        self.browser.get(addr)
        about = BeautifulSoup(self.browser.page_source)
        relative = about.select("div.main > div.wrap > div.pright > div.pfood > ul#RightControl11_ScenicBaseInfo > li")
        if len(relative) == 5:
            # get province and city information
            pos = relative[0].select("a")
            # It will only be right when we got two extract two infor
            if len(pos) == 2:
                if pos[0].string:
                    scenic.province = pos[0].string
                if pos[1].string:
                    scenic.city = pos[1].string
                self._logger.info("current position: province: "+scenic.province+" city: "+scenic.city)
            else:
                return None
            # get the type of scenic
            for item in relative[1].select("a"):
                if item.string:
                    scenic.types.append(item.string)
            # get the quality of scenic
            qua = relative[2].find("a")
            if qua:
                scenic.quality = qua.string
            # get the scenic level
            lev = relative[3].find("a")
            if lev:
                scenic.level = lev.string
            # get the fit time of the scenic
            for item in relative[4].select("a"):
                if item.string:
                    scenic.fits.append(item.string)
        else:
            self._logger.error("there is not ralative information"+str(len(relative)))
            return None

        # get the description of the scenic
        desc = about.find(id="AboutInfo")
        if desc:
            for s in desc.stripped_strings:
                scenic.description = scenic.description + s
            for item in desc.find_all("p"):
                # if a tag p contains image address,it always has the style or align attr
                attrs = item.attrs
                if "style" in attrs.keys() or "align" in attrs.keys():
                    for img in item.find_all("img"):
                        if not img.attrs["src"]:
                            continue
                        scenic.images.append(self.base+img.attrs["src"])
                else:
                    for s in item.stripped_strings:
                        scenic.description = scenic.description + "\n" + s
        else:
            self._logger.info("there is no description information and scenic pictures")
        scenic.website = link

        return scenic

    def extractScenicAttractions(self,link):
        """extract information of attractions of a specified scenic
        # Parameters:
        link:  the address where you can get attractions of scenic
        # Return:
        The return value is a list which the item is dict,each item contains the following attrs:
        
        """
        attractions = []
        addr = link+"about.html"
        self.browser.get(addr)
        page = BeautifulSoup(self.browser.page_source)
        lists = page.select("")

if __name__ == "__main__":
    grab = Grab()
    grab.getProvinces()

    #grab.searchScenic(33)
    """
    result = grab.extractScenicAbout("http://scenic.cthy.com/scenic-10046/")
    print result.symbol
    print result.name
    """
