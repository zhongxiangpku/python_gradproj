import os
import MySQLdb
import codecs
import string

def readfile(file):
    os.chdir('C:\Users\dell\Desktop')
    fs = codecs.open(file, encoding='gbk')
    lines = fs.readlines()
    fs.close()
    mysql = "update note set departure = %s where departure = %s"
    db = MySQLdb.connect('127.0.0.1', 'root', 'admin', 'pythondb', charset="gbk")
    cursor = db.cursor()
    try:
        for line in lines:
            line = line.strip('\r\n')
            items = string.split(line, ',')
            #print items[0],items[1]
            mysql = "update note set departure ='"+items[1]+"' where departure ='"+items[0]+ "';"
            print mysql
            #cursor.execute(mysql)
            #db.commit()
    except Exception,e:
        print Exception,":",e
       #db.rollback()
    #db.close()
    # for line in lines:
    #     # print line
    #     items = string.split(line, ',')
    #     print items[0], items[1]


file = 'errorcityname2.csv'
readfile(file)