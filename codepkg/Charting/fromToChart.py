# encoding: UTF-8

import codecs
import os
import string
import MySQLdb
import codepkg.data_process.geoutil
import math
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from codepkg import mod_config

def countingFromCity(city,file):
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset='utf8')
    cursor = db.cursor()
    mysql = 'SELECT city,count(*) FROM pythondb.citynote where departure ="' + city + '" and departure != city group by city order by count(*) desc limit 0,30'
    cursor.execute(mysql)
    results = cursor.fetchall()
    fs = codecs.open(file, 'w+', encoding='utf8')
    for row in results:
        print city,row[0],row[1]
        fs.write("[{name:'"+city + "'},{name:'" + str(row[0]) + "',value:" + str(row[1]) + "}],\r\n")
    #SELECT city,count(*) FROM pythondb.citynote where departure = '北京' and departure != city group by city;
    fs.flush()
    fs.close()


pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
print pwd

valueOutputFile_beijing = pwd+'\\Datas\\beijing_output_Data.txt'
valueOutputFile_shanghai = pwd+'\\Datas\\shanghai_output_Data.txt'
valueOutputFile_tianjin = pwd+'\\Datas\\tianjin_output_Data.txt'
valueOutputFile_shenzhen = pwd+'\\Datas\\shenzhen_output_Data.txt'
# countingFromCity('北京',valueOutputFile_beijing)
# countingFromCity('上海',valueOutputFile_shanghai)
# countingFromCity('天津',valueOutputFile_tianjin)
countingFromCity('保定',valueOutputFile_shenzhen)