import os
import codecs
import string

def remove_samenode_file(source, target):
    sourcefs = codecs.open(source, encoding='utf-8')
    targetfs = codecs.open(target, 'w+', encoding='utf-8')
    lines = sourcefs.readlines()
    sourcefs.close()
    try:
        index = 1
        print "lines size:", len(lines)
        for line in lines:
            print index, line
            line = line.strip('\r\n')
            items = string.split(line, ',')
            if items[0] == items[1]:
                continue

            targetfs.write(items[0] + "," + items[1] + ", " + items[2] + "\r\n")
            index += 1
        targetfs.flush()
        targetfs.close()
    except Exception, e:
        print Exception, ":", e


pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
print pwd

source_cityUndirectEdgeFile = pwd + '/Datas/undirectCityEdges.txt'
source_cityDirectEdgeFile = pwd+'/Datas/directCityEdges.txt'
source_spotUndirectEdgeFile = pwd+'/Datas/undirectSpotEdges.txt'
source_spotDirectEdgeFile = pwd+'/Datas/directSpotEdges.txt'

target_cityUndirectEdgeFile = pwd + '/Datas/undirectCityEdges_rse.txt'
target_cityDirectEdgeFile = pwd+'/Datas/directCityEdges_rse.txt'
target_spotUndirectEdgeFile = pwd+'/Datas/undirectSpotEdges_rse.txt'
target_spotDirectEdgeFile = pwd+'/Datas/directSpotEdges_rse.txt'

remove_samenode_file(source_cityUndirectEdgeFile, target_cityUndirectEdgeFile)
remove_samenode_file(source_cityDirectEdgeFile, target_cityDirectEdgeFile)
remove_samenode_file(source_spotUndirectEdgeFile, target_spotUndirectEdgeFile)
remove_samenode_file(source_spotDirectEdgeFile, target_spotDirectEdgeFile)
