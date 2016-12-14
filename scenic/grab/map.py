#!/usr/bin/python
# coding: utf-8

__author__ = "Brokenwind"

import numpy
import re
import sys
import urllib2
import json
from decimal import *
# import Logger
sys.path.append("..")
from log import Logger
# set global charset
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class BaiduMap:
    def __init__(self):
        self._logger = Logger(__file__)
        self.status ={0:"正常",
                      1:"服务器内部错误",
                      2:"请求参数非法",
                      3:"权限校验失败",
                      4:"配额校验失败",
                      5:"ak不存在或者非法",
                      101:"服务禁用",
                      102:"不通过白名单或者安全码不对",
                      200:"无权限",
                      300:"配额错误"}
        self.geoprefix = "http://api.map.baidu.com/geocoder/v2/?address="
        self.revprefix = "http://api.map.baidu.com/geocoder/v2/?location="
        self.suffix = "&output=json&ak="

    def getGeoAddress(self,position,ak):
        """get the longitude and latitude
        # Parameters:
        position: the name of a position
        ak: baidu access key,you need apply for it
        # Return: a dict which contains following attrs:
        location: consists of lng and lat attrs
        precise:
        confidence:
        level:
        """
        url = self.geoprefix + position + self.suffix + ak
        result = None
        try:
            response = urllib2.urlopen(url)
            data = json.loads(response.read())
            #data = json.loads('{"status":103,"result":{"location":{"lng":123.9872889421725,"lat":47.34769981336638},"precise":0,"confidence":10,"level":"城市"}}')
            self._logger.info("get address: "+str(data))
            if not data:
                return None
            if "status" in data.keys():
                state = data["status"]
                if not state == 0:
                    if state < 200:
                        if state in self.status.keys():
                            self._logger.warn("did not got address,reason: "+self.status[state])
                        else:
                            self._logger.warn("did not got address,unknow reason")
                    elif state < 300:
                        self._logger.warn("did not got address,reason: "+self.status[200])
                    else:
                        self._logger.warn("did not got address,reason: "+self.status[300])
                    return None
                else:
                    if "result" in data.keys():
                        self._logger.info("successfully got the address")
                        return data["result"]
                    else:
                        self._logger.warn("the data do not have attr result")
                        return None
            else:
                self._logger.warn("the response data do not have attr status")
                return None

        except Exception,e:
            self._logger.error("error occured when get geo data")
            return None
    
    def reverseGeoAddress(self,lng,lat,pois,ak):
        """got the position according to the given longitude and latitude 
        # Parameters:
        lng: the longitude
        lat: the latitude
        pois: 是否显示指定位置周边的poi，0为不显示，1为显示。当值为1时，显示周边100米内的poi。
        ak: baidu access key
        # Return: a dict
        location 		lat 	纬度坐标
                        	lng 	经度坐标 
        business 		所在商圈信息，如 "人民大学,中关村,苏州街"
        addressComponent	country 	国家
                                province 	省名
 			        city 	城市名
			        district 	区县名
			        street 	街道名
			        street_number 	街道门牌号
			        adcode 	行政区划代码
                                country_code 	国家代码
                                direction 	和当前坐标点的方向，当有门牌号的时候返回数据
                                distance 	和当前坐标点的距离，当有门牌号的时候返回数据
        pois（周边poi数组） 	addr 	地址信息
        			cp 	数据来源
			        direction 	和当前坐标点的方向
			        distance 	离坐标点距离
			        name 	poi名称
			        poiType 	poi类型，如’ 办公大厦,商务大厦’
			        point 	poi坐标{x,y}
			        tel 	电话
			        uid 	poi唯一标识
			        zip 	邮编
        sematic_description 	constant 	当前位置结合POI的语义化结果描述。 
        """
        location = str(lng)+","+str(lat)
        poisattr = "&pois="+str(pois)
        url = self.revprefix + location + poisattr + self.suffix + ak
        print url
        result = None
        try:
            response = urllib2.urlopen(url)
            data = json.loads(response.read())
            self._logger.info("get data: "+str(data))
            if not data:
                return None
            if "status" in data.keys():
                state = data["status"]
                if not state == 0:
                    if state < 200:
                        if state in self.status.keys():
                            self._logger.warn("did not got address,reason: "+self.status[state])
                        else:
                            self._logger.warn("did not got address,unknow reason")
                    elif state < 300:
                        self._logger.warn("did not got address,reason: "+self.status[200])
                    else:
                        self._logger.warn("did not got address,reason: "+self.status[300])
                    return None
                else:
                    if "result" in data.keys():
                        self._logger.info("successfully got the address")
                        return data["result"]
                    else:
                        self._logger.warn("the data do not have attr result")
                        return None
            else:
                self._logger.warn("the response data do not have attr status")
                return None

        except Exception,e:
            self._logger.error("error occured when to reverse the geo data")
            return None

if __name__ == "__main__":
    search = BaiduMap()
    print "%.13f" % search.getGeoAddress("齐齐哈尔铁农园艺","sh0wDYRg1LnB5OYTefZcuHu3zwuoFeOy")["location"]["lng"]
    #print search.reverseGeoAddress("47.34769981336638","123.9872889421725",1,"sh0wDYRg1LnB5OYTefZcuHu3zwuoFeOy")["formatted_address"]
