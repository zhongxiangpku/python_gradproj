import networkx as nx
import os
import matplotlib.pyplot as plt

class man():
    @staticmethod
    def mans():
        print 'i am a man!'

    def setsize(self,size):
        self.size = size

    def getsize(self):
        return self.size

    Size = property(getsize, setsize)

myman = man()
myman.size = 10
print myman.size
man().mans()

print os.getcwd()
G = nx.random_graphs.barabasi_albert_graph(30,1)
nx.draw(G)
plt.savefig("ba.png")
plt.show()    