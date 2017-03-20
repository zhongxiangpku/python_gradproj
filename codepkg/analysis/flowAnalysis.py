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

def listCityNames():
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    mysql = 'select cname from city'
    cursor.execute(mysql)
    results = cursor.fetchall()
    return list(results)

def computeInFlowInfos():
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    queryInFlowSQL = 'select toccity,count(*) from citytravel group by toccity'
    cursor.execute(queryInFlowSQL)
    rows = cursor.fetchall()

    mymap = {}
    for row in rows:
        mymap[row[0]] = row[1]
    for city in allCities:
        key = city[0]
        inflow = mymap.get(key)
        if inflow is None:
            inflow = 0
        updateInFlowSQL = 'update city set inflow = %s where cname = "%s"' % (inflow,key)
        print updateInFlowSQL
        cursor.execute(updateInFlowSQL)
        db.commit()
    db.close()

def computeOutFlowInfos():
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    queryOutFlowSQL = 'select fromcity,count(*) from citytravel group by fromcity'
    cursor.execute(queryOutFlowSQL)
    rows = cursor.fetchall()

    mymap = {}
    for row in rows:
        mymap[row[0]] = row[1]
    for city in allCities:
        key = city[0]
        outflow = mymap.get(key)
        if outflow is None:
            outflow = 0
        updateOutFlowSQL = 'update city set outflow = %s where cname = "%s"' % (outflow,key)
        print updateOutFlowSQL
        cursor.execute(updateOutFlowSQL)
        db.commit()
    db.close()


def computeSameFlowInfos():
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    querySameFlowSQL = 'select fromcity,toccity,count(*) from citytravel where fromcity = toccity group by fromcity,toccity'
    cursor.execute(querySameFlowSQL)
    rows = cursor.fetchall()

    mymap = {}
    for row in rows:
        mymap[row[0]] = row[2]
    for city in allCities:
        key = city[0]
        sameflow = mymap.get(key)
        if sameflow is None:
            sameflow = 0
        updateSameFlowSQL = 'update city set sameflow = %s where cname = "%s"' % (sameflow, key)
        print updateSameFlowSQL
        cursor.execute(updateSameFlowSQL)
        db.commit()
    db.close()

def computeUserCount():
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    queryUserCountSQL = 'select obode,count(*) from user group by obode'
    cursor.execute(queryUserCountSQL)
    rows = cursor.fetchall()

    mymap = {}
    for row in rows:
        mymap[row[0]] = row[1]
    for city in allCities:
        key = city[0]
        usercount = mymap.get(key)
        if usercount is None:
            usercount = 0
        updateUserCountSQL = 'update city set usercount = %s where cname = "%s"' % (usercount, key)
        print updateUserCountSQL
        cursor.execute(updateUserCountSQL)
        db.commit()
    db.close()

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
        key = str(row[0])
        coords[key] = coord

    for key, value in coords.items():
        print key, value

def gravityModel(count,distance,file):
    fs = codecs.open(file, 'w+', encoding='utf8')
    fs.write("id;pi;pj;dij;fij"+ "\r\n")
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    queryUserCountSQL = 'select cname,usercount from city'
    cursor.execute(queryUserCountSQL)
    rows = cursor.fetchall()
    userCountMap = {}
    for row in rows:
        key = str(row[0])
        userCountMap[key] = row[1]

    getCoords()
    flowMap = {}
    index = 1
    index1 = 1
    index2 = 1
    for city1 in allCities:
        key1 = str(city1[0])
        index2 = 1
        flowMap = {}
        flowSQL = "select toccity,count(*) from citytravel where fromcity = '" + key1 + "' group by toccity"
        cursor.execute(flowSQL)
        rows = cursor.fetchall()
        for row in rows:
            key = str(row[0])
            flowMap[key] = row[1]

        for city2 in allCities:
            key2 = str(city2[0])
            if key1 == key2:
                continue

            pi = userCountMap[key1]
            pj = userCountMap[key2]
            if pi<count or pj<count:
                continue

            toponym1 = coords[key1]
            toponym2 = coords[key2]
            lat1 = toponym1['lat']
            lng1 = toponym1['lng']
            lat2 = toponym2['lat']
            lng2 = toponym2['lng']
            dij =  geoutil.getPointDistance(lat1, lng1, lat2, lng2)

            # flowSQL  = "select count(*) from citytravel where fromcity = '"+str(key1)+"' and toccity = '"+str(key2)+"'"
            # print flowSQL
            # cursor.execute(flowSQL)
            # rows = cursor.fetchall()
            # fij = rows[0][0]
            if key2 in flowMap.keys():
                fij = flowMap[key2]

                if fij>0:
                    print index,index1,index2,'pi=',pi,'pj=',pj,'dij=',dij,'fij=',fij
                    fs.write(str(index)+";"+str(pi)+";"+str(pj)+";"+str(dij)+";"+str(fij) + "\r\n")

                    index2 += 1
                    index += 1
        index1+=1
    fs.flush()
    fs.close()

