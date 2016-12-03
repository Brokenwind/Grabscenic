#!/usr/bin/python
# codig:utf-8

from mysql import MySQL
from bs4 import BeautifulSoup

class Tables:
    """Create or Drop tables,delete data from tables
    """
    def __init__(self):
        try:
            fsock = open("sqls.xml", "r")
        except IOError:
            print "The file don't exist, Please double check!"
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
            self.db.execute(sql)
    def dropAll(self):
        """drop all the tables
        """
        dropSqls= self.sqls.find(id="dropSql")
        for item in dropSqls.select("item"):
            sql = item.string
            self.db.execute(sql)

    def dropTable(self,name):
        """drop specified table
        """
        drop = self.sqls.find(id="dropSql").find(name)
        if drop:
            self.db.execute(sql)
        else:
            print "Don't have the table"

    def cleanAll(self):
        """delete data from all the tables,but not drop tables
        """
        cleanSqls= self.sqls.find(id="cleanSql")
        for item in cleanSqls.select("item"):
            sql = item.string
            print "clean the table "+item.attrs["id"]
            self.db.execute(sql)

    def cleanTable(self,name):
        """clean the data of specified table
        """
        pass

if __name__ == "__main__":
    tables = Tables()
    tables.initDB()
    tables.cleanAll()
    #tables.dropAll()
