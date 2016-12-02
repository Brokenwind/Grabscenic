#!/usr/bin/python

import numpy
import re
import search
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
                print "got the link of "+item.string
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
        self.extractScenicAbout(link)

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
        scenic = {}
        addr = link+"about.html"
        self.browser.get(addr)
        about = BeautifulSoup(self.browser.page_source)
        relative = about.select("div.main > div.wrap > div.pright > div.pfood > ul#RightControl11_ScenicBaseInfo > li")
        if len(relative) == 5:
            # get province and city information
            pos = relative[0].select("a")
            # It will only be right when we got two extract two infor
            if len(pos) == 2:
                scenic["province"] = pos[0].string
                scenic["city"] = pos[1].string
            else:
                return None
            # get the type of scenic
            types = []
            for item in relative[1].select("a"):
                types.append(item.string)
            scenic["types"] = types
            # get the quality of scenic
            scenic["quality"] = relative[2].find("a").string
            # get the scenic level
            scenic["level"] = relative[3].find("a").string
            # get the fit time of the scenic
            fits = []
            for item in relative[4].select("a"):
                fits.append(item.string)
            scenic["fits"] = fits
        else:
            print "there is not ralative information"+str(len(relative))
            return None
        # get the description of the scenic
        desc = about.find(id="AboutInfo")
        descText = ""
        descImg = []
        """
        for item in about.find("br"):
            item.replace_with("\n")
        """
        for s in desc.stripped_strings:
            descText = descText + s
        ptags = desc.find_all("p")
        if ptags:
            for item in ptags:
                con = item.stripped_strings
                if con:
                    for s in con:
                        descText = descText + "\n" + s
                img = item.find("img")
                if img:
                    descImg.append(self.base+img.attrs["src"])
        scenic["description"] = descText
        scenic["images"]=descImg
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
    grab.extractScenicAbout("http://scenic.cthy.com/scenic-10046/")
