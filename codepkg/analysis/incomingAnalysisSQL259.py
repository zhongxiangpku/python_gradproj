# encoding: UTF-8

import codecs
import math
import os
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
    mysql = 'select cname from city where cname != "神农架林区" and usercount>=20 and usercount * 1.0 /(population *100) > 0.001'
    cursor.execute(mysql)
    results = cursor.fetchall()
    cityLst = []
    for row in results:
        cityLst.append(str(row[0]))
    return cityLst
    #return list(results)


def generateInComingVector(city,map,except1,except2):
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset='utf8')
    cursor = db.cursor()
    #mysql ='select fromcity, count(*) from citytravel where toccity ="' + city + '" and fromcity !="'+except1+'" and fromcity != "'+ except2 +'" group by fromcity'
    mysql = 'select fromcity, count(*) from citytravel where toccity ="' + city + '" group by fromcity'
    cursor.execute(mysql)
    results = cursor.fetchall()
    for row in results:
        key = str(row[0])
        if key == except1 or key == except2:
            continue
        if key not in allCities:
            continue
        map[key] = row[1]
    # for cityItem in allCities:
    #     key = cityItem[0]
    #     if key in map.keys():
    #         continue
    #     else:
    #         map[key] = 0

#输出R制图数据组
def outputRPlotData(city1,city2,file):
    generateInComingVector(city1,xMap,city1, city2)
    generateInComingVector(city2, yMap, city1, city2)
    fs = codecs.open(file, 'w+', encoding='utf8')
    for city in allCities:
        key = city[0]
        print key,xMap[key],yMap[key]
        fs.write(key + "," + str(xMap[key]) + "," + str(yMap[key]) + "\r\n")
    fs.flush()
    fs.close()

def computeSimilarity(cityX,cityY,mapX,mapY):

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
    for city in allCities:
        key = str(city)
        if key not in mapX or key not in mapY:
            continue

        # print key
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

    return rtn

# 计算所有城市两两之间的相似度
def calculateAllIncommingSimilarity():
    insertOutSimilaritySQL = "insert into insimilarity_259(fromcity,tocity,similarity,createtime,updatetime) values(%s, %s, %s, %s,%s)"
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset='utf8')
    cursor = db.cursor()
    #fs = codecs.open(file, 'w+', encoding='utf8')
    count = 0
    myset = set()

    queryAllUidsSQL = "select fromcity,tocity from insimilarity_259 "
    cursor.execute(queryAllUidsSQL)
    uidResults = cursor.fetchall()
    for row in uidResults:
        icity1 = str(row[0])
        icity2 = str(row[1])
        myset.add(icity1 + icity2)

    index1 = 1

    for city1 in allCities:
        key1 = city1#str(city1[0])
        index2 = 1
        for city2 in allCities:

            key2 = city2#str(city2[0])
            now = int(time.time())
            timeArray = time.localtime(now)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            print 'index1 = ',index1,'index2 = ',index2,otherStyleTime, 'Computing similarity of ', key1, '&', key2, '------------------'

            index2 += 1
            setKey1 = key1+key2
            setKey2 = key2+key1
            if setKey1 in myset or setKey2 in myset:
                continue
            if key1 == key2:
                continue
            if key1 == '神农架林区' or key2 == '神农架林区':
                continue
            else:
                xMap = {}
                yMap = {}

                generateInComingVector(key1, xMap, key1, key2)
                generateInComingVector(key2,yMap, key1, key2)
                similarity = computeSimilarity(key1, key2, xMap, yMap)
                myset.add(setKey1)

                now = int(time.time())
                timeArray = time.localtime(now)
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                print otherStyleTime,key1, '&', key2, ' similairy = ', similarity
                insertInSimilarityValues = []
                insertInSimilarityValue1 = (key1, key2, similarity, otherStyleTime, otherStyleTime)
                insertInSimilarityValue2 = (key2, key1, similarity, otherStyleTime, otherStyleTime)
                insertInSimilarityValues.append(insertInSimilarityValue1)
                insertInSimilarityValues.append(insertInSimilarityValue2)
                cursor.executemany(insertOutSimilaritySQL, insertInSimilarityValues)
                db.commit()

        index1 += 1

