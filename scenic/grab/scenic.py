#!/usr/bin/python
# codig:utf-8

import uuid
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class Scenic:
    """It is used to encapsule the result of grabing
    """
    def __init__(self):
        self.id = ""
        self.name = ""
        self.mapname = ""
        self.province = ""
        self.city = ""
        self.area = ""
        self.types = []
        self.level = "unknown"
        self.quality = "unknown"
        self.fits = []
        self.description = ""
        self.website = ""
        self.symbol = ""
        self.images = []
        self.price = "unknown"
        self.suggest = "unknown"
        self.opentime = "00:00"
        self.closetime = "23:00"
        self.longitude = "0.0"
        self.latitude = "0.0"
        self.precise = "0"
        self.confidence = "0"
    def __str__(self):
        return "id "+self.id+"\nprovince"+self.province+"\ncity "+self.city+"\ntypes "+str(self.types)+"\nquality "+self.quality+"\nfits "+str(self.fits)+"\ndescription "+self.description+"\nimages "+str(self.images)

    def encode(self):
        """If attributes is None and than given a empty string,or it will ben ecncode into utf-8
        """
        self.id = self.name
        self.name = self.name and self.name.encode("UTF-8") or ""
        self.province = self.province and self.province.encode("UTF-8") or ""
        self.city = self.city and self.city.encode("UTF-8") or ""
        self.area = self.area and self.area.encode("UTF-8") or ""
        for i in range(0,len(self.types)):
            self.types[i] = self.types[i].encode("UTF-8")
        self.level = self.level and self.level.encode("UTF-8") or ""
        self.quality = self.quality and self.quality.encode("UTF-8") or ""
        for i in range(0,len(self.fits)):
            self.fits[i] = self.fits[i].encode("UTF-8")
        self.description = self.description and self.description.encode("UTF-8") or ""
        self.website = self.website and self.website.encode("UTF-8") or ""
        self.symbol = self.symbol and self.symbol.encode("UTF-8") or ""
        self.price = self.price and self.price.encode("UTF-8") or ""
        for i in range(0,len(self.images)):
            self.images[i] = self.images[i].encode("UTF-8")
        self.suggest = self.suggest and self.suggest.encode("UTF-8") or ""
        self.opentime = self.opentime and self.opentime.encode("UTF-8") or ""
        self.closetime = self.closetime and self.closetime.encode("UTF-8") or ""
        self.longitude = self.longitude and self.longitude.encode("UTF-8") or ""
        self.latitude = self.latitude and self.latitude.encode("UTF-8") or ""
        self.mapname = self.mapname and self.mapname.encode("UTF-8") or ""
if __name__ == "__main__":
    scenic = Scenic()
    print scenic

