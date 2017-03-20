# encoding: UTF-8
import codecs
import os
import sys
import codepkg.data_process.geoutil as geoutil
import MySQLdb

from codepkg import mod_config
import time
reload(sys)
sys.setdefaultencoding( "utf-8" )


def chrodMapData():
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    citylist = ['北京', '上海', '广州', '成都',
    '杭州', '深圳', '西安', '武汉',
    '天津', '南京', '苏州', '重庆',
    '青岛', '沈阳', '郑州', '长沙',
    '厦门', '济南', '大连', '嘉兴']

    mymap = {}
    for city in citylist:
        mymap[city] = 0

    for city in citylist:

        mysql = 'select fromcity,toccity,count(*) from citytravel where fromcity != toccity and fromcity = "'+city+'"group by fromcity,toccity order by count(*) desc limit 0,20'
        cursor.execute(mysql)
        results = cursor.fetchall()
        for row in results:
            toccity = str(row[1])
            if toccity in citylist:
                mymap[toccity] = row[2]

        #print mymap
        mystr = 'c('
        for city in citylist:
            #print city,mymap[city]
            mystr += str(mymap[city])+','
        print mystr[0:len(mystr)-1]+"),"

        values = mymap.values()
        for city in citylist:
            mymap[city] = 0

def fun2():
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    mysql = 'select uid,fromcity,toccity from citytravel'
    cursor.execute(mysql)
    results = cursor.fetchall()
    userSet = set()

    inflowMap = {}
    outflowMap = {}
    for row in results:
        uid = str(row[0])
        fromcity = str(row[1])
        toccity = str(row[2])
        if uid in userSet:
            continue
        userSet.add(uid)

pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
print pwd


chrodMapData()
