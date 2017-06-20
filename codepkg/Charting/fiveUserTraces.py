# encoding: UTF-8

import codecs
import os
import sys

import MySQLdb

reload(sys)
sys.setdefaultencoding( "utf-8" )

from codepkg import mod_config

def getCityCoordData():
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset='utf8')
    cursor = db.cursor()
    mysql = 'select cname,fcity,fprovince,lng,lat FROM pythondb.city'
    cursor.execute(mysql)
    results = cursor.fetchall()

    lst = ['北京','上海','广州','乌鲁木齐','重庆','杭州','苏州','深圳','武汉','长沙','西安','无锡','大理州','香港',
           '郑州','长春','三亚','酒泉','北海','辽阳','石河子','海口','伊犁州','厦门','合肥','天津','成都','西宁']
    for row in results:
        #print row[0], row[1], row[2], row[3], row[4]
        #[{coord: [10, 20]},{coord: [20, 30]}
        key = str(row[0])
        if row[0] in lst:
            print  row[0], "{coord:[",  str(row[3]) , "," , str(row[4]) , "]}"

getCityCoordData()
