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
                print('(%s, %s, %.3f)' % (n, nbr, data))
    except Exception,msg:
        print msg
    return g

pwd = os.getcwd()
pwd = os.path.dirname(pwd)
pwd = os.path.dirname(pwd)
undirectCityEdgeFile = pwd + '\\Datas\\rsa_datas\\undirectCityEdges_rse.txt'

G = createNetwork(undirectCityEdgeFile)
print len(G.nodes()),len(G.edges())
print 'average clustering:',nx.average_clustering(G)
print 'degree_assortativity_coefficient:',nx.degree_assortativity_coefficient(G)
print 'average_neighbor_degree:',nx.average_neighbor_degree(G)
print 'average_shortest_path_length',nx.average_shortest_path_length(G)

ERG = nx.random_graphs.erdos_renyi_graph(20,0.2)
#print 'graph_clique_number',nx.number_of_cliques(G)
degree =  nx.degree_histogram(G)
x = range(len(degree))
y = [z / float(sum(degree)) for z in degree]
plt.loglog(x,y,color="blue",linewidth=2)
#plt.show()

# nx.draw(G)
# plt.show()

directCityEdgeFile = pwd + '\\Datas\\rsa_datas\\directCityEdges_rse.txt'
DG = createNetwork(directCityEdgeFile)
print len(DG.nodes()),len(DG.edges())
print 'average clustering:',nx.average_clustering(DG)
print 'degree_assortativity_coefficient:',nx.degree_assortativity_coefficient(DG)
print 'average_neighbor_degree:',nx.average_neighbor_degree(DG)
print 'average_shortest_path_length',nx.average_shortest_path_length(DG)
#print 'graph_clique_number',nx.number_of_cliques(DG)
# nx.draw(DG)
# plt.show()
