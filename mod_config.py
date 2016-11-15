#coding=utf8

import ConfigParser
import os

#获取config配置文件

def getConfig(section,key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0]+'/config.txt'
    print path
    config.read(path)
    return config.get(section, key)

dbhost = getConfig("database", "dbhost")
dbuser = getConfig("database", "dbuser")
dbpassword = getConfig("database", "dbpassword")
dbname = getConfig("database", "dbname")
dbcharset = getConfig("database", "dbcharset")