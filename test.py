import os
import codecs
import string

import xlwt
from datetime import datetime

style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    num_format_str='#,##0.00')
style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet')

ws.write(0, 0, 1234.56, style0)
ws.write(1, 0, datetime.now(), style1)
ws.write(2, 0, 1)
ws.write(2, 1, 1)
ws.write(2, 2, xlwt.Formula("A3+B3"))

wb.save('example.xls')

# print os.getcwd()
#
# pwd = os.getcwd()
# pwd = pwd + '\\Datas'
#
# for i in os.listdir(pwd):
#     if os.path.isfile(os.path.join(pwd,i)):
#         print pwd+"\\"+i
#
# mymap = {}
# s= []
# s.append(1)
# s.append(2)
# mymap['url'] = s
# mymap['url'].append(3)
# if 'url' in mymap.keys():
#     print mymap['url']
# print mymap
#
# lst = [1,2,3,4,5]
# for i in range(0,len(lst)):
#     for j in range(i+1,len(lst)):
#         print lst[i], lst[j]


# filein = "C:\Users\dell\Desktop\input.txt"
# fileout = "C:\Users\dell\Desktop\output.txt"
#
# def readfile(filein, fileout):
#     os.chdir('C:\Users\dell\Desktop')
#     map = {}
#     fs = codecs.open(filein, encoding='gbk')
#     fs2 = codecs.open(fileout,'w+', encoding='gbk')
#     lines = fs.readlines()
#     fs.close()
#     try:
#         for line in lines:
#             line = line.strip('\r\n')
#             items = string.split(line, ';')
#             key = str(items[0])
#             value = int(items[1])
#             print key, value
#             if(key not in map.keys()):
#                 map[key] = value
#             else:
#                 map[key] += value
#         for key, value in map.items():
#             fs2.write(key + "," + str(value) + "\r\n")
#         fs2.close()
#     except Exception, e:
#         print Exception, ":", e
#
# readfile(filein,fileout)




