#!/usr/bin/python
# coding=utf-8
import numpy
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from pandas import DataFrame,Series
from scenic import Scenic
from tables import Tables
from baidu import Baidu
from map import BaiduMap
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
        self.provinces = []
        #self._browser = webdriver.PhantomJS()
        self._browser = webdriver.Firefox()
        self.tabopera = Tables();
        self.record = open("record.txt","a+")
        self.fdate = open("date.txt","a+")
        self.fprice = open("price.txt","a+")
        self.sprovince = 0
        self.spage = 1
        self.snum = 0
        self.picturenum = 10
        self.baidu = Baidu()
        self.map = BaiduMap()
        self.ak = "sh0wDYRg1LnB5OYTefZcuHu3zwuoFeOy"
    def __del__(self):
        self._browser.quit()
        self.record.close()

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

        self._browser.get(self.base)
        entry = BeautifulSoup(self._browser.page_source)
        map = entry.find("map") 
        if map:
            # the pattern to extract number from link
            pattern = re.compile(r".*(\d\d)/")
            self._logger.info("got the the tag containing the information of provinces")
            for item in map.find_all("area"):
                number = re.findall(pattern,item.attrs["href"])
                if number:
                    self.provinces.append(number[0])
                else:
                    continue
        else:
            self._logger.info("sorry,did not get the province map data")
            return None
        return self.provinces

    def searchAll(self):
        for i in range(self.sprovince,len(self.provinces)):
            self.searchScenic(i)
        
    def searchScenic(self,num):
        """Extract scenics information of a spicified province.
        # Parameters:
        num: the number of a province which you want to grab scenic information
        # Return:
        """
        prefix = "/scenicSearch/"
        suffix = "-0-0-0-0-1.html"
        self._browser.get(self.base+prefix+str(self.provinces[num])+suffix)
        first = BeautifulSoup(self._browser.page_source)
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

        for i in range(self.spage,pageCount+1):
            self.searchSeniceSpiPage(num,str(i))
        # it is import, it must be reset to 1
        self.spage = 1
        return True

    def searchSeniceSpiPage(self,num,pagenum):
        """Search scenics information from a specified page of a specified province
        # Parameters:
        num:  the number of a province which you want to grab scenic information
        page: where now you want to extract scenic information from
        # Return:
        """
        addr = "/scenicSearch/"+str(self.provinces[num])+"-0-0-0-0-"+str(pagenum)+".html"
        # record the current searching page
        self._browser.get(self.base+addr)
        page = BeautifulSoup(self._browser.page_source)
        sightTags = page.select("div.sightlist > div.sightshow > div.sightdetail > h4 > a") 
        link = ""
        if sightTags:
            for i in range(self.snum,len(sightTags)):
                # recording the number of province,page,item for recovery
                self.record.write(str(num)+" "+str(pagenum)+" "+str(i)+"\n")
                self._logger.info("current position: "+str(num)+" "+str(pagenum)+" "+str(i))
                self._logger.info("got the link of "+sightTags[i].string)
                link = sightTags[i].attrs["href"]
                self.extractScenicInfor(link)
        else:
            self._logger.error("searchSeniceSpiPage: can not get the list of scenics")
            return False
        # it is import, it must be reset to 1
        self.snum = 0
        return True

    def extractScenicInfor(self,link):
        """Extract a scenic information with the given scenic address
        # Parameters:
        link:  the address where you can get detailed information of scenic
        # Return:
        """
        scenic = self.extractScenicAbout(link)
        if not scenic:
            return False;
        scenic = self.remedy(scenic)
        scenic = self.remedyMap(scenic)
        self.tabopera.insertData(scenic)
        return True

    def remedy(self,scenic):
        """if the return of function  extractScenicAbout if not enough,we need to access baidu for more information
        """
        openpat = u"开放时间"
        suggpat = u"时长"
        areapat = u"面积"
        pricepat = u"门票"

        # this is for getting longitude and latitude
        scenic.mapname = scenic.name

        # remedy pictures
        picnum = len(scenic.images)
        if picnum < 10:
            self._logger.info("There are "+str(picnum)+" pictures.Getting the reset from baidu image")
            imgs = self.baidu.image(scenic.name,self.picturenum - len(scenic.images))
            if imgs:
                scenic.images.extend(imgs)

        if not scenic.description:
            self._logger.info("Got details from baike")
            baike = self.baidu.baike(scenic.name)
            if not baike:
                self._logger.error("Remedy: can not got information from baidu baike")
                return scenic
            if "detail" in baike.keys():
                scenic.description = baike["detail"]
        else:
            baike = self.baidu.baike(scenic.name,False)
            if not baike:
                self._logger.error("Remedy: can not got information from baidu baike")
                return scenic

        # use the name in baike for baidu searching
        if "name" in baike.keys():
            scenic.mapname = baike["name"]

        if "basic" in baike.keys():
            basic = baike["basic"]
            for item in basic.keys():
                if re.findall(openpat,item):
                    times = re.findall(r"(\d+[:|;]\d+).*(\d+[:|;]\d+)",basic[item])
                    if times:
                        scenic.opentime = times[0][0]
                        scenic.closetime = times[0][1]
                    else:
                        scenic.opentime = "00:00"
                        scenic.closetime = "23:00"
                if re.findall(suggpat,item):
                    scenic.suggest = basic[item]
                if re.findall(pricepat,item):
                    scenic.price = basic[item]
                if re.findall(areapat,item):
                    scenic.area = basic[item]
        if not scenic.opentime:
            scenic.opentime = "00:00"
        if not scenic.closetime:
            scenic.closetime = "23:00"
        if not scenic.price:
            scenic.price = "0"
        if not scenic.area:
            scenic.area = "未知"
        if not scenic.symbol:
            if scenic.images:
                scenic.symbol = scenic.images[0]
        return scenic

    def remedyMap(self,scenic):
        # map relatives:
        mapret = self.map.getGeoAddress(scenic.mapname,self.ak)
        if mapret:
            if "location" in mapret.keys():
                scenic.latitude = "%.13f" % mapret["location"]["lat"]
                scenic.longitude = "%.13f" % mapret["location"]["lng"]
            if "precise" in mapret.keys():
                scenic.precise = str(mapret["precise"])
            if "confidence" in mapret.keys():
                scenic.confidence = str(mapret["confidence"])
        return scenic
        
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
        self._browser.get(link)
        first = BeautifulSoup(self._browser.page_source)
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
        self._browser.get(addr)
        about = BeautifulSoup(self._browser.page_source)
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
                scenic.description = scenic.description + s + "\n"
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
                        scenic.description = scenic.description + s + "\n" 
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
        self._browser.get(addr)
        page = BeautifulSoup(self._browser.page_source)
        lists = page.select("")

    def startGrab(self):
        content = self.record.readlines()
        # if do not have record
        if len(content) != 0:
            line = content[len(content)-1]
            strs = line.split(" ")
            self.sprovince = int(strs[0])
            self.spage = int(strs[1])
            self.snum = int(strs[2])
        self.getProvinces()
        self.searchAll()

if __name__ == "__main__":
    grab = Grab()
    grab.getProvinces()
    #grab.extractScenicInfor("http://scenic.cthy.com/scenic-12654/")
    grab.startGrab()
    #grab.searchScenic(-2)
    """
    result = grab.extractScenicAbout("http://scenic.cthy.com/scenic-10046/")
    print result.symbol
    print result.name
    """
