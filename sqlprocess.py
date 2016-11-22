import os
import MySQLdb
import codecs
import string

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
    except Exception,e:
        print Exception,":",e

def getCityUndirectEdgePairs(file):
    db = MySQLdb.connect('127.0.0.1', 'root', 'admin', 'pythondb', charset="gbk")
    cursor = db.cursor()
    fs = codecs.open(file, 'w+',encoding='gbk')
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
                undirectEdgeMap[pair1]+=1
            elif pair2 in undirectEdgeSet:
                undirectEdgeMap[pair2] += 1
            else:
                undirectEdgeMap[pair1]=1
                undirectEdgeSet.add(pair1)
        sum = 0
        for key,value in undirectEdgeMap.items():
            fs.write(key+","+str(value)+"\r\n")
            #print key,value
            sum+=value
        fs.flush()
        fs.close()
        print len(undirectEdgeMap),sum
    except Exception, msg:
        print msg
    finally:
        db.close()

def getCityDirectEdgePairs(file):
    db = MySQLdb.connect('127.0.0.1', 'root', 'admin', 'pythondb', charset="gbk")
    cursor = db.cursor()
    fs = codecs.open(file, 'w+',encoding='gbk')
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
        print len(directEdgeMap),sum
    except Exception, msg:
        print msg
    finally:
        db.close()

def getSpotUndirectEdgePairs(file):
    db = MySQLdb.connect('127.0.0.1', 'root', 'admin', 'pythondb', charset="gbk")
    cursor = db.cursor()
    fs = codecs.open(file, 'w+', encoding='gbk')
    try:
        mysql = 'select departure,city,spot,url from note'
        cursor.execute(mysql)
        results = cursor.fetchall()
        for row in results:
            departure = row[0]
            destination = row[1]
            spot = row[2]
            url = row[3]
            pair1 = departure + "," + destination+","+url
            print pair1
            if pair1 in undirectSpotEdgeSet:
                undirectSpotEdgeMap[pair1] += 1
            else:
                undirectSpotEdgeMap[pair1] = 1
                undirectSpotEdgeSet.add(pair1)

            pair2 = destination+","+spot
            if pair2 in undirectCitySpotEdgeSet:
                undirectCitySpotEdgeMap[pair2]+=1
            else:
                undirectCitySpotEdgeMap[pair2] = 1
                undirectCitySpotEdgeSet.add(pair2)
        sum = 0
        for key, value in undirectSpotEdgeMap.items():
            fs.write(key + "," + str(value) + "\r\n")
            print key,value
            sum += value
        fs.flush()
        fs.close()
        print len(undirectSpotEdgeMap), sum
    except Exception, msg:
        print msg
    finally:
        db.close()


#city graph edge
undirectEdgeSet = set()
undirectEdgeMap = {}
directEdgeSet = set()
directEdgeMap = {}

#spot graph edge
undirectCitySpotEdgeSet = set()
undirectCitySpotEdgeMap = {}
undirectSpotEdgeSet = set()
undirectSpotEdgeMap = {}

directSpotEdgeSet = set()
directSpotEdgeMap = {}
# file = 'errorcityname2.csv'
# readfile(file)

cityUndirectEdgeFile = 'C:\Users\dell\Desktop\undirectCityEdges.txt'
cityDirectEdgeFile = 'C:\Users\dell\Desktop\directCityEdges.txt'
spotUndirectEdgeFile = 'C:\Users\dell\Desktop\undirectSpotEdges.txt'
spotDirectEdgeFile = 'C:\Users\dell\Desktop\directSpotEdges.txt'

#getCityUndirectEdgePairs(cityUndirectEdgeFile)
#getCityDirectEdgePairs(cityDirectEdgeFile)
getSpotUndirectEdgePairs(spotUndirectEdgeFile)