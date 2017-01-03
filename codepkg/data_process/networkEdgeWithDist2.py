# encoding: UTF-8

import codecs
import os
import string
import MySQLdb
import geoutil

from codepkg import mod_config

MAXROW = 300000
coords = {}
pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
print pwd
cityUndirectEdgeFile = pwd+'/Datas/undirectCityEdges_dist.txt'
cityDirectEdgeFile = pwd+'/Datas/directCityEdges_dist.txt'
spotUndirectEdgeFile = pwd+'/Datas/undirectSpotEdges_dist.txt'
spotDirectEdgeFile = pwd+'/Datas/directSpotEdges_dist.txt'

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
    # print len(coords)

#city undirect graph edge
undirectEdgeSet = set()
undirectEdgeMap = {}
def getCityUndirectEdgePairs(file):
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    fs = codecs.open(file, 'w+', encoding='utf-8')
    try:
        mysql = 'select departure,city from citynote'
        cursor.execute(mysql)
        results = cursor.fetchall()
        for row in results:
            departure = row[0]
            destination = row[1]
            pair1 = departure+","+destination
            pair2 = destination+","+departure
            if pair1 in undirectEdgeSet:
                undirectEdgeMap[pair1] += 1
            elif pair2 in undirectEdgeSet:
                undirectEdgeMap[pair2] += 1
            else:
                undirectEdgeMap[pair1] = 1
                undirectEdgeSet.add(pair1)
        sum = 0
        for key, value in undirectEdgeMap.items():
            pairs = key.strip('\r\n')
            items = string.split(pairs, ',')
            toponym1 = coords[items[0]]
            toponym2 = coords[items[1]]
            lat1 = toponym1['lat']
            lng1 = toponym1['lng']
            lat2 = toponym2['lat']
            lng2 = toponym2['lng']
            distance = geoutil.getPointDistance(lat1, lng1, lat2, lng2)
            weight = 0
            if distance>0:
                weight = value / distance
            print items[0], toponym1, items[1], toponym2, distance
            fs.write(key+","+str(value) + "," + str(distance) + ","+str(weight)+"\r\n")
            #print key,value
            sum += value
        fs.flush()
        fs.close()
        print len(undirectEdgeMap), sum
    except Exception, msg:
        print msg
    finally:
        db.close()

#city direct graph edge
directEdgeSet = set()
directEdgeMap = {}
def getCityDirectEdgePairs(file):
    #db = MySQLdb.connect('127.0.0.1', 'root', 'admin', 'pythondb', charset="gbk")
    print mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname, mod_config.dbcharset
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    fs = codecs.open(file, 'w+',encoding='utf-8')
    try:
        mysql = 'select departure,city from citynote'
        cursor.execute(mysql)
        results = cursor.fetchall()
        for row in results:
            departure = row[0]
            destination = row[1]
            pair = departure+","+destination
            #print pair
            if pair in directEdgeSet:
                directEdgeMap[pair]+=1
            else:
                directEdgeMap[pair]=1
                directEdgeSet.add(pair)
        sum = 0
        for key,value in directEdgeMap.items():
            pairs = key.strip('\r\n')
            items = string.split(pairs, ',')
            toponym1 = coords[items[0]]
            toponym2 = coords[items[1]]
            lat1 = toponym1['lat']
            lng1 = toponym1['lng']
            lat2 = toponym2['lat']
            lng2 = toponym2['lng']
            distance = geoutil.getPointDistance(lat1, lng1, lat2, lng2)
            weight = 0
            if distance > 0:
                weight = value / distance
            print items[0], toponym1, items[1], toponym2, distance
            fs.write(key + "," + str(value) + "," + str(distance) + "," + str(weight) + "\r\n")
            # fs.write(key+","+str(value)+"\r\n")
            #print key,value
            sum+=value
        fs.flush()
        fs.close()
        print len(directEdgeMap), sum
    except Exception, msg:
        print msg
    finally:
        db.close()

#spot undirect  graph edge
undirectCitySpotEdgeMap = {}
undirectSpotEdgeMap = {}

