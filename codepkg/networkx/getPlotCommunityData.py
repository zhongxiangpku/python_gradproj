#coding=utf-8

import networkx as nx
from networkx import *
import os
import matplotlib.pyplot as plt
import codecs
import string
import time
import matplotlib
import MySQLdb
from codepkg import mod_config


def listCityNames():
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    mysql = 'select cname from city where cname != "神农架林区" and usercount>=20 and usercount * 1.0 /(population *100) > 0.001'
    cursor.execute(mysql)
    results = cursor.fetchall()
    return list(results)


# partitionCities = listCityNames()
# print len(partitionCities)
# for row in partitionCities:
#     print row[0]
pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
print pwd

clusterFile = pwd + '\\cluster3.txt'
#createMatrix()

formatCityNameMap = {}
def getFormatCityName():
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    mysql = 'select cname,arcgis_name from city  '
    cursor.execute(mysql)
    results = cursor.fetchall()
    for row in results:
        key = row[0]
        value = row[1]
        formatCityNameMap[key] = value

def readClusteResult(infile,outfile):
    ifs = codecs.open(infile, encoding='gbk')
    ofs = codecs.open(outfile, 'w+', encoding='gbk')
    lines = ifs.readlines()
    ifs.close()

    getFormatCityName()
    length = len(lines)

    for i in range(length):
        line = lines[i].strip('\r\n')
        items = string.split(line, ',')

        key = items[0]
        value = items[1]
        print key, formatCityNameMap[key], value
        ofs.write(key + "," + formatCityNameMap[key] + "," + str(value) + "\r\n")
    ofs.close()

def getSubGraphs(communityFile,subGraphFile1,subGraphFile2,subGraphFile3,subGraphFile4):
    ifs = codecs.open(communityFile, encoding='gbk')
    ofs1 = codecs.open(subGraphFile1, 'w+', encoding='gbk')
    ofs2 = codecs.open(subGraphFile2, 'w+', encoding='gbk')
    ofs3 = codecs.open(subGraphFile3, 'w+', encoding='gbk')
    ofs4 = codecs.open(subGraphFile4, 'w+', encoding='gbk')
    lines = ifs.readlines()
    ifs.close()
    graphSet1 = set()
    graphSet2 = set()
    graphSet3 = set()
    graphSet4 = set()
    getFormatCityName()
    length = len(lines)

    # for key in formatCityNameMap.keys():

    for i in range(length):
        line = lines[i].strip('\r\n')
        items = string.split(line, ',')

        key = items[0]
        value = int(items[1])
        if value == 1:
            graphSet1.add(key)
        elif value == 2:
            graphSet2.add(key)
        elif value == 3:
            graphSet3.add(key)
        elif value == 4:
            graphSet4.add(key)

    print "========================graph set1======================="
    for item in graphSet1:
        print item
    print "========================graph set2======================="
    for item in graphSet2:
        print item
    print "========================graph set3======================="
    for item in graphSet3:
        print item
    print "========================graph set4======================="
    for item in graphSet4:
        print item

    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    validCityLst = set()
    mysql = 'select cname from city where cname != "神农架林区" and usercount>=20 and usercount * 1.0 /(population *100) > 0.001'
    cursor.execute(mysql)
    results = cursor.fetchall()
    for row in results:
        cityKey = row[0]
        validCityLst.add(cityKey)

    mysql = 'select fromcity,toccity,count(*) as frenquency from citytravel where fromcity!=toccity GROUP BY  fromcity,toccity having count(*)>=10'
    cursor.execute(mysql)
    results = cursor.fetchall()
    edgeMap = {}

    for row in results:
        start = row[0]
        end = row[1]
        freq = int(row[2])
        if start not in validCityLst or end not in validCityLst:
            continue
        key1 = start + ";" + end
        key2 = end + ";" + start
        if key1 not in edgeMap.keys() and key2 not in edgeMap.keys():
            edgeMap[key1] = freq
        elif key1 not in edgeMap.keys() and key2 in edgeMap.keys():
            edgeMap[key2] = edgeMap[key2] + freq
        elif key1 in edgeMap.keys() and key2 not in edgeMap.keys():
            edgeMap[key1] = edgeMap[key1] + freq
        else:
            print 'process error!'

    for k, v in edgeMap.items():
        items = string.split(k, ';')
        fromcity = items[0]
        tocity = items[1]
        if fromcity in graphSet1 and tocity in graphSet1:
            ofs1.write(k + ";" + str(v) + "\r\n")
        elif fromcity in graphSet2 and tocity in graphSet2:
            ofs2.write(k + ";" + str(v) + "\r\n")
        elif fromcity in graphSet3 and tocity in graphSet3:
            ofs3.write(k + ";" + str(v) + "\r\n")
        elif fromcity in graphSet4 and tocity in graphSet4:
            ofs4.write(k + ";" + str(v) + "\r\n")
        print k, v

    ofs1.flush()
    ofs2.flush()
    ofs3.flush()
    ofs4.flush()
    ofs1.close()
    ofs2.close()
    ofs3.close()
    ofs4.close()


# clusterResultFile = pwd + '\\community.csv'
# clusterResultArcGISFile = pwd + '\\community_data.txt'
# readClusteResult(clusterResultFile,clusterResultArcGISFile)

# subGraphFile1 = pwd + '\\graph_edge1.txt'
# subGraphFile2 = pwd + '\\graph_edge2.txt'
# subGraphFile3 = pwd + '\\graph_edge3.txt'
# subGraphFile4 = pwd + '\\graph_edge4.txt'
# getSubGraphs(clusterResultFile,subGraphFile1,subGraphFile2,subGraphFile3,subGraphFile4)

clusterResultFile = pwd + '\\community_level2.csv'
clusterResultArcGISFile = pwd + '\\community_data2.txt'
readClusteResult(clusterResultFile,clusterResultArcGISFile)
