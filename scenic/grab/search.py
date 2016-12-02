#!/usr/bin/python
#coding=utf-8

import numpy as np
from pandas import DataFrame,Series

class SearchParams:
    def __init__(self):
        self.unknownCode = -1
        self.unknownName = "unknown"
        self.typeCode = [0,101, 102, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116]
        self.typeName = ["全部","海滨海岛","特殊地貌","城市风景","生物景观","壁画石窟","民俗风情","历史圣地","纪念地","山岳","岩洞","江河","湖泊","陵寝","其他","温泉"]
        self.scenicType = Series(self.typeCode,index=self.typeName)
        self.classCode = [0, 201, 202, 203, 204, 205]
        self.className = ["全部","5A","4A","3A","2A","其他"]
        self.scenicClass = Series(self.classCode,index=self.className)
        self.qualityCode = [0,301,302,303]
        self.qualityName =["全部","国家级风景名胜区","省级风景名胜区","其他"]
        self.scenicQuality = Series(self.qualityCode,index=self.qualityName)
        self.fitCode = [0,401,402,403,404,405]
        self.fitName = ["全部","春季","夏季","秋季","冬季","四季皆宜"]
        self.scenicFit = Series(self.fitCode,index=self.fitName)

    def getTypeCode(self,typeName):
        if typeName in self.typeName:
            return self.scenicType[typeName]
        else:
            return self.unknownCode
    
    def getClassCode(self,className):
        if className in self.className:
            return self.scenicClass[className]
        else:
            return self.unknownCode

    def getQualityCode(self,qualityName):
        if qualityName in self.qualityName:
            return self.scenicQuality[qualityName]
        else:
            return self.unknownCode

    def getFitCode(self,fitName):
        if fitName in self.fitName:
            return self.scenicFit[fitName]
        else:
            return self.unknownCode

    """
    def getTypeName(self,typeCode):
        if typeCode in self.typeCode:
            return self.scenicType[typeCode]
        else:
            return self.unknownName
    
    def getClassName(self,classCode):
        if classCode in self.classCode:
            return self.scenicClass[classCode]
        else:
            return self.unknownName

    def getQualityName(self,qualityCode):
        if qualityCode in self.qualityCode:
            return self.scenicQuality[qualityCode]
        else:
            return self.unknownName

    def getFitName(self,fitCode):
        if fitCode in self.fitCode:
            return self.scenicFit[fitCode]
        else:
            return self.unknownName
    """
if __name__ == "__main__":
    search =  SearchParams()
    print search.getTypeCode("全部")
    print search.getClassCode("全部")
    print search.getQualityCode("全部")
    print search.getFitCode("全部")
