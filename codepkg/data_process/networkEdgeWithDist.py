import codecs
import os
import string
import MySQLdb
import geoutil

from codepkg import mod_config

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

pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
print pwd
cityUndirectEdgeFile = pwd+'/Datas/undirectCityEdges_dist.txt'

getCoords()
getCityUndirectEdgePairs(cityUndirectEdgeFile)

