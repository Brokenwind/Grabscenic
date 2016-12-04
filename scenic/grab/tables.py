#!/usr/bin/python
# codig:utf-8

from search import SearchParams
from mysql import MySQL
from bs4 import BeautifulSoup
from scenic import Scenic
import uuid
import sys
sys.path.append("..")
from log import Logger

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class Tables:
    """Create or Drop tables,delete data from tables
    """
    def __init__(self):
        self._logger = Logger(__file__)
        try:
            fsock = open("sqls.xml", "r")
        except IOError:
            self._logger.error("The file don't exist, Please double check!")
        self.sqls = BeautifulSoup(fsock.read())
        dbconfig = {'host':'127.0.0.1', 
                'port': 3306, 
                'user':'root', 
                'passwd':'123456', 
                'db':'scenic', 
                'charset':'utf8'}
        self.db = MySQL(dbconfig)

    def initDB(self):
        """create all tables
        """
        createSqls = self.sqls.find(id="createSql")
        for item in createSqls.select("item"):
            sql = item.string
            self._logger.info("create the table "+item.attrs["id"])
            self.db.execute(sql)
        # must reopen the cursor, or it will raise exception with error code 1024. What a fucking error
        self.db.reopenCursor()

    def dropAll(self):
        """drop all the tables
        """
        dropSqls= self.sqls.find(id="dropSql")
        for item in dropSqls.select("item"):
            sql = item.string
            self._logger.info("drop the table "+item.attrs["id"])
            self.db.execute(sql)
    def dropTable(self,name):
        """drop specified table
        """
        drop = self.sqls.find(id="dropSql").find(name)
        if drop:
            self._logger.info("drop the table "+name)
            self.db.execute(sql)
        else:
            self._logger.warn("Don't have the table "+name)
    def cleanAll(self):
        """delete data from all the tables,but not drop tables
        """
        cleanSqls= self.sqls.find(id="cleanSql")
        for item in cleanSqls.select("item"):
            sql = item.string
            self._logger.info("clean the table "+item.attrs["id"])
            self.db.execute(sql)
    def cleanTable(self,name):
        """clean the data of specified table
        """
        pass

    def insertTable(self,name,params):
        """insert values int to the specified table
        # Parameters:
        name: the name of the table
        params: the value insert into the tables. It can be tuple for inserting a row,or can be a list to insert serveral rows
        # Return:
        """
        insert = self.sqls.find(id="insertSql").find(id=name).string
        if insert:
            self._logger.info(insert + " insert into table "+name)
            self.db.insert(insert,params)
        else:
            self._logger.error("did not find the table "+name+" when insert")

    def insertData(self,data):
        """It is the interface for outer calling
        # Parameters:
        data: the value insert into the tables. It can be tuple for inserting a row,or can be a list to insert serveral rows
        # Return:
        """
        if isinstance(data,Scenic):
            data.encode()
            search = SearchParams()
            sceneryParams = (data.id,data.name,data.province,data.city,data.area,data.level,data.quality,data.description,data.website,data.symbol,None,None,data.price)
            imageParams = []
            for item in data.images:
                imageParams.append( (data.id,str(uuid.uuid1()),item,data.name,data.name) )
            typesParams = []
            for item in data.types:
                typesParams.append((data.id,search.scenicType[item]))
            fitsParams = []
            for item in data.fits:
                fitsParams.append((data.id,search.scenicFit[item]))
            
            self.insertTable("scenery",sceneryParams)
            # insert into database when only there are pictures,or it will occur error
            if imageParams:
                self.insertTable("sceneryImages",imageParams)
            self.insertTable("typeRelation",typesParams)
            self.insertTable("fitSeason",fitsParams)
        else:
            self._logger.error("the parameter is not the instance of Scenic")
            return False

    def initTables(self):
        """Initial basic tables including sceneryType,season
        """
        basic = SearchParams()
        # insert basic data into sceneryType table
        params = []
        for item in basic.scenicType.keys():
            params.append((basic.scenicType[item],item,item))
        self.insertTable("sceneryType",params)
        # insert basic data into season table
        params = []
        for item in basic.scenicFit.keys():
            params.append((basic.scenicFit[item],item))
        self.insertTable("season",params)

if __name__ == "__main__":
    tables = Tables()
    tables.dropAll()    
    tables.initDB()
    tables.cleanAll()
    tables.initTables()
    #tables.insertTable("season",(0,"all"))
    #tables.insertTable("sceneryType",(0,"all","all kinds of types"))
    #tables.insertTable("scenery",("xihuID3","xihu","zhejiang","hangzhou",None,"5A","","","","","",""))
    #tables.insertTable("fitSeason",("xihuID",501))
    #tables.insertTable("typeRelation",("xihuID",0))
    #tables.insertTable("sceneryImages",("xihuID",0,"www.baidu.com","xihu","nice","2016-03-12"))
    """
    params = []
    params.append((501,"spring"))
    params.append((502,"summer"))
    tables.insertTable("season",params)
    """
