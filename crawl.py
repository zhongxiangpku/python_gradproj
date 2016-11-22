#!/usr/bin/python
# encoding: UTF-8

import os
import MySQLdb
from bs4 import BeautifulSoup
import urllib
import urllib2
import json
import time
import pinyin
import string
import mod_config

BASE_URL = "http://lvyou.baidu.com/destination/ajax/jingdian?format=ajax&surl="

def getSpotsCount(url):
    req = urllib2.Request(url)
    #print req
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    #print res
    respJson = json.loads(res)
    count = respJson["data"]["scene_total"]
    return count

def getSpots(url,city):
    try:
        mysql = "insert into spot(ename,cname,city,lat,lng,formataddress,status,finish,createtime,updatetime) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname, mod_config.dbcharset)
        cursor = db.cursor()

        req = urllib2.Request(url)
        # print req
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        # print res
        respJson = json.loads(res)
        datas = respJson['data']["scene_list"]
        for spot in datas:
            #spotJson = json.loads(spot)
            now = int(time.time())
            timeArray = time.localtime(now)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            print otherStyleTime
            ename = spot['surl']
            sname = spot['sname']
            mapinfo = string.strip(spot['ext']['map_info'])
            address = string.strip(spot['ext']['address'])
            address = string.strip(address[0:200])
            lng = 0.0
            lat = 0.0
            if ',' in mapinfo:
                coords = string.split(mapinfo,',')
                if len(coords) == 2:
                    lng = float(coords[0])
                    lat = float(coords[1])
                    if lat>100:
                        temp = lat
                        lat = lng
                        lng = temp
            print address,mapinfo
            #ename = pinyin.get_pinyin(sname)
            cursor.execute(mysql,(ename, sname, city, lat,lng,address,1,0,otherStyleTime,otherStyleTime))
            db.commit()
    except Exception,msg:
        db.rollback()
        print msg


def crawlSpot():
    try:
        mysql = 'select * from city where finish = 0'
        db = MySQLdb.connect(mod_config.dbhost,
                             mod_config.dbuser,
                             mod_config.dbpassword,
                             mod_config.dbname,
                             mod_config.dbcharset)
        cursor = db.cursor()
        cursor.execute(mysql)
        results = cursor.fetchall()
        for row in results:
            params = '&pn=1&rn=10'
            url = BASE_URL+row[1]+params
            print row[2],'\t',url
            count = getSpotsCount(url)

            perpage = 10
            pages = (count + perpage - 1) / perpage
            i = 1
            while i<=pages:
                params = "&pn="+str(i)+"&rn="+str(perpage)
                url = BASE_URL+row[1]+params
                getSpots(url,row[2])
                i+=1
            mysql2='update city set finish =1 where id = %s' % row[0]
            cursor.execute(mysql2)
            db.commit()
    except Exception,msg:
        print msg
    finally:
        pass

def getNote(city,cname,ename,maxcount):
    try:
        mysql = "insert into note(nid,title,url,postime,status,finish,source,spot,city,abs,departure,destinations,path,places,viewcount,favoritecount,recommendcount,createtime,updatetime) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        db = MySQLdb.connect(mod_config.dbhost,
                             mod_config.dbuser,
                             mod_config.dbpassword,
                             mod_config.dbname,
                             mod_config.dbcharset)


        cursor = db.cursor()
        i = 0
        index = 0
        while i<maxcount:
            currentURL = "https://lvyou.baidu.com/search/ajax/search?format=ajax&word=" + cname + "&surl=" + ename + "&pn=" + str(i)+ "&rn=10&t=" +str(time.time())
            currentURL = currentURL.encode("utf8")
            req = urllib2.Request(currentURL)
            res_data = urllib2.urlopen(req)
            res = res_data.read()
            # print res
            respJson = json.loads(res)
            if respJson['errno'] == 0:
                notes_list = respJson['data']['search_res']['notes_list']
                print respJson['data']['search_res']
                if notes_list is None or len(notes_list) <= 1:
                    break
                for note in notes_list:
                    nid = ''
                    recommend_count=0
                    favorite_count=0
                    view_count=0
                    publish_time =0
                    title=''
                    departure=''
                    places=''
                    destinations=''
                    path=''
                    loc=''
                    abstracts=''

                    nid = note['nid']
                    recommend_count = note['recommend_count']
                    view_count = note['view_count']
                    favorite_count = note['favorite_count']

                    publish_time = note['publish_time']
                    ltime = time.localtime(float(publish_time))
                    postime = time.strftime("%Y-%m-%d %H:%M:%S", ltime)

                    title = note['title']
                    departure = note['departure']
                    places = note['places']
                    destinations = note['destinations']
                    path = note['path']
                    loc = note['loc']
                    abstracts = note['content']

                    now = int(time.time())
                    timeArray = time.localtime(now)
                    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

                    destinationStrs = string.join(destinations, '-')
                    pathStrs = string.join(path, '-')
                    placeStrs = string.join(places, '-')

                    print 'index=%d' % index, nid, recommend_count, view_count, favorite_count, postime, title, departure, placeStrs, destinationStrs, pathStrs, loc, abstracts

                    cursor.execute(mysql,(nid,title,loc,postime,1,0,'百度',cname,city,abstracts,departure,destinationStrs,pathStrs,placeStrs,view_count,favorite_count,recommend_count,otherStyleTime,otherStyleTime))
                    db.commit()
                    index+=1
            i+=10
    except Exception,msg:
        db.rollback()
        print msg

