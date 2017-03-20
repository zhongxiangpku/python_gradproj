# encoding: UTF-8
import codecs
import os
import sys
import MySQLdb
import string
from codepkg import mod_config
reload(sys)
sys.setdefaultencoding( "utf-8" )


def mappingPopulation(file):
    fs = codecs.open(file, 'w+', encoding='utf8')
    #fs.write("id;pi;pj;dij;fij" + "\r\n")
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                     charset=mod_config.dbcharset)
    cursor = db.cursor()
    queryUserCountSQL = 'select cname,population from city'
    cursor.execute(queryUserCountSQL)
    rows = cursor.fetchall()
    userCountMap = {}
    for row in rows:
        key = str(row[0])
        userCountMap[key] = row[1]
        fs.write("{name:'" +key+"',value:"+str(row[1])+ "},\r\n")
        #{name: '齐齐哈尔', value: 14},
    fs.close()

def mappingPenetarte(readFile,writeFile):
    ifs = codecs.open(readFile, 'r+', encoding='utf8')
    ofs = codecs.open(writeFile, 'w+', encoding='utf8')
    lines = ifs.readlines()
    for line in lines:
        line = line.strip('\r\n')
        items = string.split(line, '\t')

        print items[0], items[1], items[2], items[3]
        ofs.write("{name:'" + items[0] + "',value:" + str(float(items[3])*10000) + "},\r\n")
        # {name: '齐齐哈尔', value: 14},
    ofs.close()

pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
print pwd

# populationFile = pwd + '\\population.txt'
# mappingPopulation(populationFile)

penetrateInFile = pwd +'\\penetrateIn.txt'
penetrateOutFile = pwd +'\\penetrate.txt'
mappingPenetarte(penetrateInFile, penetrateOutFile)