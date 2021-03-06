# encoding: UTF-8

import codecs
import math
import os
import sys

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


def generateInComingVector(city,map,except1,except2):
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset='utf8')
    cursor = db.cursor()
    mysql ='select fromcity, count(*) from citytravel where toccity ="' + city + '" and fromcity !="'+except1+'"  and fromcity != "'+ except2 +'" group by fromcity order by count(*) desc'
    cursor.execute(mysql)
    results = cursor.fetchall()
    for row in results:
        map[row[0]] = row[1]
    for cityItem in allCities:
        key = cityItem[0]
        if key in map.keys():
            continue
        else:
            map[key] = 0

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
    for city in allCities:
        key = city[0]
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
    print cityX,'&',cityY,' similairy = ',rtn
    return rtn

# 计算所有城市两两之间的相似度
def calculateAllIncommingSimilarity(file):
    fs = codecs.open(file, 'w+', encoding='utf8')
    count = 0
    myset = set()
    for city1 in allCities:
        key1 = city1[0]
        for city2 in allCities:
            key2 = city2[0]

            setKey1 = city1+city2
            setKey2 = city2+city1
            if setKey1 in myset or setKey2 in myset:
                continue
            if key1 == key2:
                continue
            else:
                xMap = {}
                yMap = {}
                generateInComingVector(key1, xMap, key1, key2)
                generateInComingVector(key2,yMap, key1, key2)
                similarity = computeSimilarity(key1, key2, xMap, yMap)
                myset.add(setKey1)
                fs.write(key1 + "," + key2 + ","+str(similarity)+"\r\n")
                fs.write(key2 + "," + key1 + "," + str(similarity) + "\r\n")
    fs.flush()
    fs.close()

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
abazhousanyaPlotData = pwd+'\\Datas\\abazhou_sanya_incomming_plot.txt'
incomingSimilarityFilePath2 = pwd+'\\Datas\\similarity_datas\\inComming_Similarity_2.txt'

allCities = listCityNames()
xMap = {}
yMap = {}
# outputRPlotData("北京","天津",beijingtianjinPlotData)
#outputRPlotData("阿坝州","三亚",abazhousanyaPlotData)


#calculateAllIncommingSimilarity(incomingSimilarityFilePath2)

queryCity = r'大理州'
inputSimilarityFilePath = pwd+'\\Datas\\similarity_datas\\inComming_Similarity2.txt'
#outputSimilarityFilePath = pwd+'\\Datas\\similarity_datas\\output_incomming_Similarity_abazhou'+'.txt'
# outputSimilarityFilePath = pwd+'\\Datas\\similarity_datas\\output_incomming_Similarity_guilin'+'.txt'
# outputSimilarityFilePath = pwd+'\\Datas\\similarity_datas\\output_incomming_Similarity_sanya'+'.txt'
# outputSimilarityFilePath = pwd+'\\Datas\\similarity_datas\\output_incomming_Similarity_qingdao'+'.txt'
# outputSimilarityFilePath = pwd+'\\Datas\\similarity_datas\\output_incomming_Similarity_chengdu'+'.txt'
outputSimilarityFilePath = pwd+'\\Datas\\similarity_datas\\output_incomming_Similarity_dalizhou'+'.txt'
getMappingSimilarityData(queryCity,inputSimilarityFilePath,outputSimilarityFilePath)





