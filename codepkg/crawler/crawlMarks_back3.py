# encoding: UTF-8

import json
import string
import time
import urllib2

import MySQLdb

from codepkg import mod_config
from sgmllib import SGMLParser
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

# BASE_URL='https://lvyou.baidu.com'
# BASE_URL_USER = "https://lvyou.baidu.com/gugong/remark"
# "https://lvyou.baidu.com/user/ajax/remark/getsceneremarklist?xid=6208c401f1153f0fd41f74fe&score=0&pn=0&rn=15&style=hot&format=ajax&flag=1&t=1487127343546"
def getReMarksCount(url):
    req = urllib2.Request(url)
    res_data = urllib2.urlopen(req)
    html = res_data.read()
    soup = BeautifulSoup(html,'html.parser')
    #print soup.prettify()
    countTag = soup.select('[class="scene-rating-counts nslog nslog-show"]')

    countStr = countTag[0].get_text()
    countStr = str(countStr)
    digitIndex = countStr.find('条点评')
    if digitIndex == -1:
        return 0
    count = countStr[0:digitIndex]
    # print count
    return count


def getUsers():
    try:
        insertUserSQL = "insert into user(uid,userindex,uname,obode,status,finish,createtime,updatetime) values(%s, %s, %s, %s, %s, %s, %s, %s)"
        db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                             charset='utf8')
        cursor = db.cursor()

        queryAllUidsSQL = "select uid from user"
        cursor.execute(queryAllUidsSQL)
        uidResults = cursor.fetchall()
        for row in uidResults:
            uidSet.add(row[0])

        getAllCitySQL = 'select ename,city,cname from spot where status = 0'
        cursor.execute(getAllCitySQL)
        results = cursor.fetchall()
        current_spot_index = 1
        for row in results:
            url = 'https://lvyou.baidu.com/'+row[0]+'/remark'
            start = 0
            print 'get total count of '+row[0],url
            end = int(getReMarksCount(url))

            offset = 100
            i = 1
            BASE_MARK_URL = url
            while start<end:
                url = BASE_MARK_URL +'?rn='+str(offset)+'&pn='+str(start)+'&style=hot#remark-container'
                print url,end
                #time.sleep(1)
                req = urllib2.Request(url)
                res_data = urllib2.urlopen(req)
                html = res_data.read()
                soup = BeautifulSoup(html, 'html.parser')
                #print soup.prettify()
                remarkItems = soup.select('[class="ri-uname"]')
                values = []
                for item in remarkItems:
                    #remarkItems[i].
                    uname = item['title']
                    userindex = item['href']
                    userindex = str(userindex)
                    uidIndex = userindex.find('/user/')
                    uid = userindex[6:]
                    now = int(time.time())
                    timeArray = time.localtime(now)
                    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    #print  i,uid,userindex,uname
                    i += 1

                    if uid not in uidSet:
                        value=(uid, userindex, uname, '', 1, 0, otherStyleTime, otherStyleTime)
                        values.append(value)
                        #cursor.execute(insertUserSQL,(uid, userindex, uname, '',  otherStyleTime, otherStyleTime))
                        #db.commit()
                        uidSet.add(uid)
                cursor.executemany(insertUserSQL, values)
                db.commit()
                start+=offset
            print 'current_spot_index='+str(current_spot_index),row[1],'-',row[2],getReMarksCount(url)
            current_spot_index+=1
            updateSQL = 'update spot set status = 1 where ename = "'+row[0]+'"'
            cursor.execute(updateSQL)
            db.commit()
    except Exception,msg:
        db.rollback()
        print msg
        getUsers()

