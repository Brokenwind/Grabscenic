#!/usr/bin/python
# coding: utf-8

import MySQLdb
import time

class MySQL:
    # the mysql error code
    error_code = ''
    # the instance of this class
    _instance = None
    # the database connection object
    _conn = None
    # the cursor
    _cur = None
    # the default timeout
    _TIMEOUT = 30
    _timecount = 0
    def __init__(self, dbconfig):
        """create database connection with specified arguments
        # Parameters:
        dbconfig: the configuration argument:
            host:
            user:
            passwd:
            port:
            charset:
        # Return:
        """
        try:
            self._conn = MySQLdb.connect(host=dbconfig['host'],
                port=dbconfig['port'], 
                user=dbconfig['user'],
                passwd=dbconfig['passwd'],
                db=dbconfig['db'],
                charset=dbconfig['charset'])
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            error_msg = 'MySQL error! ', e.args[0], e.args[1]
            print error_msg
            # if not exceed the default timeout, try again
            if self._timecount < self._TIMEOUT:
                interval = 5
                self._timecount += interval
                time.sleep(interval)
                self.__init__(dbconfig)
            else:
                raise Exception(error_msg)
        self._cur = self._conn.cursor()

    def query(self,sql,params=None):
        """Execute select without parameter
        # Parameters:
        sql: the query sql you want to execute
        # Return:
        
        """
        try:
            self._cur.execute("SET NAMES utf8") 
            if params:
                result = self._cur.execute(sql,params)
            else:
                result = self._cur.execute(sql)
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print "database error code:",e.args[0],e.args[1]
            result = None
        return result

    def update(self,sql,params=None):
        """update table with given sql statement
        """
        try:
            self._cur.execute("SET NAMES utf8") 
            if params:
                result = self._cur.execute(sql,params)
            else:
                result = self._cur.execute(sql)
            self._conn.commit()
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print "database error code:",e.args[0],e.args[1]
            self.rollback()
            result = False
        return result

    def insert(self,sql,params=None):
        """if primary key is auto incremented, it will return the id
        """
        try:
            self._cur.execute("SET NAMES utf8")
            if params:
                self._cur.execute(sql,params)
            else:
                self._cur.execute(sql)
            self._conn.commit()
            return self._conn.insert_id()
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            self.rollback()
            return False
	
    def fetchAll(self):
        """return all the selected values
        """
        return self._cur.fetchall()
    def fetchOne(self):
        """return current data,and the cursor move to the next position
        """
        return self._cur.fetchone()
 
    def getCount(self):
        """get the count of the result
        """
        return self._cur.rowcount
						  
    def commit(self):
        """commint the operation
        """
        self._conn.commit()
						
    def rollback(self):
        """rollback the operation
        """
        self._conn.rollback()
    def __del__(self): 
        """close the cursor and database,release resources
        """
        try:
            self._cur.close() 
            self._conn.close() 
        except:
            pass
		
    def  close(self):
        """call self defined __del__() to close cursor and database
        """
        self.__del__()

if __name__ == '__main__':
    dbconfig = {'host':'127.0.0.1', 
                'port': 3306, 
                'user':'root', 
                'passwd':'123456', 
                'db':'test', 
                'charset':'utf8'}
    db = MySQL(dbconfig)
    sql = "SELECT * FROM `user`"
    db.query(sql);
    result = db.fetchAll();
    print type(result)
    for row in result:
        for colum in row:
            print colum
    # sql="insert into password(password_id,password) values('%s','%s')" % ("asdfaddsndrd","1234")
    sql="insert into password(password_id,password) values('%s','%s')"
    params = ("asdfaddsnewpasswoddrd","1234")
    print db.insert(sql,params)
    print db.error_code
    db.close()
