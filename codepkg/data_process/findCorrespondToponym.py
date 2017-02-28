# encoding: UTF-8

import codecs
import os
import sys

import MySQLdb

reload(sys)
sys.setdefaultencoding( "utf-8" )

from codepkg import mod_config

def findUncorrectToponym(file):
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset='utf8')
    cursor = db.cursor()

    fs = codecs.open(file, 'r+', encoding='utf8')
    lines = fs.readlines()
    # line = fs.readline()
    # print line
    for line in lines:
        # line = line.remove('\r\n')
        city = str(line)
        city = city.replace("\r\n","")
        #print 'city=',city
        mysql = 'SELECT count(*) FROM pythondb.city where arcgis_name ="' + city + '"'
        cursor.execute(mysql)
        results = cursor.fetchall()
        #print results[0][0]
        if results[0][0] == 0:
            print city
    fs.flush()
    fs.close()

pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
print pwd

valueOutputFile = pwd+'\\Datas\\temp_toponym.txt'
findUncorrectToponym(valueOutputFile)
findUncorrectToponym(valueOutputFile)