def crawlNotes():
    try:
        db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                             charset='utf8')
        cursor = db.cursor()
        queryAllUidsSQL = "select uid from user where finish = 1 "
        cursor.execute(queryAllUidsSQL)
        uidResults = cursor.fetchall()

        searchSQL = "select uid from user where status = 1 and finish = 0 limit 3000,1000"
        insertSpotTravelSQL = "insert into spottravel(userid,fromcity,toprovince,toecity,toccity,toespot,tocspot,createtime,updatetime) values(%s, %s, %s, %s,%s, %s, %s, %s, %s)"

        cursor.execute(searchSQL)
        rows = cursor.fetchall()
        FOOTPRINT_BASE_URL = 'https://lvyou.baidu.com/user/footprint/'

        index = 1 + len(uidResults)
        for row in rows:
            if row[0] in uidSet:
                continue

            now = int(time.time())
            timeArray = time.localtime(now)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

            uidSet.add(row[0])
            footPrintURL = FOOTPRINT_BASE_URL+row[0]
            print otherStyleTime,str(index),"uid=",row[0],footPrintURL

            req = urllib2.Request(footPrintURL)
            res_data = urllib2.urlopen(req)
            html = res_data.read()
            soup = BeautifulSoup(html, 'html.parser')
            # personalInfo = soup.select('[class="personal-info"]')
            # if len(personalInfo) == 0:
            #     updateSQL = "update user set obode='用户不存在',finish = 1, status = 0 where uid = '" + row[0] + "'"
            #     cursor.execute(updateSQL)
            #     db.commit()
            #     continue
            # obode = personalInfo[0].span.get_text()
            # obode = obode.strip()[4:]
            #if obode == '未填':
            #    continue
            #print str(index),'常住地:',obode,"uid=",row[0],footPrintURL
            index += 1
            #insertCityTravleValues = []
            insertSpotTravleValues = []

            chinaList = soup.select('[class="china-list"]')
            if chinaList == None or len(chinaList) <=0:
                updateSQL = "update user set finish = 1 where uid = '" + row[0] + "'"
                cursor.execute(updateSQL)
                db.commit()
                continue
            footprintList = chinaList[0].select('[class="footprint-list"]')
            footprintList = footprintList[0].find_all("div", attrs={"class": "footprint-item"})
            #footprintList = footprintList.select('[class="footprint-item"]')

            toProvince=''
            toECity=''
            toCCity = ''
            toESpot=''
            toCSpot = ''
            for footprint in footprintList:
                provinceTag = footprint.find("a", attrs={"class": "parent-sname"})
                toProvince = provinceTag.get_text()

                clearfixFootprintParentDiv = footprint.find("div")
                citylistTag = clearfixFootprintParentDiv.find_all("div")

                for cityTag in citylistTag:
                    cityDataTag = cityTag.find("div",attrs={"class": "footprint-data"})
                    if cityDataTag != None:
                        cityDataA = cityDataTag.find("a",attrs={"class": "sub-sname"})
                        toECity = cityDataA.attrs['href'][1:]
                        toCCity = cityDataA.get_text()
                        #print '省份:',toProvince,'城市',toECity,toCCity

                        #insertCityTravleValue = (row[0], obode, toProvince, toECity, toCCity, otherStyleTime, otherStyleTime)
                        #insertCityTravleValues.append(insertCityTravleValue)

                    sceneCardListTag = cityTag.find("div",attrs={"class": "scene-card-list"})
                    if sceneCardListTag != None:
                        sceneCardListDivs = sceneCardListTag.find_all("div",attrs={"class": "scene-card"})
                        for sceneCardDiv in sceneCardListDivs:
                            #print sceneCardDiv
                            toESpotTag = sceneCardDiv.find("a")
                            toCSpotTag = sceneCardDiv.find("div", attrs={"class": "scene-sname"})
                            if toESpotTag != None and toCSpotTag != None:
                                toESpot = toESpotTag.attrs['href']
                                toCSpot = toCSpotTag.get_text()
                                #print '景点',toESpot,toCSpot
                                insertSpotTravleValue = (row[0], '', toProvince, toECity, toCCity,toESpot,toCSpot, otherStyleTime, otherStyleTime)
                                insertSpotTravleValues.append(insertSpotTravleValue)
            # cursor.executemany(insertCityTravleSQL,insertCityTravleValues)
            # db.commit()
            cursor.executemany(insertSpotTravelSQL, insertSpotTravleValues)
            db.commit()
            updateSQL = "update user set finish = 1 where uid = '" + row[0] + "'"
            cursor.execute(updateSQL)
            db.commit()
    except Exception,msg:
        db.rollback()
        print msg
        updateSQL = "update user set status = -1,finish = 1 where uid = '" + row[0] + "'"
        cursor.execute(updateSQL)
        db.commit()
        crawlNotes()

uidSet = set()
urlset = set()
if __name__ == '__main__':
    #getUsers()
    crawlNotes()