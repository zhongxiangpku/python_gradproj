# encoding: UTF-8
import codecs
import os
import sys
import MySQLdb
import string
from codepkg import mod_config
reload(sys)
sys.setdefaultencoding( "utf-8" )


def mappingUserCountRankPlot(file):
    fs = codecs.open(file, 'w+', encoding='utf8')
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                     charset=mod_config.dbcharset)
    cursor = db.cursor()
    queryUserCountSQL = 'select cname,usercount from city order by usercount desc'
    cursor.execute(queryUserCountSQL)
    rows = cursor.fetchall()
    index = 1
    for row in rows:
        key = str(row[0])
        fs.write(str(index)+";" +key+";"+str(row[1])+ "\r\n")
        index+=1
    fs.close()

def mappingCityVisitCountRankPlot(file):
    fs = codecs.open(file, 'w+', encoding='utf8')
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                     charset=mod_config.dbcharset)
    cursor = db.cursor()
    queryUserCountSQL = 'select fromcity,count(*) from pythondb.citytravel where  fromcity != toccity group by fromcity having count(*) > 0 order by count(*) desc'
    cursor.execute(queryUserCountSQL)
    rows = cursor.fetchall()
    index = 1
    for row in rows:
        key = str(row[0])
        fs.write(str(index)+";" +key+";"+str(row[1])+ "\r\n")
        index+=1
    fs.close()

pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
print pwd

# rankUserCountFile = pwd + '\\rankusercountplot.txt'
# mappingUserCountRankPlot(rankUserCountFile)

rankCityVisitCountFile = pwd + '\\rankCityVisitCount.txt'
mappingCityVisitCountRankPlot(rankCityVisitCountFile)

