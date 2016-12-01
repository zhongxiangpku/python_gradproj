import os
import MySQLdb
import codecs
import string
import mod_config

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

def getSpotUndirectEdgePairs(file):
    # print mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname, mod_config.dbcharset
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname, charset=mod_config.dbcharset)#'222.29.117.151', 'root', 'admin', 'pythondb', charset='utf8')
    cursor = db.cursor()

    # fs = codecs.open(file, 'w+', encoding='utf8')
    try:
        mysql = 'select departure,city,spot,url from note '
        cursor.execute(mysql)
        results = cursor.fetchall()
        for row in results:
            departure = row[0]
            destination = row[1]
            spot = row[2]
            url = row[3]
            pair1 = departure + "," + destination+","+url
            # departure city -> destination city
            # print pair1
            if pair1 in undirectCitySpotEdgeSet:
                undirectCitySpotEdgeMap[pair1] += 1
            else:
                undirectCitySpotEdgeMap[pair1] = 1
                undirectCitySpotEdgeSet.add(pair1)

            # destination city -> destination spot
            pair2 = destination+","+spot
            # print pair2
            if pair2 in undirectSpotEdgeSet:
                undirectSpotEdgeMap[pair2] += 1
            else:
                undirectSpotEdgeMap[pair2] = 1
                undirectSpotEdgeSet.add(pair2)

            if url not in undirectSpot2SpotEdgeMap.keys():
                undirectSpot2SpotEdgeMap[url] = []
                undirectSpot2SpotEdgeMap[url].append(spot)
            else:
                undirectSpot2SpotEdgeMap[url].append(spot)

        index = 1
        for key, value in undirectSpot2SpotEdgeMap.items():
            str = ''
            if len(value)>1:
                for item in value:
                    str += item+ ' '
                    #str.append(item)
                print index, key, str
                index += 1
        sum = 0
        # for key, value in undirectCitySpotEdgeMap.items():
        #     key2 = key.rfind(',')
        #     key = key[0:key2]
        #     print key
        #     fs.write(key + "," + str(value) + "\r\n")
        #     print key, value
        #     sum += value
        #
        # for key, value in undirectSpotEdgeMap.items():
        #     fs.write(key + "," + str(value) + "\r\n")
        #     print key, value
        #     sum += value
        # fs.flush()
        # fs.close()
        print len(undirectCitySpotEdgeMap), len(undirectSpotEdgeMap), sum
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
undirectSpot2SpotEdgeMap = {}


directSpotEdgeSet = set()
directSpotEdgeMap = {}


# file = 'errorcityname2.csv'
# readfile(file)

pwd = os.getcwd()
print pwd
cityUndirectEdgeFile = pwd+'/undirectCityEdges.txt'
cityDirectEdgeFile = pwd+'/directCityEdges.txt'
spotUndirectEdgeFile = pwd+'/undirectSpotEdges.txt'
spotDirectEdgeFile = pwd+'/directSpotEdges.txt'

#getCityUndirectEdgePairs(cityUndirectEdgeFile)
#getCityDirectEdgePairs(cityDirectEdgeFile)
getSpotUndirectEdgePairs(spotUndirectEdgeFile)