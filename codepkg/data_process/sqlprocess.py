import codecs
import os
import string

import MySQLdb

from codepkg import mod_config


def readfile(file):
    os.chdir('C:\Users\dell\Desktop')
    fs = codecs.open(file, encoding='gbk')
    lines = fs.readlines()
    fs.close()
    try:
        for line in lines:
            line = line.strip('\r\n')
            items = string.split(line, ',')
            mysql = "update citynote set departure ='"+items[1]+"' where departure ='"+items[0]+ "';"
            print mysql
    except Exception, e:
        print Exception, ":", e

#city undirect graph edge
undirectEdgeSet = set()
undirectEdgeMap = {}
def getCityUndirectEdgePairs(file):
    # db = MySQLdb.connect('127.0.0.1', 'root', 'admin', 'pythondb', charset="gbk")
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
            pair1 = departure+","+destination
            pair2 = destination+","+departure
            #print pair1,pair2
            if pair1 in undirectEdgeSet:
                undirectEdgeMap[pair1] += 1
            elif pair2 in undirectEdgeSet:
                undirectEdgeMap[pair2] += 1
            else:
                undirectEdgeMap[pair1] = 1
                undirectEdgeSet.add(pair1)
        sum = 0
        for key, value in undirectEdgeMap.items():
            fs.write(key+","+str(value)+"\r\n")
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
            fs.write(key+","+str(value)+"\r\n")
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
#undirectCitySpotEdgeSet = set()
undirectCitySpotEdgeMap = {}

#undirectSpotEdgeSet = set()
undirectSpotEdgeMap = {}

undirectSpot2SpotEdgeMapWithWeight = {}
undirectSpot2SpotEdgeMap = {}
def getSpotUndirectEdgePairs(file):
    # print mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname, mod_config.dbcharset
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname, charset=mod_config.dbcharset)#'222.29.117.151', 'root', 'admin', 'pythondb', charset='utf8')
    cursor = db.cursor()

    fs = codecs.open(file, 'w+', encoding='utf8')
    try:
        mysql = 'select departure,city,spot,url from note limit 0,10000'
        cursor.execute(mysql)
        results = cursor.fetchall()
        for row in results:
            departure = row[0]
            destination = row[1]
            spot = row[1]+row[2]
            url = row[3]
            pair1 = departure + "," + destination+","+url
            # departure city -> destination city
            # print pair1
            if pair1 in undirectCitySpotEdgeMap.keys():
                undirectCitySpotEdgeMap[pair1] += 1
            else:
                undirectCitySpotEdgeMap[pair1] = 1
                #undirectCitySpotEdgeSet.add(pair1)

            # destination city -> destination spot
            pair2 = destination+","+spot
            # print pair2
            if pair2 in undirectSpotEdgeMap.keys():
                undirectSpotEdgeMap[pair2] += 1
            else:
                undirectSpotEdgeMap[pair2] = 1
                #undirectSpotEdgeSet.add(pair2)

            if url not in undirectSpot2SpotEdgeMap.keys():
                undirectSpot2SpotEdgeMap[url] = set()
                undirectSpot2SpotEdgeMap[url].add(spot)
            else:
                undirectSpot2SpotEdgeMap[url].add(spot)

        for key, value in undirectSpot2SpotEdgeMap.items():
            if len(value) > 1:
                lstValue = list(value)
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

        # index = 1
        # for key, value in undirectSpot2SpotEdgeMapWithWeight.items():
        #     print index, key, value
        #     index += 1

        sum = 0
        for key, value in undirectCitySpotEdgeMap.items():
            key2 = key.rfind(',')
            key = key[0:key2]
            #print key
            fs.write(key + "," + str(value) + "\r\n")
            print key, value
            sum += value

        for key, value in undirectSpotEdgeMap.items():
            fs.write(key + "," + str(value) + "\r\n")
            print key, value
            sum += value

        for key, value in undirectSpot2SpotEdgeMapWithWeight.items():
            fs.write(key + "," + str(value) + "\r\n")
            print key, value
            sum += value
        fs.flush()
        fs.close()
        print len(undirectCitySpotEdgeMap) + len(undirectSpotEdgeMap) + len(undirectSpot2SpotEdgeMapWithWeight), sum
    except Exception, msg:
        print msg
    finally:
        db.close()






