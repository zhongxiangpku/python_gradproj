# encoding: UTF-8

import codecs
import math
import os
import string
import sys
import time

import MySQLdb

from codepkg import mod_config

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


def generateOutComingVector(city,map,except1,except2):
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset='utf8')
    cursor = db.cursor()
    mysql ='select toccity, count(*) from citytravel where fromcity ="' + city + '" and toccity !="'+except1+'"  and toccity != "'+ except2 +'" group by toccity order by count(*) desc'
    cursor.execute(mysql)
    results = cursor.fetchall()
    for row in results:
        #print row[0],row[1]
        map[row[0]] = row[1]
    for cityItem in cities:
        key = cityItem[0]
        if key in map.keys():
            continue
        else:
            map[key] = 0

def computeSimilarity(cityX,cityY,mapX,mapY):
    print 'Computing similarity of ',cityX, '&', cityY,'------------------'
    sumCi = sum(mapX.values())
    lenCi = len(mapX.values())
    sumCj = sum(mapY.values())
    lenCj = len(mapY.values())
    ECi = sumCi*1.0/lenCi
    ECj = sumCj * 1.0 / lenCj
    # print('sumCi, lenCi, ECi ',sumCi,lenCi,sumCi*1.0/lenCi)
    # print('sumCj, lenCj, ECj ', sumCj, lenCj, sumCj * 1.0 / lenCj)
    sumInnerProduct = 0.0
    sumProductX = 0.0
    sumProductY = 0.0
    for city in cities:
        key = city[0]
        Cin = mapX[key]
        Cjn = mapY[key]
        #print key, xMap[key], yMap[key]
        # 考虑正值
        # sumInnerProduct += math.fabs(((Cin - ECi) * (Cjn - ECj)))
        sumInnerProduct += ((Cin - ECi)*(Cjn - ECj))
        sumProductX += ((Cin - ECi) * (Cin - ECi))
        sumProductY += ((Cjn - ECj) * (Cjn - ECj))
    if sumProductX - 0 < 0.0001 or sumProductY - 0.0 < 0.0001:
        return 0
    rtn = sumInnerProduct / (math.sqrt(sumProductX) * math.sqrt(sumProductY))
    print cityX,'&',cityY,' similairy = ',rtn
    return rtn

# 计算所有城市两两之间的相似度
def calculateAllSimilarity():
    # fs = codecs.open(similarityFilePath2, 'w+', encoding='utf8')
    count = 0
    insertOutSimilaritySQL = "insert into outsimilarity(fromcity,tocity,similarity,createtime,updatetime) values(%s, %s, %s, %s,%s)"
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset='utf8')
    cursor = db.cursor()

    myset = set()
    queryAllUidsSQL = "select fromcity,tocity from outsimilarity "
    cursor.execute(queryAllUidsSQL)
    uidResults = cursor.fetchall()
    for row in uidResults:
        #print row[0],row[1]
        icity1 = str(row[0])
        icity2 = str(row[1])
        myset.add(icity1+icity2)

    for city1 in cities:
        key1 = str(city1[0])
        for city2 in cities:
            key2 = str(city2[0])
            setKey1 = key1 + key2
            setKey2 = key2 + key1
            if setKey1 in myset or setKey2 in myset:
                continue
            if key1 == key2:
                now = int(time.time())
                timeArray = time.localtime(now)
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                insertOutSimilarityValue = (key1, key2, 1.0, otherStyleTime, otherStyleTime)
                cursor.execute(insertOutSimilaritySQL, insertOutSimilarityValue)
                db.commit()
                continue
            # else:
            #     xMap = {}
            #     yMap = {}
            #     generateOutComingVector(key1, xMap, key1, key2)
            #     generateOutComingVector(key2,yMap, key1, key2)
            #     similarity = computeSimilarity(key1, key2, xMap, yMap)
            #     myset.add(setKey1)
            #     now = int(time.time())
            #     timeArray = time.localtime(now)
            #     otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            #
            #     insertOutSimilarityValues = []
            #     insertOutSimilarityValue1 = (key1, key2, similarity, otherStyleTime, otherStyleTime)
            #     insertOutSimilarityValue2 = (key2, key1, similarity, otherStyleTime, otherStyleTime)
            #     insertOutSimilarityValues.append(insertOutSimilarityValue1)
            #     insertOutSimilarityValues.append(insertOutSimilarityValue2)
            #     cursor.executemany(insertOutSimilaritySQL, insertOutSimilarityValues)
            #     db.commit()
                # fs.write(key1 + "," + key2 + "," + str(similarity) + "\r\n")
                # fs.write(key2 + "," + key1 + "," + str(similarity) + "\r\n")
    # fs.flush()
    # fs.close()

