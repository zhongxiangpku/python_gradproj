#coding=utf-8

import networkx as nx
from networkx import *
import os
import matplotlib.pyplot as plt
import codecs
import string

#根据边文件构建不带地理距离加权的网络（城市－景点，有向－无向）
def createNetwork(gname, file):
    #os.chdir('C:\Users\dell\Desktop')
    fs = codecs.open(file, encoding='utf-8')
    lines = fs.readlines()
    g = nx.Graph(name = gname)
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

#根据边文件构建带地理距离加权的网络（城市－景点，有向－无向）
def createDistNetwork(gname, file):
    fs = codecs.open(file, encoding='utf-8')
    lines = fs.readlines()
    g = nx.Graph(name = gname)
    try:
        for line in lines:
            line = line.strip('\r\n')
            items = string.split(line, ',')
            if items[0] == items[1]:
                continue
            g.add_edge(items[0], items[1], weight=int(items[4]))
        for n, nbrs in g.adjacency_iter():
            for nbr, eattr in nbrs.items():
                data = eattr['weight']
                print('(%s, %s, %.3f)' % (n, nbr, data))
    except Exception, msg:
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

#计算knn
def computeKnn(graph, knn_file,weight=None):
    G = nx.path_graph(4)
    G.edge[1][2]['weight'] = 3
    print nx.k_nearest_neighbors(G)
    knnfs = codecs.open(knn_file, 'w+', encoding='utf-8')
    knn = nx.average_degree_connectivity(graph)
    print graph, 'knn as follows:'
    print knn
    for (key, value) in knn.items():
        knnfs.write(str(key)+ ',' + str(value) + '\r\n')
    knnfs.flush()
    knnfs.close()







pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
#不考虑地理距离建网络
undirectCityEdgeFile = pwd + '/Datas/Edge_datas/undirectCityEdges_rse.txt'
directCityEdgeFile = pwd + '/Datas/Edge_datas/directCityEdges_rse.txt'
undirectSpotEdgeFile = pwd + '/Datas/Edge_datas/undirectSpotEdges_rse.txt'
directSpotEdgeFile = pwd + '/Datas/Edge_datas/directSpotEdges_rse.txt'
undirect_city_network = createNetwork('非地理无向城市网络', undirectCityEdgeFile)
# direct_city_network = createNetwork('非地理有向城市网络',directCityEdgeFile)
# undirect_spot_network = createNetwork('非地理无向景点网络',undirectSpotEdgeFile)
# direct_spot_network = createNetwork('非地理有向景点网络',directSpotEdgeFile)
computeBasicIndex(undirect_city_network)
# computeBasicIndex(direct_city_network)
# computeBasicIndex(undirect_spot_network)
# computeBasicIndex(direct_spot_network)

#计算中心性
# node_degree_centrality_file= pwd +'/Datas/Centrality_datas/cityUndirectEdge_nodeDegreeCentralityFile.txt'
# node_betweenness_centrality_file= pwd +'/Datas/Centrality_datas/cityUndirectEdge_nodeBetweennessCentralityFile.txt'
# node_closeness_centrality_file= pwd +'/Datas/Centrality_datas/cityUndirectEdge_nodeClosenessCentralityFile.txt'
# edge_betweenness_centrality_file= pwd +'/Datas/Centrality_datas/cityUndirectEdge_edgeBetweennessCentralityFile.txt'
# computeCentrality(undirect_city_network,
#                   node_degree_centrality_file,
#                   node_betweenness_centrality_file,
#                   node_closeness_centrality_file,
#                   edge_betweenness_centrality_file)


#计算knn
# cityUndirectEdge_knn_file= pwd +'\\Datas\\knn_datas\\cityUndirectEdge_knnFile.txt'
# computeKnn(undirect_city_network, cityUndirectEdge_knn_file)














#考虑地理距离作为边权建网络
# undirectCityDistEdgeFile = pwd + '/Datas/Edge_datas/undirectCityEdges_dist_rse.txt'
# directCityDistEdgeFile = pwd + '/Datas/Edge_datas/directCityEdges_dist_rse.txt'
# undirectSpotDistEdgeFile = pwd + '/Datas/Edge_datas/undirectSpotEdges_dist_rse.txt'
# directSpotDistEdgeFile = pwd + '/Datas/Edge_datas/directSpotEdges_dist_rse.txt'
# undirect_city_dist_network = createNetwork('地理无向城市网络',undirectCityDistEdgeFile)
# direct_city_dist_network = createNetwork('地理有向城市网络',directCityDistEdgeFile)
# undirect_spot_dist_network = createNetwork('地理无向景点网络',undirectSpotDistEdgeFile)
# direct_spot_dist_network = createNetwork('地理有向景点网络',directSpotDistEdgeFile)
# computeBasicIndex(undirect_city_dist_network)
# computeBasicIndex(direct_city_dist_network)
# computeBasicIndex(undirect_spot_dist_network)
# computeBasicIndex(direct_spot_dist_network)

