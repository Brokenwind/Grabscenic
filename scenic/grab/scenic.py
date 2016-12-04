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
        self.id = str(uuid.uuid1())
        self.name = ""
        self.province = ""
        self.city = ""
        self.area = ""
        self.types = []
        self.level = ""
        self.quality = ""
        self.fits = []
        self.description = ""
        self.website = ""
        self.symbol = ""
        self.images = []
        self.price = 0.0

    def __str__(self):
        return "id "+self.id+"\nprovince"+self.province+"\ncity "+self.city+"\ntypes "+str(self.types)+"\nquality "+self.quality+"\nfits "+str(self.fits)+"\ndescription "+self.description+"\nimages "+str(self.images)

    def encode(self):
        self.name = self.name.encode("UTF-8")
        self.province = self.province.encode("UTF-8")
        self.city = self.city.encode("UTF-8")
        self.area = self.area.encode("UTF-8")
        for i in range(0,len(self.types)):
            self.types[i] = self.types[i].encode("UTF-8")
        self.level = self.level.encode("UTF-8")
        self.quality = self.quality.encode("UTF-8")
        for i in range(0,len(self.fits)):
            self.fits[i] = self.fits[i].encode("UTF-8")
        self.description = self.description.encode("UTF-8")
        self.website = self.website.encode("UTF-8")
        self.symbol = self.symbol.encode("UTF-8")
        for i in range(0,len(self.images)):
            self.images[i] = self.images[i].encode("UTF-8")

if __name__ == "__main__":
    scenic = Scenic()
    print scenic

