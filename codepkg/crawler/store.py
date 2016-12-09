#!/usr/bin/python

import os
import MySQLdb
import codecs
import string
from travel import City

ids = []
provinces=[]
cnames = []
clevels = []
def readfile(file):
    os.chdir('C:\Users\dell\Desktop\python')
    fs = codecs.open(file, encoding='gbk')
    lines = fs.readlines()
    citys=[]
    for line in lines:
        items = string.split(line, '\t')
        city = City()
        city.id = int(items[0])
        city.province = items[1]
        city.cname = items[2]
        city.clevel = items[3]
        citys.append(city)
    fs.close()
    return citys

def storeProvince(file):
    os.chdir('C:\Users\dell\Desktop')
    try:
        fs = codecs.open(file, encoding='gbk')
        lines = fs.readlines()
        mysql = "insert into province values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        db = MySQLdb.connect('127.0.0.1', 'root', 'admin', 'pythondb', charset="utf8")
        cursor = db.cursor()
        for line in lines:
            line = line.strip('\r\n')
            items = string.split(line,'\t')
            cursor.execute(mysql,items)
            db.commit()
    except Exception,msg:
        print msg
    finally:
        fs.close()

def storeCity(file):
    os.chdir('C:\Users\dell\Desktop')
    try:
        fs = codecs.open(file, encoding='gbk')
        lines = fs.readlines()
        mysql = "insert into city values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        db = MySQLdb.connect('127.0.0.1', 'root', 'admin', 'pythondb', charset="utf8")
        cursor = db.cursor()
        for line in lines:
            line = line.strip('\r\n')
            items = string.split(line, '\t')
            cursor.execute(mysql, items)
            db.commit()
    except Exception, msg:
        print msg
    finally:
        fs.close()

def store(citylst):
    mysql = "insert into city values(%s, %s, %s, %s)"
    try:
        cnt = 0
        for city in citylst:
            city.output()
            ids.append(city.id)
            provinces.append(city.province)
            cnames.append(city.cname)
            clevels.append(city.clevel)
            # cnt+=1
            # if cnt>=100:
            #     break
        #print zip(ids,cnames)
        db = MySQLdb.connect('127.0.0.1', 'root', 'admin', 'pythondb',charset="utf8")
        cursor = db.cursor()
        params = zip(ids,provinces,cnames,clevels)
        i = 0
        while i<len(params):
            items = params[i:i+100]
            rtn = cursor.executemany(mysql, items)
            db.commit()
            if rtn >= 1:
                print 'insert %d records' % rtn
            i+=100
        # print params
        # rtn = cursor.executemany(mysql,params)
        # db.commit()
        # if rtn >= 1:
        #     print 'insert %d records' % rtn
        # for id,province,cname,clevel in zip(ids,provinces,cnames,clevels):
        #     rtn = cursor.execute(mysql, (id,province,cname,clevel))
        #     db.commit()
        #     if rtn == 1:
        #         print 'insert %d records' % rtn
        # for city in citylst:
        #     city.output()
        #     rtn = cursor.execute(mysql,(city.id, city.province, city.cname, city.clevel))
        #     db.commit()
        #     if rtn == 1:
        #         print 'insert %d records' % rtn
    except Exception,msg:
        print msg
        db.rollback()
    finally:
        print 'Finished database operate'

if __name__ == '__main__':
    # file = 'city.txt'
    # citylst = readfile(file)
    # store(citylst)
    storeCity('city.txt')
    # storeProvince('province.txt')
