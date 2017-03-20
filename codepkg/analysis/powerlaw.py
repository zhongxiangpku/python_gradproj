# encoding: UTF-8

import codecs
import math
import os
import sys

import MySQLdb

from codepkg import mod_config
import codepkg.data_process.geoutil

reload(sys)
sys.setdefaultencoding( "utf-8" )

def listCityNames():
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    mysql = 'select cname from city'
    cursor.execute(mysql)
    results = cursor.fetchall()
    return list(results)

coords = {}

def getCoords():
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    mysql = 'select cname, lat, lng from city'
    cursor.execute(mysql)
    results = cursor.fetchall()

    for row in results:
        lat = row[1]
        lng = row[2]
        coord = {}
        coord['lat'] = lat
        coord['lng'] = lng
        coords[row[0]] = coord

    mysql = 'select city, cname, lat, lng from spot'
    cursor.execute(mysql)
    results = cursor.fetchall()
    for row in results:
        lat = row[2]
        lng = row[3]
        coord = {}
        coord['lat'] = lat
        coord['lng'] = lng
        coords[row[0] + row[1]] = coord

    for key, value in coords.items():
        print key, value


def statisticGyrationFreq(file):
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    mysql = 'select gyration from user where gyration>0'
    cursor.execute(mysql)
    results = cursor.fetchall()

    incident = 10
    minGyration =  0
    results = list(results)
    maxGyration = max(results)
    maxGyration = maxGyration[0] + incident

    currentGyration = minGyration
    mymap = {}
    while currentGyration<maxGyration:
        index = currentGyration / incident
        mymap[index] = 0
        currentGyration += incident

    cnt = len(results)
    for row in results:
        key = int(row[0]/incident)
        mymap[key] = mymap[key] + 1

    fs = codecs.open(file, 'w+', encoding='utf8')
    fs.write("distance,frequency")
    for k,v in mymap.items():
        print k,v
        fs.write(str(k*10) + "," + str(v*1.0/cnt) + "\r\n")
    fs.flush()
    fs.close()

def statisticDistanceFreq(file):
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    mysql = 'select fromcity,toccity from citytravel where fromcity != toccity limit 0,1200000'
    cursor.execute(mysql)
    results = cursor.fetchall()

    getCoords()
    distances = []
    index = 1
    for row in results:
        departure = row[0]
        destination = row[1]
        if departure == destination:
            continue
        toponym1 = coords[departure]
        toponym2 = coords[destination]
        lat1 = toponym1['lat']
        lng1 = toponym1['lng']
        lat2 = toponym2['lat']
        lng2 = toponym2['lng']
        distance = codepkg.data_process.geoutil.getPointDistance(lat1, lng1, lat2, lng2)
        print index,departure,destination,distance
        index += 1
        distances.append(distance)

    incident = 50
    minGyration = 0
    maxGyration = max(distances)
    maxGyration = maxGyration + incident

    currentGyration = minGyration
    mymap = {}
    while currentGyration < maxGyration:
        index = currentGyration / incident
        mymap[index] = 0
        currentGyration += incident

    for dist in distances:
        key = int(dist / incident)
        mymap[key] = mymap[key] + 1

    cnt = len(distances)
    fs = codecs.open(file, 'w+', encoding='utf8')
    fs.write("distance,frequency")
    for k, v in mymap.items():
        print k, v
        if v>0:
            fs.write(str(k*incident) + "," + str(v * 1.0 /cnt) + "\r\n")
    fs.flush()
    fs.close()


pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
print pwd

gyrationvsFrequencyFile = pwd+'\\Datas\\gyrationvsfrequency.txt'
distancevsFrequencyFile = pwd+'\\Datas\\distancevsfrequency50.txt'
#statisticGyrationFreq(gyrationvsFrequencyFile)

statisticDistanceFreq(distancevsFrequencyFile)