def crawlNotes():
    try:
        mysql = 'select * from spot where finish = 0'
        db = MySQLdb.connect(mod_config.dbhost,
                             mod_config.dbuser,
                             mod_config.dbpassword,
                             mod_config.dbname,
                             mod_config.dbcharset)
        cursor = db.cursor()
        cursor.execute(mysql)
        results = cursor.fetchall()
        index = 1
        for row in results:
            print str(index),row[2],row[1],row[3]
            getNote(row[3],row[2],row[1],5000)
            mysql2 = 'update spot set finish = 1 where id = %s' % row[0]
            cursor.execute(mysql2)
            db.commit()
            index+=1
    except Exception,msg:
        #db.rollback()
        print msg


def getCNote(city,cname,ename,maxcount):
    try:
        mysql = "insert into citynote(nid,title,url,postime,status,finish,source,spot,city,abs,departure,destinations,path,places,viewcount,favoritecount,recommendcount,createtime,updatetime) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        db = MySQLdb.connect('localhost', 'root', 'admin', 'pythondb', charset='utf8')
        cursor = db.cursor()
        i = 0
        index = 0
        while i<maxcount:
            currentURL = "https://lvyou.baidu.com/search/ajax/search?format=ajax&word=" + cname + "&surl=" + ename + "&pn=" + str(i)+ "&rn=10&t=" +str(time.time())
            currentURL = currentURL.encode("utf8")
            req = urllib2.Request(currentURL)
            res_data = urllib2.urlopen(req)
            res = res_data.read()
            # print res
            respJson = json.loads(res)
            if respJson['errno'] == 0:
                notes_list = respJson['data']['search_res']['notes_list']
                print respJson['data']['search_res']
                if notes_list is None or len(notes_list) <= 1:
                    break
                for note in notes_list:
                    nid = ''
                    recommend_count=0
                    favorite_count=0
                    view_count=0
                    publish_time =0
                    title=''
                    departure=''
                    places=''
                    destinations=''
                    path=''
                    loc=''
                    abstracts=''

                    nid = note['nid']
                    recommend_count = note['recommend_count']
                    view_count = note['view_count']
                    favorite_count = note['favorite_count']

                    publish_time = note['publish_time']
                    ltime = time.localtime(float(publish_time))
                    postime = time.strftime("%Y-%m-%d %H:%M:%S", ltime)

                    title = note['title']
                    departure = note['departure']
                    places = note['places']
                    destinations = note['destinations']
                    path = note['path']
                    loc = note['loc']
                    abstracts = note['content']

                    now = int(time.time())
                    timeArray = time.localtime(now)
                    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

                    destinationStrs = string.join(destinations, '-')
                    pathStrs = string.join(path, '-')
                    placeStrs = string.join(places, '-')

                    print 'index=%d' % index, nid, departure, city, cname, loc
                    startend = departure+city+loc
                    if startend not in myset:
                        cursor.execute(mysql,(nid,title,loc,postime,1,0,'百度',cname,city,abstracts,departure,destinationStrs,pathStrs,placeStrs,view_count,favorite_count,recommend_count,otherStyleTime,otherStyleTime))
                        db.commit()
                        index+=1
                        myset.add(startend)
            i+=10
    except Exception,msg:
        db.rollback()
        print msg

