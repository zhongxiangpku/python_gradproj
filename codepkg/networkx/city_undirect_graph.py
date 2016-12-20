#coding=utf-8

import networkx as nx
from networkx import *
import os
import matplotlib.pyplot as plt
import codecs
import string

def createNetwork(file):
    #os.chdir('C:\Users\dell\Desktop')
    fs = codecs.open(file, encoding='utf-8')
    lines = fs.readlines()
    g = nx.Graph()
    try:
        for line in lines:
            line = line.strip('\r\n')
            items = string.split(line,',')
            if items[0] == items[1]:
                continue
            g.add_edge(items[0],items[1],weight=int(items[2]))
        for n, nbrs in g.adjacency_iter():
            for nbr, eattr in nbrs.items():
                data = eattr['weight']
               #print('(%s, %s, %.3f)' % (n, nbr, data))
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
    print 'Graph name =',graph.name,graph
    print '|V|=',len(graph.nodes())
    print '|E|=',len(graph.edges())
    #print '<k>=',
    print 'average clustering:', nx.average_clustering(graph)
    print 'degree_assortativity_coefficient:', nx.degree_assortativity_coefficient(graph)
    print 'average_neighbor_degree:', nx.average_neighbor_degree(graph)
    print 'average_shortest_path_length', nx.average_shortest_path_length(graph)

pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
#不考虑地理距离建网络
undirectCityEdgeFile = pwd + '\\Datas\\rsa_datas\\undirectCityEdges_rse.txt'
directCityEdgeFile = pwd + '\\Datas\\rsa_datas\\directCityEdges_rse.txt'
undirectSpotEdgeFile = pwd + '\\Datas\\rsa_datas\\undirectSpotEdges_rse.txt'
directSpotEdgeFile = pwd + '\\Datas\\rsa_datas\\directSpotEdges_rse.txt'
# undirect_city_network = createNetwork(undirectCityEdgeFile)
# direct_city_network = createNetwork(directCityEdgeFile)
# undirect_spot_network = createNetwork(undirectSpotEdgeFile)
# direct_spot_network = createNetwork(directSpotEdgeFile)
# computeBasicIndex(undirect_city_network)
# computeBasicIndex(direct_city_network)
# computeBasicIndex(undirect_spot_network)
# computeBasicIndex(direct_spot_network)

#考虑地理距离作为边权建网络
undirectCityDistEdgeFile = pwd + '\\Datas\\dist_datas\\undirectCityEdges_dist_rse.txt'
directCityDistEdgeFile = pwd + '\\Datas\\dist_datas\\directCityEdges_dist_rse.txt'
undirectSpotDistEdgeFile = pwd + '\\Datas\\dist_datas\\undirectSpotEdges_dist_rse.txt'
directSpotDistEdgeFile = pwd + '\\Datas\\dist_datas\\directSpotEdges_dist_rse.txt'
undirect_city_dist_network = createNetwork(undirectCityDistEdgeFile)
direct_city_dist_network = createNetwork(directCityDistEdgeFile)
undirect_spot_dist_network = createNetwork(undirectSpotDistEdgeFile)
direct_spot_dist_network = createNetwork(directSpotDistEdgeFile)
# computeBasicIndex(undirect_city_dist_network)
# computeBasicIndex(direct_city_dist_network)
computeBasicIndex(undirect_spot_dist_network)
# computeBasicIndex(direct_spot_dist_network)

# G = createNetwork(undirectCityEdgeFile)
# print len(G.nodes()),len(G.edges())
# print 'average clustering:',nx.average_clustering(G)
# print 'degree_assortativity_coefficient:',nx.degree_assortativity_coefficient(G)
# print 'average_neighbor_degree:',nx.average_neighbor_degree(G)
# print 'average_shortest_path_length',nx.average_shortest_path_length(G)
# KD = nx.all_pairs_node_connectivity(G)
# for key,value in KD.items():
#     print key, value
#
# ERG = nx.random_graphs.erdos_renyi_graph(20,0.2)
# #print 'graph_clique_number',nx.number_of_cliques(G)
# degree =  nx.degree_histogram(G)
# x = range(len(degree))
# y = [z / float(sum(degree)) for z in degree]
# plt.loglog(x,y,color="blue",linewidth=2)
# #plt.show()
#
# # nx.draw(G)
# # plt.show()
#
# directCityEdgeFile = pwd + '\\Datas\\rsa_datas\\directCityEdges_rse.txt'
# DG = createNetwork(directCityEdgeFile)
# print len(DG.nodes()),len(DG.edges())
# print 'average clustering:',nx.average_clustering(DG)
# print 'degree_assortativity_coefficient:',nx.degree_assortativity_coefficient(DG)
# print 'average_neighbor_degree:',nx.average_neighbor_degree(DG)
# print 'average_shortest_path_length',nx.average_shortest_path_length(DG)
# #print 'graph_clique_number',nx.number_of_cliques(DG)
# # nx.draw(DG)
# # plt.show()