undirectSpot2SpotEdgeMapWithWeight = {}
undirectSpot2SpotEdgeMap = {}
def getSpotUndirectEdgePairs(file):
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname, charset=mod_config.dbcharset)#'222.29.117.151', 'root', 'admin', 'pythondb', charset='utf8')
    cursor = db.cursor()

    fs = codecs.open(file, 'w+', encoding='utf8')
    try:
        mysql = 'select departure,city,spot,url from note limit 0,'+ str(MAXROW)
        cursor.execute(mysql)
        results = cursor.fetchall()
        sqlindex = 1
        undirectCitySpotEdgeMapUrls = set()
        for row in results:
            departure = row[0]
            destination = row[1]
            spot = row[1] + row[2]
            url = row[3]
            pair1 = departure + "," + destination
            pair11 = departure + "," + destination +","+url
            print "sqlindex=", sqlindex, url, departure, destination, spot
            sqlindex += 1
            # departure city -> destination city
            # print pair1
            if pair1 in undirectCitySpotEdgeMap.keys():
                if pair11 not in undirectCitySpotEdgeMapUrls:
                    undirectCitySpotEdgeMap[pair1] += 1
            else:
                undirectCitySpotEdgeMap[pair1] = 1
                undirectCitySpotEdgeMapUrls.add(pair11)
                #undirectCitySpotEdgeSet.add(pair1)

            # destination city -> destination spot
            pair2 = destination+","+spot
            # print pair2
            if pair2 in undirectSpotEdgeMap.keys():
                undirectSpotEdgeMap[pair2] += 1
            else:
                undirectSpotEdgeMap[pair2] = 1
                #undirectSpotEdgeSet.add(pair2)

            # if url not in undirectSpot2SpotEdgeMap.keys():
            #     undirectSpot2SpotEdgeMap[url] = set()
            #     undirectSpot2SpotEdgeMap[url].add(spot)
            # else:
            #     undirectSpot2SpotEdgeMap[url].add(spot)
            if url not in undirectSpot2SpotEdgeMap.keys():
                undirectSpot2SpotEdgeMap[url] = {}
                if destination not in undirectSpot2SpotEdgeMap[url].keys():
                    undirectSpot2SpotEdgeMap[url][destination] = set()
                    undirectSpot2SpotEdgeMap[url][destination].add(spot)
            else:
                if destination not in undirectSpot2SpotEdgeMap[url].keys():
                    undirectSpot2SpotEdgeMap[url][destination] = set()
                    undirectSpot2SpotEdgeMap[url][destination].add(spot)
                else:
                    undirectSpot2SpotEdgeMap[url][destination].add(spot)

        spotindex = 1
        for key, value in undirectSpot2SpotEdgeMap.items():
            spotSet = ()
            spotKey = ''
            for (k, v) in value.items():
                spotKey = k
                spotSet = v
            lstValue = list(spotSet)
            print "spotindex=", spotindex, key, spotKey
            spotindex += 1
            for i in range(0,len(lstValue)):
                for j in range(i+1,len(lstValue)):
                    pair31 = lstValue[i]+ "," +lstValue[j]
                    pair32 = lstValue[j] + "," + lstValue[i]
                    #print pair31, pair32
                    if pair31 in undirectSpot2SpotEdgeMapWithWeight.keys():
                        undirectSpot2SpotEdgeMapWithWeight[pair31]+=1
                    elif pair32 in undirectSpot2SpotEdgeMapWithWeight.keys():
                        undirectSpot2SpotEdgeMapWithWeight[pair32] += 1
                    else:
                        undirectSpot2SpotEdgeMapWithWeight[pair31] = 1

        sum = 0
        for key, value in undirectCitySpotEdgeMap.items():
            # key2 = key.rfind(',')
            # key = key[0:key2]
            pairs = key.strip('\r\n')
            items = string.split(pairs, ',')
            toponym1 = coords[items[0]]
            toponym2 = coords[items[1]]
            lat1 = toponym1['lat']
            lng1 = toponym1['lng']
            lat2 = toponym2['lat']
            lng2 = toponym2['lng']
            distance = geoutil.getPointDistance(lat1, lng1, lat2, lng2)
            weight = 0
            if distance > 0:
                weight = value / distance
            print items[0], toponym1, items[1], toponym2, distance
            fs.write(key + "," + str(value) + "," + str(distance) + "," + str(weight) + "\r\n")

            #print key
            #fs.write(key + "," + str(value) + "\r\n")
            print key, value
            sum += value

        for key, value in undirectSpotEdgeMap.items():
            print key, value
            pairs = key.strip('\r\n')
            items = string.split(pairs, ',')
            toponym1 = coords.get(items[0])
            toponym2 = coords.get(items[1])
            if toponym1 is None:
                print items[0],'is None'
            elif toponym2 is None:
                print items[1], 'is None'
            if toponym1 is not None and toponym2 is not None:
                lat1 = toponym1.get('lat')
                lng1 = toponym1.get('lng')
                lat2 = toponym2.get('lat')
                lng2 = toponym2.get('lng')
                print items[0], items[1]
                distance = geoutil.getPointDistance(lat1, lng1, lat2, lng2)
                weight = 0
                if distance > 0:
                    weight = value / distance
                print items[0], toponym1, items[1], toponym2, distance
                fs.write(key + "," + str(value) + "," + str(distance) + "," + str(weight) + "\r\n")
                # fs.write(key + "," + str(value) + "\r\n")
                # print key, value
                sum += value

        for key, value in undirectSpot2SpotEdgeMapWithWeight.items():
            pairs = key.strip('\r\n')
            items = string.split(pairs, ',')
            toponym1 = coords[items[0]]
            toponym2 = coords[items[1]]
            lat1 = toponym1['lat']
            lng1 = toponym1['lng']
            lat2 = toponym2['lat']
            lng2 = toponym2['lng']
            distance = geoutil.getPointDistance(lat1, lng1, lat2, lng2)
            weight = 0
            if distance > 0:
                weight = value / distance
            print items[0], toponym1, items[1], toponym2, distance
            fs.write(key + "," + str(value) + "," + str(distance) + "," + str(weight) + "\r\n")
            # fs.write(key + "," + str(value) + "\r\n")
            # print key, value
            sum += value
        fs.flush()
        fs.close()
        print len(undirectCitySpotEdgeMap) + len(undirectSpotEdgeMap) + len(undirectSpot2SpotEdgeMapWithWeight), sum
    except Exception, msg:
        print 'error:', msg
    finally:
        db.close()