def getMappingSimilarityData(city,infile,outfile):
    mymap = {}
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset='utf8')
    cursor = db.cursor()
    mysql = 'select cname, arcgis_name from city'
    cursor.execute(mysql)
    results = cursor.fetchall()
    for row in results:
       mymap[row[0]] = row[1]

    ifs = codecs.open(infile, 'r+', encoding='utf8')
    ofs = codecs.open(outfile, 'w+', encoding='utf8')
    lines = ifs.readlines()
    for line in lines:
        line = line.replace("\r\n", "")
        strs = line.split(',')

        print city,strs[0],strs[1],strs[2]
        #print mymap[strs[0]],',',mymap[strs[1]],',',strs[2]
        key = strs[0]
        key = str(key)
        if key == city:
            ofs.write(mymap[strs[0]]+','+mymap[strs[1]]+','+strs[2]+"\r\n")
    ifs.close()
    ofs.flush()
    ofs.close()

def getMappingSimilarityDataFromSQL(city,outfile):
    mymap = {}
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset='utf8')
    cursor = db.cursor()
    mysql = 'select cname, arcgis_name from city'
    cursor.execute(mysql)
    results = cursor.fetchall()
    for row in results:
       mymap[row[0]] = row[1]

    ofs = codecs.open(outfile, 'w+', encoding='utf8')

    mysql = 'select tocity,similarity from insimilarity_259 where fromcity ="'+city+'"'
    cursor.execute(mysql)
    results = cursor.fetchall()
    similarityMap = {}
    for row in  results:
        similarityMap[row[0]] = row[1]

    for item in mymap.keys():
        similarity = -1.0
        if item in similarityMap.keys():
            similarity = similarityMap[item]
        if item == city:
            similarity = 1.0
        ofs.write(city+','+mymap[item]+','+str(similarity)+"\r\n")
    ofs.flush()
    ofs.close()
pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
print pwd

beijingtianjinPlotData = pwd+'\\Datas\\beijing_tianjin_incomming_plotData.txt'
beijingxianPlotData = pwd+'\\Datas\\beijing_xian_incomming_plotData.txt'
changshawuhanPlotData = pwd+'\\Datas\\changsha_wuhan_incomming_plot.txt'
beijingshanghaiPlotData = pwd+'\\Datas\\beijing_shanghai_incomming_plot.txt'
chengduabazhouPlotData = pwd+'\\Datas\\chengdu_abazhou_incomming_plot.txt'
chengdushenzhenPlotData = pwd+'\\Datas\\chengdu_shenzhen_incomming_plot.txt'
abazhoudalizhouPlotData = pwd+'\\Datas\\abazhou_dalizhou_incomming_plot.txt'
abazhouchengduPlotData = pwd+'\\Datas\\abazhou_chengdu_incomming_plot.txt'
incomingSimilarityFilePath2 = pwd+'\\Datas\\similarity_datas\\inComming_Similarity_2.txt'

allCities = listCityNames()
xMap = {}
yMap = {}
# outputRPlotData("阿坝州","成都",abazhouchengduPlotData)
# outputRPlotData("阿坝州","大理州",abazhoudalizhouPlotData)


# calculateAllIncommingSimilarity()
# queryCity = r'张家界'
# inputSimilarityFilePath = pwd+'\\Datas\\similarity_datas\\inComming_Similarity2.txt'
# outputSimilarityFilePath = pwd+'\\Datas\\similarity_datas\\output_incomming_Similarity_zhangjiajie'+'.txt'
# getMappingSimilarityData(queryCity,inputSimilarityFilePath,outputSimilarityFilePath)

queryCity = r'桂林'
outputSimilarityFilePath = pwd+'\\Datas\\similarity_datas\\output_incomming_Similarity_guilin259'+'.txt'
getMappingSimilarityDataFromSQL(queryCity,outputSimilarityFilePath)





