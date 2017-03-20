# encoding: UTF-8

import codecs
import math
import os
import sys

import MySQLdb

from codepkg import mod_config
import codepkg.data_process.geoutil

reload(sys)
sys.setdefaultencoding( "utf-8" )
import networkx as nx                   #导入NetworkX包，为了少打几个字母，将其重命名为nx
import matplotlib.pyplot as plt         #导入绘图包matplotlib
import string

def getGraphEdgeSet(outputFile):
    db = MySQLdb.connect(mod_config.dbhost, mod_config.dbuser, mod_config.dbpassword, mod_config.dbname,
                         charset=mod_config.dbcharset)
    cursor = db.cursor()
    mysql = 'select fromcity,toccity,count(*) as frenquency from citytravel where fromcity!=toccity GROUP BY  fromcity,toccity having count(*)>=10'
    cursor.execute(mysql)
    results = cursor.fetchall()
    edgeMap = {}

    # mysql = 'select cname from city where cname != "神农架林区" and usercount>=20 and usercount * 1.0 /(population *100) > 0.001'

    for row in results:
        start = str(row[0])
        end = str(row[1])
        freq = int(row[2])

        key1 = start + ";"+end
        key2 = end + ";"+start
        if key1 not in edgeMap.keys() and key2 not in edgeMap.keys():
            edgeMap[key1] = freq
        elif key1 not in edgeMap.keys() and key2  in edgeMap.keys():
            edgeMap[key2] = edgeMap[key2]  + freq
        elif key1 in edgeMap.keys() and key2 not in edgeMap.keys():
            edgeMap[key1] = edgeMap[key1]  + freq
        else:
            print 'process error!'

    fs = codecs.open(outputFile, 'w+', encoding='utf8')
    #fs.write("start;frequency")
    for k, v in edgeMap.items():
        print k, v
        fs.write(k+";"+str(v)+"\r\n")
    fs.flush()
    fs.close()

#根据边文件构建不带地理距离加权的网络（城市－景点，有向－无向）
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
            items = string.split(line,';')
            if items[0] == items[1]:
                continue
            g.add_edge(items[0],items[1],weight=int(items[2]))
    except Exception,msg:
        print msg
    return g

'''
计算网络的基本指标，包括:
    节点数，边数， 平均度， 平均聚集系数， 平均最短路径
    同配性指数
'''
def computeBasicIndex(graph):
    print '---------------------------------------------------'
    print 'Graph name =', graph.name
    nodes = len(graph.nodes())
    edges = len(graph.edges())
    print '|V|=', len(graph.nodes())
    print '|E|=', len(graph.edges())
    print '<k>=', len(graph.edges()) *1.0 / len(graph.nodes())

    randomGraph = nx.dense_gnm_random_graph(nodes, edges)
    print 'average_shortest_path_length', nx.average_shortest_path_length(graph)
    print '随机网络average_shortest_path_length of random graph with same node number and edge number', nx.average_shortest_path_length(randomGraph)

    #print 'average clustering:', nx.average_clustering(graph)
    #print '随机网络average clustering of random graph with same node number and edge number :', nx.average_clustering(randomGraph)
    if nx.is_directed(graph):
        un_digraph = graph.to_undirected()
        print 'average clustering:', nx.average_clustering(un_digraph)
        un_randomdiGraph = randomGraph.to_undirected()
        print '随机网络average clustering of random graph with same node number and edge number :', nx.average_clustering(
            randomGraph)
    else:
        print 'average clustering:', nx.average_clustering(graph)
        print '随机网络average clustering of random graph with same node number and edge number :', nx.average_clustering(randomGraph)
    print 'degree_assortativity_coefficient:', nx.degree_assortativity_coefficient(graph)
    # print 'average_neighbor_degree:', nx.average_neighbor_degree(graph)
    print '---------------------------------------------------'

#计算中心性，包括度中心性，中介中心性，邻近中心性以及边中介中心性
def computeCentrality(graph,node_degree_centrality_file, node_betweenness_centrality_file, node_closeness_centrality_file, edge_betweenness_centrality_file):
    ndcfs = codecs.open(node_degree_centrality_file, 'w+', encoding='utf-8')
    nbcfs = codecs.open(node_betweenness_centrality_file, 'w+', encoding='utf-8')
    nccfs = codecs.open(node_closeness_centrality_file, 'w+', encoding='utf-8')
    ebcfs = codecs.open(edge_betweenness_centrality_file, 'w+', encoding='utf-8')

    #计算节点度中心性
    nodeDegreeCentrality = nx.degree_centrality(graph)
    print graph, 'nodes degree centrality as follows:'
    print nodeDegreeCentrality
    for (key, value) in nodeDegreeCentrality.items():
        ndcfs.write(key+','+str(value)+'\r\n')
    ndcfs.flush()
    ndcfs.close()

    # 计算节点中介中心性
    nodeBetweennessCentrality = nx.betweenness_centrality(graph)
    print graph, 'nodes betweenness centrality as follows:'
    print nodeBetweennessCentrality
    for (key, value) in nodeBetweennessCentrality.items():
        nbcfs.write(key+','+str(value)+'\r\n')
    nbcfs.flush()
    nbcfs.close()

    # 计算节点介中心性
    nodeClosenessCentrality = nx.closeness_centrality(graph)
    print graph, 'nodes closeness centrality as follows:'
    print nodeClosenessCentrality
    for (key, value) in nodeClosenessCentrality.items():
        nccfs.write(key+','+str(value)+'\r\n')
    nccfs.flush()
    nccfs.close()

    # 计算边度中心性
    edgeBetweennessCentrality = nx.edge_betweenness_centrality(graph)
    print graph, 'edges betweenness centrality as follows:'
    print edgeBetweennessCentrality
    for (key, value) in edgeBetweennessCentrality.items():
        ebcfs.write(key[0]+','+key[1]+','+str(value)+'\r\n')
    ebcfs.flush()
    ebcfs.close()


pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
#不考虑地理距离建网络
cityGraphEdgeSetFile2 = pwd + '/Datas/Edge_datas/cityGraphEdgeSet2.txt'
getGraphEdgeSet(cityGraphEdgeSetFile2)

graph  = createNetwork("城市交互网络模型",False,cityGraphEdgeSetFile2)
computeBasicIndex(graph)

