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

coords = {}

mymap = {}
def getAirportData(file):
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset='utf8')
    cursor = db.cursor()
    # mysql = 'SELECT city,count(*) FROM pythondb.citynote where departure ="' + city + '" and departure != city group by city order by count(*) desc limit 0,30'
    mysql = 'select cname,fcity,fprovince,lng,lat FROM pythondb.city'
    cursor.execute(mysql)
    results = cursor.fetchall()
    fs = codecs.open(file, 'w+', encoding='utf8')
    index = 0
    for row in results:
        print row[0], row[1], row[2], row[3], row[4]
        fs.write("['" + row[0] + "','" + row[1] + "','" + row[2] + "'," + str(row[3]) + "," + str(row[4]) + "],\r\n")
        mymap[row[0]] = index;
        index += 1
    fs.flush()
    fs.close()

def getRoute(file):
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset='utf8')
    cursor = db.cursor()
    mysql = 'select fromcity,toccity,count(*) FROM pythondb.citytravel where fromcity != "未填" and fromcity != toccity group by fromcity,toccity having count(*) >= 10 order by count(*) desc;'
    cursor.execute(mysql)
    results = cursor.fetchall()
    fs = codecs.open(file, 'w+', encoding='utf8')
    for row in results:
        print row[0],  row[1], mymap[row[0]], mymap[row[1]],'count=',row[2]
        fs.write("[1," + str(mymap[row[0]]) + "," + str(mymap[row[1]]) +"],\r\n")
    #SELECT city,count(*) FROM pythondb.citynote where departure = '北京' and departure != city group by city;
    fs.flush()
    fs.close()



pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
print pwd

airports = pwd+'\\Datas\\Echart_datas\\airports.txt'
routes = pwd+'\\Datas\\Echart_datas\\routes.txt'

getAirportData(airports)
getRoute(routes)