def crawlCNotes():
    try:
        mysql = 'select * from spot where finish = 0'
        db = MySQLdb.connect('localhost', 'root', 'admin', 'pythondb', charset='utf8')
        cursor = db.cursor()
        cursor.execute(mysql)
        results = cursor.fetchall()
        index = 1
        for row in results:
            print str(index),row[2],row[1],row[3]
            getCNote(row[3],row[2],row[1],5000)
            mysql2 = 'update spot set finish = 1 where id = %s' % row[0]
            cursor.execute(mysql2)
            db.commit()
            index+=1
    except Exception,msg:
        #db.rollback()
        print msg


def getUNote(city,cname,ename,maxcount):
    try:
        mysql = "insert into unote(nid,title,url,postime,status,finish,source,spot,city,abs,departure,destinations,path,places,viewcount,favoritecount,recommendcount,createtime,updatetime) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        db = MySQLdb.connect('localhost', 'root', 'admin', 'pythondb', charset='utf8')
        cursor = db.cursor()
        i = 0
        index = 0
        while i<maxcount:
            currentURL = "https://lvyou.baidu.com/search/ajax/search?format=ajax&word=" + cname + "&surl=" + ename + "&pn=" + str(i)+ "&rn=10&t=" +str(time.time())
            currentURL = currentURL.encode("utf8")
            req = urllib2.Request(currentURL)
            res_data = urllib2.urlopen(req)
            res = res_data.read()
            # print res
            respJson = json.loads(res)
            if respJson['errno'] == 0:
                notes_list = respJson['data']['search_res']['notes_list']
                print respJson['data']['search_res']
                if notes_list is None or len(notes_list) <= 1:
                    break
                for note in notes_list:
                    nid = ''
                    recommend_count=0
                    favorite_count=0
                    view_count=0
                    publish_time =0
                    title=''
                    departure=''
                    places=''
                    destinations=''
                    path=''
                    loc=''
                    abstracts=''

                    nid = note['nid']
                    recommend_count = note['recommend_count']
                    view_count = note['view_count']
                    favorite_count = note['favorite_count']

                    publish_time = note['publish_time']
                    ltime = time.localtime(float(publish_time))
                    postime = time.strftime("%Y-%m-%d %H:%M:%S", ltime)

                    title = note['title']
                    departure = note['departure']
                    places = note['places']
                    destinations = note['destinations']
                    path = note['path']
                    loc = note['loc']
                    abstracts = note['content']

                    now = int(time.time())
                    timeArray = time.localtime(now)
                    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

                    destinationStrs = string.join(destinations, '-')
                    pathStrs = string.join(path, '-')
                    placeStrs = string.join(places, '-')

                    print 'index=%d' % index, nid, departure, city, cname, loc
                    if loc not in urlset:
                        cursor.execute(mysql,(nid,title,loc,postime,1,0,'百度',cname,city,abstracts,departure,destinationStrs,pathStrs,placeStrs,view_count,favorite_count,recommend_count,otherStyleTime,otherStyleTime))
                        db.commit()
                        index+=1
                        urlset.add(loc)
                    index += 1
            i+=10
    except Exception,msg:
        db.rollback()
        print msg

def crawlUNotes():
    try:
        mysql = 'select * from spot where finish = 0'
        db = MySQLdb.connect('localhost', 'root', 'admin', 'pythondb', charset='utf8')
        cursor = db.cursor()
        cursor.execute(mysql)
        results = cursor.fetchall()
        index = 1
        for row in results:
            print str(index),row[2],row[1],row[3]
            getUNote(row[3],row[2],row[1],5000)
            mysql2 = 'update spot set finish = 1 where id = %s' % row[0]
            cursor.execute(mysql2)
            db.commit()
            index+=1
    except Exception,msg:
        #db.rollback()
        print msg

myset = set()

urlset = set()
if __name__ == '__main__':
    # crawlSpot()
    # crawlNotes()
    # crawlCNotes()
    crawlUNotes()