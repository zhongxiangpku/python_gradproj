# encoding: UTF-8

import codecs
import os
import string
import MySQLdb
import geoutil

from codepkg import mod_config

fromToMap = {}

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

def getCityUndirectEdgePairs(file):
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    # fs = codecs.open(file, 'w+',encoding='utf-8')
    try:
        mysql = 'select departure,city from citynote'
        cursor.execute(mysql)
        results = cursor.fetchall()
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
            distance = geoutil.getPointDistance(lat1, lng1, lat2, lng2)
            print departure, destination, distance
            if departure not in fromToMap.keys():
                fromToMap[departure] = {}
                fromToMap[departure][destination] = distance
            elif departure in fromToMap.keys():
                fromToMap[departure][destination] = distance

        count = 0
        avg_dist = 0.0
        for key, value in fromToMap.items():
            count = len(value.keys())
            for (k,v) in value.items():
                avg_dist += v
                # print key,k,v
            print key, str(count), str(avg_dist/count)
            #fs.write(key+","+str(value)+"\r\n")
            # print key,value
            #sum += value
        # fs.flush()
        # fs.close()
    except Exception, msg:
        print msg
    finally:
        db.close()

def getConnectionCountAndDistance(file):
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    fs = codecs.open(file, 'w+',encoding='utf-8')
    try:
        mysql = 'select departure,city from citynote limit 0,10000'
        cursor.execute(mysql)
        results = cursor.fetchall()
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
            distance = geoutil.getPointDistance(lat1, lng1, lat2, lng2)
            print departure, destination, distance
            if departure not in fromToMap.keys():
                fromToMap[departure] = {}
                if destination not in fromToMap[departure].keys():
                    fromToMap[departure][destination] = {}
                    fromToMap[departure][destination]['count'] = 1
                    fromToMap[departure][destination]['distance'] = distance
            elif departure in fromToMap.keys():
                if destination not in fromToMap[departure].keys():
                    fromToMap[departure][destination] = {}
                    fromToMap[departure][destination]['count'] = 1
                    fromToMap[departure][destination]['distance'] = distance
                elif destination in fromToMap[departure].keys():
                    fromToMap[departure][destination]['count'] += 1

        count = 0
        avg_dist = 0.0
        for key, value in fromToMap.items():
            count = len(value.keys())
            avg_dist = 0.0
            for (k,v) in value.items():
                c_count = v['count']
                c_distance = v['distance']
                count += c_count
                avg_dist += c_count * c_distance
                # print key,k,v
            print key, str(count), str(avg_dist/count)
            fs.write( key+";"+str(count)+";"+str(avg_dist/count)+"\r\n")
            # print key,value
            #sum += value
        fs.flush()
        fs.close()
    except Exception, msg:
        print msg
    finally:
        db.close()

pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
print pwd

mobileDistanceFile = pwd+'\\Datas\\mobileDistanceFile.txt'

getCoords()
# getCityUndirectEdgePairs('')
getConnectionCountAndDistance(mobileDistanceFile)