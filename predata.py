#!/usr/bin/python
#coding=utf8

import MySQLdb
import os
import mod_config

def getCityPair():
    try:
        mysql = 'select  from spot where finish = 0'
        db = MySQLdb.connect(mod_config.dbhost,
                             mod_config.dbuser,
                             mod_config.dbpassword,
                             mod_config.dbname,
                             mod_config.dbcharset)
        cursor = db.cursor()
        cursor.execute(mysql)
        results = cursor.fetchall()
        index = 1
        for row in results:
            print str(index), row[2], row[1], row[3]
            getNote(row[3], row[2], row[1], 5000)
            mysql2 = 'update spot set finish = 1 where id = %s' % row[0]
            cursor.execute(mysql2)
            db.commit()
            index += 1
    except Exception, msg:
        # db.rollback()
        print msg