#spot direct  graph edge
directCitySpotEdgeMap = {}
directSpotEdgeMap = {}

directSpot2SpotEdgeMapWithWeight = {}
directSpot2SpotEdgeMap = {}
def getSpotdirectEdgePairs(file):
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname, charset=mod_config.dbcharset)#'222.29.117.151', 'root', 'admin', 'pythondb', charset='utf8')
    cursor = db.cursor()

    fs = codecs.open(file, 'w+', encoding='utf8')
    try:
        mysql = 'select departure,city,spot,url from note limit 0, 10000 '
        cursor.execute(mysql)
        results = cursor.fetchall()
        sqlindex = 1
        for row in results:
            departure = row[0]
            destination = row[1]
            spot = row[1] + row[2]
            url = row[3]
            print "sqlindex=", sqlindex, url, departure, destination, spot
            sqlindex += 1
            pair1 = departure + "," + destination+","+url
            # departure city -> destination city
            # print pair1
            if pair1 in directCitySpotEdgeMap.keys():
                directCitySpotEdgeMap[pair1] += 1
            else:
                directCitySpotEdgeMap[pair1] = 1
                #undirectCitySpotEdgeSet.add(pair1)

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
                directSpot2SpotEdgeMap[url] = set()
                directSpot2SpotEdgeMap[url].add(spot)
            else:
                directSpot2SpotEdgeMap[url].add(spot)

        spotindex = 1
        for key, value in directSpot2SpotEdgeMap.items():
            print 'spotindex=', spotindex, key
            spotindex += 1
            if len(value) > 1:
                lstValue = list(value)
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


        # index = 1
        # for key, value in undirectSpot2SpotEdgeMapWithWeight.items():
        #     print index, key, value
        #     index += 1

        dataindex = 1
        sum = 0
        for key, value in directCitySpotEdgeMap.items():
            print 'dataindex=', dataindex, key, value
            dataindex += 1
            key2 = key.rfind(',')
            key = key[0:key2]
            #print key
            fs.write(key + "," + str(value) + "\r\n")
            # print key, value
            sum += value

        for key, value in directSpotEdgeMap.items():
            print 'dataindex=', dataindex, key, value
            dataindex += 1
            fs.write(key + "," + str(value) + "\r\n")
            # print key, value
            sum += value

        for key, value in directSpot2SpotEdgeMapWithWeight.items():
            print 'dataindex=', dataindex, key, value
            dataindex += 1
            fs.write(key + "," + str(value) + "\r\n")
            # print key, value
            sum += value
        fs.flush()
        fs.close()
        print len(directCitySpotEdgeMap), len(directSpotEdgeMap), len(directSpot2SpotEdgeMapWithWeight), len(directCitySpotEdgeMap) + len(directSpotEdgeMap) + len(directSpot2SpotEdgeMapWithWeight), sum
    except Exception, msg:
        print msg
    finally:
        db.close()

# file = 'errorcityname2.csv'
# readfile(file)


pwd = os.getcwd()
print pwd
cityUndirectEdgeFile = pwd+'/Datas/undirectCityEdges.txt'
cityDirectEdgeFile = pwd+'/Datas/directCityEdges.txt'
spotUndirectEdgeFile = pwd+'\\Datas\\undirectSpotEdges2.txt'
spotDirectEdgeFile = pwd+'\\Datas\\directSpotEdges2.txt'

# getCityUndirectEdgePairs(cityUndirectEdgeFile)
# getCityDirectEdgePairs(cityDirectEdgeFile)
getSpotUndirectEdgePairs(spotUndirectEdgeFile)
getSpotdirectEdgePairs(spotDirectEdgeFile)