#spot direct  graph edge
directCitySpotEdgeMap = {}
directSpotEdgeMap = {}

directSpot2SpotEdgeMapWithWeight = {}
directSpot2SpotEdgeMap = {}
def getSpotDirectEdgePairs(file):
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname, charset=mod_config.dbcharset)#'222.29.117.151', 'root', 'admin', 'pythondb', charset='utf8')
    cursor = db.cursor()

    fs = codecs.open(file, 'w+', encoding='utf8')
    try:
        mysql = 'select departure,city,spot,url from note limit 0,'+ str(MAXROW)
        cursor.execute(mysql)
        results = cursor.fetchall()
        sqlindex = 1
        directCitySpotEdgeMapUrls = set()
        for row in results:
            departure = row[0]
            destination = row[1]
            spot = row[1] + row[2]
            url = row[3]
            print "sqlindex=", sqlindex, url, departure, destination, spot
            sqlindex += 1
            pair1 = departure + "," + destination
            pair11 = departure + "," + destination+","+url
            # departure city -> destination city
            # print pair1
            if pair1 in directCitySpotEdgeMap.keys():
                if pair11 not in directCitySpotEdgeMapUrls:
                    directCitySpotEdgeMap[pair1] += 1
            else:
                directCitySpotEdgeMap[pair1] = 1
                directCitySpotEdgeMapUrls.add(pair11)

            # destination city -> destination spot
            pair21 = destination+","+spot
            pair22 = spot + "," + destination
            # print pair2
            if pair21 in directSpotEdgeMap.keys():
                directSpotEdgeMap[pair21] += 1
                directSpotEdgeMap[pair22] += 1
            else:
                directSpotEdgeMap[pair21] = 1
                directSpotEdgeMap[pair22] = 1

            if url not in directSpot2SpotEdgeMap.keys():
                directSpot2SpotEdgeMap[url] = {}
                if destination not in directSpot2SpotEdgeMap[url].keys():
                    directSpot2SpotEdgeMap[url][destination] = set()
                    directSpot2SpotEdgeMap[url][destination].add(spot)
            else:
                if destination not in directSpot2SpotEdgeMap[url].keys():
                    directSpot2SpotEdgeMap[url][destination] = set()
                    directSpot2SpotEdgeMap[url][destination].add(spot)
                else:
                    directSpot2SpotEdgeMap[url][destination].add(spot)

        spotindex = 1
        for key, value in directSpot2SpotEdgeMap.items():
            spotSet = ()
            spotKey = ''
            for (k, v) in value.items():
                spotKey = k
                spotSet = v
            lstValue = list(spotSet)
            print "spotindex=", spotindex, key, spotKey
            spotindex += 1
            for i in range(0, len(lstValue)):
                for j in range(i+1, len(lstValue)):
                    pair31 = lstValue[i] + "," +lstValue[j]
                    pair32 = lstValue[j] + "," + lstValue[i]
                    #print pair31, pair32
                    if pair31 in directSpot2SpotEdgeMapWithWeight.keys():
                        directSpot2SpotEdgeMapWithWeight[pair31]+=1
                        directSpot2SpotEdgeMapWithWeight[pair32] += 1
                    elif pair32 in directSpot2SpotEdgeMapWithWeight.keys():
                        directSpot2SpotEdgeMapWithWeight[pair31] += 1
                        directSpot2SpotEdgeMapWithWeight[pair32] += 1
                    else:
                        directSpot2SpotEdgeMapWithWeight[pair31] = 1
                        directSpot2SpotEdgeMapWithWeight[pair32] = 1


        dataindex = 1
        sum = 0
        for key, value in directCitySpotEdgeMap.items():
            print 'dataindex=', dataindex, key, value
            dataindex += 1
            # key2 = key.rfind(',')
            # key = key[0:key2]
            pairs = key.strip('\r\n')
            items = string.split(pairs, ',')
            toponym1 = coords[items[0]]
            toponym2 = coords[items[1]]
            lat1 = toponym1['lat']
            lng1 = toponym1['lng']
            lat2 = toponym2['lat']
            lng2 = toponym2['lng']
            distance = geoutil.getPointDistance(lat1, lng1, lat2, lng2)
            weight = 0
            if distance > 0:
                weight = value / distance
            print items[0], toponym1, items[1], toponym2, distance
            fs.write(key + "," + str(value) + "," + str(distance) + "," + str(weight) + "\r\n")
            #print key
            #fs.write(key + "," + str(value) + "\r\n")
            # print key, value
            sum += value

        for key, value in directSpotEdgeMap.items():
            print 'dataindex=', dataindex, key, value
            dataindex += 1
            pairs = key.strip('\r\n')
            items = string.split(pairs, ',')
            toponym1 = coords.get(items[0])
            toponym2 = coords.get(items[1])
            if toponym1 is None:
                print items[0], 'is None'
            elif toponym2 is None:
                print items[1], 'is None'
            if toponym1 is not None and toponym2 is not None:
                lat1 = toponym1.get('lat')
                lng1 = toponym1.get('lng')
                lat2 = toponym2.get('lat')
                lng2 = toponym2.get('lng')
                print items[0], items[1]
                distance = geoutil.getPointDistance(lat1, lng1, lat2, lng2)
                weight = 0
                if distance > 0:
                    weight = value / distance
                print items[0], toponym1, items[1], toponym2, distance
                fs.write(key + "," + str(value) + "," + str(distance) + "," + str(weight) + "\r\n")
            # fs.write(key + "," + str(value) + "\r\n")
            # print key, value
            sum += value

        for key, value in directSpot2SpotEdgeMapWithWeight.items():
            print 'dataindex=', dataindex, key, value
            dataindex += 1
            pairs = key.strip('\r\n')
            items = string.split(pairs, ',')
            toponym1 = coords[items[0]]
            toponym2 = coords[items[1]]
            lat1 = toponym1['lat']
            lng1 = toponym1['lng']
            lat2 = toponym2['lat']
            lng2 = toponym2['lng']
            distance = geoutil.getPointDistance(lat1, lng1, lat2, lng2)
            weight = 0
            if distance > 0:
                weight = value / distance
            print items[0], toponym1, items[1], toponym2, distance
            fs.write(key + "," + str(value) + "," + str(distance) + "," + str(weight) + "\r\n")
            # fs.write(key + "," + str(value) + "\r\n")
            # print key, value
            sum += value
        fs.flush()
        fs.close()
        print len(directCitySpotEdgeMap), len(directSpotEdgeMap), len(directSpot2SpotEdgeMapWithWeight), len(directCitySpotEdgeMap) + len(directSpotEdgeMap) + len(directSpot2SpotEdgeMapWithWeight), sum
    except Exception, msg:
        print msg
    finally:
        db.close()


getCoords()
# getCityUndirectEdgePairs(cityUndirectEdgeFile)
# getCityDirectEdgePairs(cityDirectEdgeFile)
# getSpotUndirectEdgePairs(spotUndirectEdgeFile)
getSpotDirectEdgePairs(spotDirectEdgeFile)

