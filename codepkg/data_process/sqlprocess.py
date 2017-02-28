# encoding: UTF-8

import codecs
import os
import string

import MySQLdb
import time
from codepkg import mod_config
import os.path
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

map = {}

pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
#不考虑地理距离建网络
undirectCityEdgeFile = pwd + '/Datas/Edge_datas/undirectCityEdges_rse.txt'
directCityEdgeFile = pwd + '/Datas/Edge_datas/directCityEdges_rse.txt'
undirectSpotEdgeFile = pwd + '/Datas/Edge_datas/undirectSpotEdges_rse.txt'
directSpotEdgeFile = pwd + '/Datas/Edge_datas/directSpotEdges_rse.txt'
undirectCityDistEdgeFile = pwd + '/Datas/Edge_datas/undirectCityEdges_dist_rse.txt'
directCityDistEdgeFile = pwd + '/Datas/Edge_datas/directCityEdges_dist_rse.txt'
undirectSpotDistEdgeFile = pwd + '/Datas/Edge_datas/undirectSpotEdges_dist_rse.txt'
directSpotDistEdgeFile = pwd + '/Datas/Edge_datas/directSpotEdges_dist_rse.txt'

populationFile = 'C:\\Users\\dell\\Desktop\\populations.csv'

def mapFileToDB():
    #1
    fname = os.path.basename(undirectCityEdgeFile)
    suffix = fname.rfind('.')
    fname = fname[0:suffix]
    map[fname] = 'graph_nodistance_undirect_city'
    #2
    fname = os.path.basename(directCityEdgeFile)
    suffix = fname.rfind('.')
    fname = fname[0:suffix]
    map[fname] = 'graph_nodistance_direct_city'
    #3
    fname = os.path.basename(undirectSpotEdgeFile)
    suffix = fname.rfind('.')
    fname = fname[0:suffix]
    map[fname] = 'graph_nodistance_undirect_spot'
    #4
    fname = os.path.basename(directSpotEdgeFile)
    suffix = fname.rfind('.')
    fname = fname[0:suffix]
    map[fname] = 'graph_nodistance_direct_spot'
    #5
    fname = os.path.basename(undirectCityDistEdgeFile)
    suffix = fname.rfind('.')
    fname = fname[0:suffix]
    map[fname] = 'graph_distance_undirect_city'
    #6
    fname = os.path.basename(directCityDistEdgeFile)
    suffix = fname.rfind('.')
    fname = fname[0:suffix]
    map[fname] = 'graph_distance_direct_city'
    #7
    fname = os.path.basename(undirectSpotDistEdgeFile)
    suffix = fname.rfind('.')
    fname = fname[0:suffix]
    map[fname] = 'graph_distance_undirect_spot'
    #8
    fname = os.path.basename(directSpotDistEdgeFile)
    suffix = fname.rfind('.')
    fname = fname[0:suffix]
    map[fname] = 'graph_distance_direct_spot'

def storeIntoDB(file):
    fname = os.path.basename(file)
    suffix = fname.rfind('.')
    fname = fname[0:suffix]
    #db = MySQLdb.connect('127.0.0.1', 'root', 'admin', 'python', charset="utf8")
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset='utf8')

    cursor = db.cursor()

    fs = codecs.open(file, 'r+', encoding='utf8')
    lines = fs.readlines()
    try:
        for line in lines:
            line = line.strip('\r\n')
            items = string.split(line, ',')
            if len(items) == 3:
                print items[0], items[1], items[2]
                mysql = 'insert into '+ map[fname] + '(source,target,frequency) values (%s,%s,%s)'
                print mysql
                cursor.execute(mysql,items)
            elif len(items) == 5:
                print items[0], items[1], str(items[2]), str(items[3]), str(items[4])
                mysql = 'insert into ' + map[fname] + '(source,target,frequency,distance,weight) values (%s,%s,%s,%s,%s)'
                print mysql
                cursor.execute(mysql,items)
        db.commit()
    except Exception, msg:
        print msg
        db.rollback()
    db.close()

def storePopulationInfo(file):
    fname = os.path.basename(file)
    suffix = fname.rfind('.')
    fname = fname[0:suffix]
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset='utf8')

    cursor = db.cursor()

    fs = codecs.open(file, 'r+', encoding='gbk')
    lines = fs.readlines()
    try:
        for line in lines:
            line = line.strip('\r\n')
            items = string.split(line, ',')

            print items[0], items[1], items[2], items[3], items[4], items[5], items[6]
            population = str(items[6])
            cname = str(items[2])
            updateSQL = "update city set population =%s where cname =  '%s'" % (population, cname)
            print updateSQL
            cursor.execute(updateSQL)
            db.commit()
            # mysql = 'insert into ' + map[fname] + '(source,target,frequency) values (%s,%s,%s)'
            # print mysql

            #cursor.execute(mysql, items)
            #db.commit()
    except Exception, msg:
        print msg
        #db.rollback()
    #db.close()

def updateSpotTravelFromcity():
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset='utf8')
    cursor = db.cursor()
    queryAllUidsSQL = "select uid,obode from pythondb.user where uid in (select distinct(userid) from pythondb.spottravel where fromcity = '')"
    cursor.execute(queryAllUidsSQL)
    uidResults = cursor.fetchall()
    index = 1
    sql = "update spottravel set fromcity ='%s' where userid='%s'"
    for row in uidResults:
        try:
            updateSQL = "update spottravel set fromcity = '"+row[1]+"' where userid = '" + row[0]+"'"
            now = int(time.time())
            timeArray = time.localtime(now)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            print index,otherStyleTime,updateSQL
            cursor.execute(updateSQL)
            db.commit()
            index += 1
        except Exception, msg:
            print msg
            db.rollback()
    db.close()

#storePopulationInfo(populationFile)
updateSpotTravelFromcity()

#mapFileToDB()
# storeIntoDB(undirectCityEdgeFile)
# storeIntoDB(directCityEdgeFile)
# storeIntoDB(undirectSpotEdgeFile)
# storeIntoDB(directSpotEdgeFile)
# storeIntoDB(undirectCityDistEdgeFile)
# storeIntoDB(directCityDistEdgeFile)
# storeIntoDB(undirectSpotDistEdgeFile)
# storeIntoDB(directSpotDistEdgeFile)