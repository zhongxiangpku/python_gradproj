import os
import codecs
import string
# encoding: UTF-8

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


def remove_dist_samenode_file(source, target):
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

            targetfs.write(items[0] + "," + items[1] + ", " + items[2] + ", " + items[3]+ ", " + items[4]+ "\r\n")
            index += 1
        targetfs.flush()
        targetfs.close()
    except Exception, e:
        print Exception, ":", e

pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
print pwd

source_cityUndirectEdgeFile = pwd + '/Datas/nodist_datas/undirectCityEdges.txt'
source_cityDirectEdgeFile = pwd+'/Datas/nodist_datas/directCityEdges.txt'
source_spotUndirectEdgeFile = pwd+'/Datas/nodist_datas/undirectSpotEdges.txt'
source_spotDirectEdgeFile = pwd+'/Datas/nodist_datas/directSpotEdges.txt'

target_cityUndirectEdgeFile = pwd + '/Datas/nodist_datas/undirectCityEdges_rse.txt'
target_cityDirectEdgeFile = pwd+'/Datas/nodist_datas/directCityEdges_rse.txt'
target_spotUndirectEdgeFile = pwd+'/Datas/nodist_datas/undirectSpotEdges_rse.txt'
target_spotDirectEdgeFile = pwd+'/Datas/nodist_datas/directSpotEdges_rse.txt'

remove_samenode_file(source_cityUndirectEdgeFile, target_cityUndirectEdgeFile)
remove_samenode_file(source_cityDirectEdgeFile, target_cityDirectEdgeFile)
remove_samenode_file(source_spotUndirectEdgeFile, target_spotUndirectEdgeFile)
remove_samenode_file(source_spotDirectEdgeFile, target_spotDirectEdgeFile)




dist_source_cityUndirectEdgeFile = pwd + '/Datas/dist_datas/undirectCityEdges_dist.txt'
dist_source_cityDirectEdgeFile = pwd+'/Datas/dist_datas/directCityEdges_dist.txt'
dist_source_spotUndirectEdgeFile = pwd+'/Datas/dist_datas/undirectSpotEdges_dist.txt'
dist_source_spotDirectEdgeFile = pwd+'/Datas/dist_datas/directSpotEdges_dist.txt'

dist_target_cityUndirectEdgeFile = pwd + '/Datas/dist_datas/undirectCityEdges_dist_rse.txt'
dist_target_cityDirectEdgeFile = pwd+'/Datas/dist_datas/directCityEdges_dist_rse.txt'
dist_target_spotUndirectEdgeFile = pwd+'/Datas/dist_datas/undirectSpotEdges_dist_rse.txt'
dist_target_spotDirectEdgeFile = pwd+'/Datas/dist_datas/directSpotEdges_dist_rse.txt'

remove_dist_samenode_file(dist_source_cityUndirectEdgeFile, dist_target_cityUndirectEdgeFile)
remove_dist_samenode_file(dist_source_cityDirectEdgeFile, dist_target_cityDirectEdgeFile)
remove_dist_samenode_file(dist_source_spotUndirectEdgeFile, dist_target_spotUndirectEdgeFile)
remove_dist_samenode_file(dist_source_spotDirectEdgeFile, dist_target_spotDirectEdgeFile)
