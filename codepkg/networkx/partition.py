#coding=utf-8

import networkx as nx
from networkx import *
import os
import matplotlib.pyplot as plt
import codecs
import string
import time
import matplotlib

# #根据边文件构建不带地理距离加权的网络（城市－景点，有向－无向）
def createNetwork(gname, directed,  file):
    #os.chdir('C:\Users\dell\Desktop')
    fs = codecs.open(file, encoding='utf-8')
    lines = fs.readlines()
    if directed:
        g = nx.DiGraph()
    else:
        g = nx.Graph(name=gname)
    try:
        for line in lines:
            line = line.strip('\r\n')
            items = string.split(line,',')
            if items[0] == items[1]:
                continue
            g.add_edge(items[0],items[1],weight=int(items[2]))
        # for n, nbrs in g.adjacency_iter():
        #     for nbr, eattr in nbrs.items():
        #         data = eattr['weight']
        #        print('(%s, %s, %.3f)' % (n, nbr, data))
    except Exception,msg:
        print msg
    return g
#
#
pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
undirectCityEdgeFile = pwd + '/Datas/Edge_datas/test.txt'


# c = list(nx.k_clique_communities(undirect_city_network, 4))
# for item in c:
#     print item
#



def find_community(graph,k):
    return list(nx.k_clique_communities(graph,k))

if __name__ == '__main__':
    wbNetwork = createNetwork('非地理无向城市网络', True, undirectCityEdgeFile)
    wbNetwork = wbNetwork.to_undirected()
    # if len(sys.argv) < 2:
    #     print "Usage: %s <InputEdgeListFile>" % sys.argv[0]
    #     sys.exit(1)

    #创建一个无向、无权图
    # edge_list_file = sys.argv[1]
    # wbNetwork = nx.read_edgelist(edge_list_file,delimiter='\t')
    print "图的节点数：%d" % wbNetwork.number_of_nodes()
    print "图的边数：%d" % wbNetwork.number_of_edges()

    #调用kclique社区算法
    print "############# k值: %d ################" % 50
    start_time = time.clock()
    rst_com = find_community(wbNetwork, 10)
    end_time = time.clock()
    print "计算耗时(秒)：%.3f" % (end_time - start_time)
    print "生成的社区数：%d" % len(rst_com)
    print rst_com
    # for k in xrange(3,100):
    #     print "############# k值: %d ################" % k
    #     start_time = time.clock()
    #     rst_com = find_community(wbNetwork,k)
    #     end_time = time.clock()
    #     print "计算耗时(秒)：%.3f" % (end_time-start_time)
    #     print "生成的社区数：%d" % len(rst_com)
