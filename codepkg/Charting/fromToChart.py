# encoding: UTF-8

import codecs
import os
import sys

import MySQLdb

reload(sys)
sys.setdefaultencoding( "utf-8" )

from codepkg import mod_config

def countingFromCity(city,file):
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset='utf8')
    cursor = db.cursor()
    #mysql = 'SELECT city,count(*) FROM pythondb.citynote where departure ="' + city + '" and departure != city group by city order by count(*) desc limit 0,30'
    mysql = 'SELECT toccity,count(*) FROM pythondb.citytravel where fromcity ="' + city + '" and fromcity != toccity group by toccity order by count(*) desc limit 0,30'
    cursor.execute(mysql)
    results = cursor.fetchall()
    fs = codecs.open(file, 'w+', encoding='utf8')
    for row in results:
        print city,row[0],row[1]
        fs.write("[{name:'"+city + "'},{name:'" + str(row[0]) + "',value:" + str(row[1]) + "}],\r\n")
    #SELECT city,count(*) FROM pythondb.citynote where departure = '北京' and departure != city group by city;
    fs.flush()
    fs.close()

def countingToCity(city,file):
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset='utf8')
    cursor = db.cursor()
    mysql = 'SELECT departure,count(*) FROM pythondb.citynote where city !="' + city + '" and departure = city group by departure order by count(*) desc limit 0,30'
    cursor.execute(mysql)
    results = cursor.fetchall()
    fs = codecs.open(file, 'w+', encoding='utf8')
    for row in results:
        print city, row[0], row[1]
        fs.write("[{name:'" + str(row[0]) + "'},{name:'" + city + "',value:" + str(row[1]) + "}],\r\n")
    # SELECT city,count(*) FROM pythondb.citynote where departure = '北京' and departure != city group by city;
    fs.flush()
    fs.close()


pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
print pwd

valueFromOutputFile_beijing = pwd+'\\Datas\\Echart_datas\\from_beijing_output_Data.txt'
valueFromOutputFile_shanghai = pwd+'\\Datas\\Echart_datas\\from_shanghai_output_Data.txt'
valueFromOutputFile_tianjin = pwd+'\\Datas\\Echart_datas\\from_tianjin_output_Data.txt'
valueFromOutputFile_shenzhen = pwd+'\\Datas\\Echart_datas\\from_shenzhen_output_Data.txt'
countingFromCity('北京',valueFromOutputFile_beijing)
countingFromCity('上海',valueFromOutputFile_shanghai)
countingFromCity('天津',valueFromOutputFile_tianjin)
countingFromCity('保定',valueFromOutputFile_shenzhen)

valueToOutputFile_abazhou = pwd+'\\Datas\\Echart_datas\\to_abazhou_output_Data.txt'
valueToOutputFile_guilin = pwd+'\\Datas\\Echart_datas\\to_guilin_output_Data.txt'
valueToOutputFile_chengdu = pwd+'\\Datas\\Echart_datas\\to_chengdu_output_Data.txt'
# countingToCity('阿坝州',valueToOutputFile_abazhou)
# countingToCity('桂林',valueToOutputFile_guilin)
# countingToCity('成都',valueToOutputFile_chengdu)