def gravityModel2(count,distance,file):
    fs = codecs.open(file, 'w+', encoding='utf8')
    fs.write("id;pi;pj;dij;fij"+ "\r\n")
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    queryUserCountSQL = 'select cname,inflow,outflow from city'
    cursor.execute(queryUserCountSQL)
    rows = cursor.fetchall()
    userCountMap = {}
    inflowMap = {}
    outflowMap = {}
    for row in rows:
        key = str(row[0])
        userCountMap[key] = row[1]
        inflowMap[key] = row[1]
        outflowMap[key] = row[2]
    getCoords()
    flowMap = {}
    index = 1
    index1 = 1
    index2 = 1
    for city1 in allCities:
        key1 = str(city1[0])
        index2 = 1
        flowMap = {}
        flowSQL = "select toccity,count(*) from citytravel where fromcity = '" + key1 + "' group by toccity"
        cursor.execute(flowSQL)
        rows = cursor.fetchall()
        for row in rows:
            key = str(row[0])
            flowMap[key] = row[1]

        for city2 in allCities:
            key2 = str(city2[0])
            if key1 == key2:
                continue

            #pi = userCountMap[key1]
            #pj = userCountMap[key2]
            pi = inflowMap[key1]
            pj = outflowMap[key2]
            if pi<count or pj<count:
                continue

            toponym1 = coords[key1]
            toponym2 = coords[key2]
            lat1 = toponym1['lat']
            lng1 = toponym1['lng']
            lat2 = toponym2['lat']
            lng2 = toponym2['lng']
            dij =  geoutil.getPointDistance(lat1, lng1, lat2, lng2)

            # flowSQL  = "select count(*) from citytravel where fromcity = '"+str(key1)+"' and toccity = '"+str(key2)+"'"
            # print flowSQL
            # cursor.execute(flowSQL)
            # rows = cursor.fetchall()
            # fij = rows[0][0]
            if key2 in flowMap.keys():
                fij = flowMap[key2]

                if fij>0:
                    print index,key1,key2,index1,index2,'pi=',pi,'pj=',pj,'dij=',dij,'fij=',fij
                    fs.write(str(index)+";"+str(pi)+";"+str(pj)+";"+str(dij)+";"+str(fij) + "\r\n")

                    index2 += 1
                    index += 1
        index1+=1
    fs.flush()
    fs.close()

def computeGyration():
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    mysql = 'select distinct(uid) from user where finish = 0 limit 0,50000'
    cursor.execute(mysql)
    users = cursor.fetchall()
    getCoords()

    selectUserTravelSQL = 'select fromcity,toccity from citytravel where userid = %s'

    updateUserSQL = 'update user set gyration = %s, visitcity = %s, finish = 1 where uid = "%s"'
    #updateUserValues = []
    index = 0
    for user in users:
        cursor.execute(selectUserTravelSQL,(user,))
        travels = cursor.fetchall()

        travelCount = 0
        gyrationSum = 0.0
        for travel in travels:
            fromcity = str(travel[0])
            toccity = str(travel[1])

            fromcity = fromcity.strip()
            toccity = toccity.strip()
            if fromcity == toccity:
                continue
            #print fromcity,toccity

            if fromcity not in coords.keys() or toccity not in coords.keys():
                continue
            toponym1 = coords[fromcity]
            toponym2 = coords[toccity]

            lat1 = toponym1['lat']
            lng1 = toponym1['lng']
            lat2 = toponym2['lat']
            lng2 = toponym2['lng']
            distance = geoutil.getPointDistance(lat1, lng1, lat2, lng2)
            travelCount += 1
            gyrationSum += distance
        now = int(time.time())
        timeArray = time.localtime(now)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        if travelCount == 0:
            #print  index, 'user=', user, 'travelCount = ', travelCount, ', gyrationSum=', gyrationSum
            index += 1
            updateUserSQL = 'update user set finish = 1 where uid = "%s"'%(str(user[0]),)
            cursor.execute(updateUserSQL)
            db.commit()
            continue;
        gyration = gyrationSum/travelCount
        if index %10 == 0:
            print  index,otherStyleTime,'user=',user, 'travelCount = ',travelCount,', gyrationSum=',gyrationSum,'gyration',gyration
        #updateUserValues.append((gyration, travelCount, str(user[0])))
        updateUserSQL = 'update user set finish = 1,gyration = %s, visitcity = %s where uid = "%s"'%(gyration, travelCount, str(user[0]))

        #print updateUserSQL
        #if index % 10 == 0:
            #cursor.executemany(updateUserSQL,updateUserValues)
        cursor.execute(updateUserSQL)
        db.commit()
        #updateUserValues = []
        index += 1


pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
print pwd

gravity_100 = pwd + '\\gravity_100.txt'
gravity_50 = pwd + '\\gravity_50.txt'
gravity_10 = pwd + '\\gravity_10.txt'
gravity_1 = pwd + '\\gravity_1.txt'

allCities = listCityNames()
# computeInFlowInfos()
# computeOutFlowInfos()
# computeSameFlowInfos()
# computeUserCount()
# gravityModel(1,0,gravity_1)
# gravityModel(100,0,gravity_100)
# gravityModel(50,0,gravity_50)

# gravityModel2(1,0,gravity_1)
# gravityModel2(10,0,gravity_10)
gravityModel2(100,0,gravity_100)
# computeGyration()
