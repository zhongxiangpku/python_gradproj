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

def createMatrix():
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    mysql = 'select fromcity,tocity, similarity from outsimilarity_259 group by fromcity,tocity '
    cursor.execute(mysql)
    results = cursor.fetchall()

    mymap = {}
    for row in results:
        fromcity = row[0]
        toccity = row[1]
        similarity = row[2]
        print fromcity,toccity,similarity
        key = fromcity+toccity
        mymap[key] = similarity

    partitionCities = listCityNames()

    indexmap = {}
    index = 0
    for city in partitionCities:
        indexmap[city[0]] = index
        index += 1

    fs = codecs.open(clusterFile, 'w+', encoding='utf8')

    length = len(partitionCities)
    matrix = [[0 for i in range(length)] for i in range(length)]
    #print matrix
    for city1 in partitionCities:
        key1 = city1[0]
        index1 = indexmap[key1]
        print index1
        for city2 in partitionCities:
            key2 = city2[0]

            index1 = indexmap[key1]
            index2 = indexmap[key2]
            matrix[index1][index2] = 0
            if  key1 == key2:
                matrix[index1][index2] = 0
            else:
                key = key1+key2
                if key in mymap.keys():
                    matrix[index1][index2] = 1.0/mymap[key]
    names = ''
    for i in range(length):
        names += partitionCities[i][0]+','
    names = names[0:len(names)-1]
    names = names+'\r\n'
    fs.write(names)

    for i in range(length):
        for j in range(length):
            if j>=i:
                continue
            matrix[i][j] += matrix[j][i]
            matrix[j][i] = matrix[i][j]

    for i in range(length):
        mystr = ''
        for j in range(length):
            mystr+=str(matrix[i][j])+','
        mystr = mystr[0:len(mystr)-1]
        mystr+='\r\n'
        fs.write(mystr)
    fs.close()

pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
print pwd

clusterFile = pwd + '\\outSimilarityClusterMatrix.txt'
createMatrix()

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

    keyList = []
    valueList = []
    mymap={}
    length = len(lines)

    for i in range(length):
        number = 0

        if i%2 == 0:
            print 'keys=', lines[i]
            line = lines[i].strip('\r\n')
            line = ' '.join(line.split())
            line = line.strip(' ')
            items = string.split(line, ' ')
            for item in items:
                keyList.append(item)
        else:
            print 'values=',lines[i]
            line = lines[i].strip('\r\n')
            line = ' '.join(line.split())
            line = line.strip(' ')
            items = string.split(line, ' ')
            for item in items:
                valueList.append(item)


            for j in range(len(keyList)):
                mymap[keyList[j]] = valueList[j]
            keyList = []
            valueList = []

    getFormatCityName()
    for key in formatCityNameMap.keys():
        if key in mymap.keys():
            ofs.write(key+","+formatCityNameMap[key]+","+str(mymap[key])+"\r\n")
            print key,formatCityNameMap[key],mymap[key]
        else:
            ofs.write(key + "," + formatCityNameMap[key] + "," + str(0) + "\r\n")
            print key, formatCityNameMap[key], 0
    ofs.close()



# clusterResultFile = pwd + '\\test.txt'
# clusterResultArcGISFile = pwd + '\\clusterResultArcGISFile.txt'
#readClusteResult(clusterResultFile,clusterResultArcGISFile)
# selectClusteResult(clusterResultFile)

# listCityNames()
