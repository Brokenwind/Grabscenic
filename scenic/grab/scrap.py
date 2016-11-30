#!/usr/bin/python

from bs4 import BeautifulSoup
from selenium import webdriver
import re

base="http://scenic.cthy.com"
browser.get(base)
index = BeautifulSoup(browser.page_source)
print index.prettify()
map = index.find("map") 
for item in map.find_all("area"):                                       
    print  item.attrs["href"]  
browser.get(base+"/province-33/")
temp = BeautifulSoup(browser.page_source)
browser.get(base+temp.select("a[href^=/scenicSearch]")[0].attrs["href"])