def getMappingSimilarityData(city,outfile):
    mymap = {}
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset='utf8')
    cursor = db.cursor()
    mysql = 'select cname, arcgis_name from city'
    cursor.execute(mysql)
    results = cursor.fetchall()
    for row in results:
       mymap[row[0]] = row[1]

    #ifs = codecs.open(infile, 'r+', encoding='utf8')
    mysql = 'select fromcity, tocity, similarity from outsimilarity where fromcity ="'+city+'"'
    ofs = codecs.open(outfile, 'w+', encoding='utf8')
    cursor.execute(mysql)
    results = cursor.fetchall()
    for row in results:
        print city,row[0],row[1],row[2]
        #print mymap[strs[0]],',',mymap[strs[1]],',',strs[2]
        key = row[0]
        key = str(key)
        if key == city:
            ofs.write(mymap[row[0]]+','+mymap[row[1]]+','+str(row[2])+"\r\n")
    ofs.flush()
    ofs.close()

pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
print pwd

beijingtianjinPlotData = pwd+'\\Datas\\beijing_tianjin_plot.txt'
changshawuhanPlotData = pwd+'\\Datas\\changsha_wuhan_plot.txt'
beijingshanghaiPlotData = pwd+'\\Datas\\beijing_shanghai_plot.txt'
similarityFilePath2 = pwd+'\\Datas\\similarity_datas\\outComming_Similarity2.txt'

cities = listCityNames()
# xMap = {}
# yMap = {}

queryCity = '北京'
inputSimilarityFilePath = pwd+'\\Datas\\similarity_datas\\outComming_Similarity.txt'
outputSimilarityFilePath = pwd+'\\Datas\\similarity_datas\\output_Similarity_'+queryCity+'.txt'
#calculateAllSimilarity()
getMappingSimilarityData(queryCity,outputSimilarityFilePath)

#输出R制图数据组
def outputRPlotData(file,city1,city2):
    generateOutComingVector(city1,xMap, city2, city1)
    generateOutComingVector(city2, yMap, city2, city1)
    fs = codecs.open(file, 'w+', encoding='utf8')
    for city in cities:
        key = city[0]
        print key,xMap[key],yMap[key]
        fs.write(key + "," + str(xMap[key]) + "," + str(yMap[key]) + "\r\n")
    fs.flush()
    fs.close()

def storeOutSimilarity(file):
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset='utf8')
    cursor = db.cursor()

    mysql = 'insert into outsimilarity(fromcity,tocity,similarity,createtime,updatetime) values (%s,%s,%s, %s, %s)'
    fs = codecs.open(file, 'r+', encoding='utf8')
    lines = fs.readlines()
    index = 1;
    insertOutSimilarityValues = []
    try:
        for line in lines:
            line = line.strip('\r\n')
            items = string.split(line, ',')

            print items[0], items[1], items[2]
            now = int(time.time())
            timeArray = time.localtime(now)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

            insertOutSimilarityValue = (items[0], items[1], items[2], otherStyleTime, otherStyleTime)
            insertOutSimilarityValues.append(insertOutSimilarityValue)
            if index %100 == 0:
                cursor.executemany(mysql,insertOutSimilarityValues)
                db.commit()
                insertOutSimilarityValues = []
            index += 1
        if len(insertOutSimilarityValues)>0:
            cursor.executemany(mysql, insertOutSimilarityValues)
            db.commit()
    except Exception, msg:
        print msg
        db.rollback()
    db.close()

#storeOutSimilarity(similarityFilePath2)
#outputRPlotData(beijingtianjinPlotData,'北京', '天津')
#outputRPlotData(beijingshanghaiPlotData,'北京', '上海')


