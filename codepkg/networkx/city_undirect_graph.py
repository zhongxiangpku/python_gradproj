#coding=utf-8

import networkx as nx
from networkx import *
import os
import matplotlib.pyplot as plt
import codecs
import string

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

def createDistNetwork(file):
    fs = codecs.open(file, encoding='utf-8')
    lines = fs.readlines()
    g = nx.Graph()
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

def computeBasicIndex(graph):
    print '---------------------------------------------------'
    print 'Graph name =',graph.name
    print '|V|=',len(graph.nodes())
    print '|E|=',len(graph.edges())
    print '<k>=',len(graph.edges()) *1.0 / len(graph.nodes())
    # print 'average clustering:', nx.average_clustering(graph)
    # print 'degree_assortativity_coefficient:', nx.degree_assortativity_coefficient(graph)
    # print 'average_neighbor_degree:', nx.average_neighbor_degree(graph)
    # print 'average_shortest_path_length', nx.average_shortest_path_length(graph)
    print '---------------------------------------------------'
pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
#不考虑地理距离建网络
undirectCityEdgeFile = pwd + '\\Datas\\Edge_datas\\undirectCityEdges_rse.txt'
directCityEdgeFile = pwd + '\\Datas\\Edge_datas\\directCityEdges_rse.txt'
undirectSpotEdgeFile = pwd + '\\Datas\\Edge_datas\\undirectSpotEdges_rse.txt'
directSpotEdgeFile = pwd + '\\Datas\\Edge_datas\\directSpotEdges_rse.txt'
undirect_city_network = createNetwork('非地理无向城市网络', undirectCityEdgeFile)
direct_city_network = createNetwork('非地理有向城市网络',directCityEdgeFile)
undirect_spot_network = createNetwork('非地理无向景点网络',undirectSpotEdgeFile)
direct_spot_network = createNetwork('非地理有向景点网络',directSpotEdgeFile)
computeBasicIndex(undirect_city_network)
computeBasicIndex(direct_city_network)
computeBasicIndex(undirect_spot_network)
computeBasicIndex(direct_spot_network)

#考虑地理距离作为边权建网络
undirectCityDistEdgeFile = pwd + '\\Datas\\Edge_datas\\undirectCityEdges_dist_rse.txt'
directCityDistEdgeFile = pwd + '\\Datas\\Edge_datas\\directCityEdges_dist_rse.txt'
undirectSpotDistEdgeFile = pwd + '\\Datas\\Edge_datas\\undirectSpotEdges_dist_rse.txt'
directSpotDistEdgeFile = pwd + '\\Datas\\Edge_datas\\directSpotEdges_dist_rse.txt'
undirect_city_dist_network = createNetwork('地理无向城市网络',undirectCityDistEdgeFile)
direct_city_dist_network = createNetwork('地理有向城市网络',directCityDistEdgeFile)
undirect_spot_dist_network = createNetwork('地理无向景点网络',undirectSpotDistEdgeFile)
direct_spot_dist_network = createNetwork('地理有向景点网络',directSpotDistEdgeFile)
computeBasicIndex(undirect_city_dist_network)
computeBasicIndex(direct_city_dist_network)
computeBasicIndex(undirect_spot_dist_network)
computeBasicIndex(direct_spot_dist_network)

