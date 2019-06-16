import numpy as np
import random
import copy
import matplotlib.pyplot as plt
import networkx as nx


class Node():
    def __init__(self, is_iNode = False, is_oNode = False, iConn = None, val=0, outVal = None):
        self.is_iNode = is_iNode;
        self.is_oNode = is_oNode;
        
        
        if iConn == None: self.iConn = [];
        else: self.iConn = iConn
        
        self.val = val;
        if outVal == None: self.outVal = val;
        else: self.outVal = outVal
    
    def addInput(self, inNode, weight=None):
        if weight == None: weight = random.uniform(-1, 1)
        self.iConn += [(inNode, weight)]
        return

    def updateVal(self):
        newVal = 0.
        total_weight = 0.
        for connection in self.iConn:
            if not  connection[0].is_iNode: newVal += connection[0].outVal*connection[1]
            else: newVal += connection[0].val*connection[1]
            
            total_weight += connection[1]

        #self.val = newVal
        self.val = (newVal/float(len(self.iConn)))

    def updateOutVal(self):
        self.outVal = self.val

class Network():
    def __init__(self, iNodes_n=0, oNodes_n=0, hNodes_n=0, Nodes_n=0, iNodes=[], oNodes=[], hNodes = [], Nodes=[]):
        self.iNodes = []; self.oNodes = []; self.Nodes = []; self.hNodes = []
        for iNode in range(iNodes_n):
            tmpNode = Node(is_iNode=True)
            self.iNodes += [tmpNode]; self.Nodes += [tmpNode]
        
        for hNode in range(hNodes_n):
            tmpNode = Node(is_iNode=False, is_oNode=False)
            self.hNodes += [tmpNode]; self.Nodes += [tmpNode]
            for iNode in self.iNodes: self.hNodes[hNode].addInput(iNode, random.uniform(-1, 1))
        
        for oNode in range(oNodes_n):
            tmpNode = Node(is_oNode=True)
            self.oNodes += [tmpNode]; self.Nodes += [tmpNode]
            for iNode in self.iNodes: self.oNodes[oNode].addInput(iNode, random.uniform(-1,1))
            for hNode in self.hNodes: self.oNodes[oNode].addInput(hNode, random.uniform(-1,1))

    def updateNet(self):
        newNet = []
        for node in self.Nodes:
            if not node.is_iNode: node.updateVal()
        for node in self.Nodes:
            if not node.is_iNode: node.updateOutVal()

    def get_mutation(self, low=-2, high=2, iters=1, lr=1):
        mutation = copy.deepcopy(self)
        for node in mutation.Nodes:
            if node.is_iNode: continue
            for conn in range(len(node.iConn)):
                new_val = node.iConn[conn][1]+random.uniform(low/float(iters/lr), high/float(iters/lr))
                if new_val > 1: new_val=1
                if new_val < -1: new_val=-1
                node.iConn[conn] = (node.iConn[conn][0], new_val)

        return mutation

    def graph(self):
        fig = plt.gcf()
        fig.clear()
        G = nx.Graph()
        elements = {}
        for idx, iNode in enumerate(self.iNodes):
            x_pos = 0
            elements[iNode] = {'label': 'i'+str(idx), 'pos':(x_pos, 1-idx/len(self.iNodes))}
        
        for idx, hNode in enumerate(self.hNodes):
            x_pos = 0.5
            elements[hNode] = {'label': 'h'+str(idx), 'pos':(x_pos, 1-idx/len(self.hNodes))}
        
        for idx, oNode in enumerate(self.oNodes):
            x_pos = 1
            elements[oNode] = {'label': 'o'+str(idx), 'pos':(x_pos, 1-idx/len(self.oNodes))}
        
        MyEdges = []; MyColors = []; MyWidths = [];
        for idx, hNode in enumerate(self.hNodes):
            for conn in hNode.iConn:
                if(conn[1] < 0): nColor = 'r'
                else: nColor = 'b'
                G.add_edge(elements[conn[0]]['label'], 'h'+str(idx))
                MyEdges += [(elements[conn[0]]['label'], 'h'+str(idx))]
                MyColors += [nColor]
                MyWidths += [3*np.abs(conn[1])]
        
        for idx, oNode in enumerate(self.oNodes):
            for conn in oNode.iConn:
                if(conn[1] < 0): nColor = 'r'
                else: nColor = 'b'
                G.add_edge(elements[conn[0]]['label'], 'o'+str(idx))
                MyEdges += [(elements[conn[0]]['label'], 'o'+str(idx))]
                MyColors += [nColor]
                MyWidths += [3*np.abs(conn[1])]
        
        pos = {}
        for Node in elements:
            pos[elements[Node]['label']] = elements[Node]['pos']

        nx.draw_networkx_nodes(G, pos, node_size=700)
        nx.draw_networkx_edges(G, pos, edgelist=MyEdges, width=MyWidths, alpha=0.5, edge_color=MyColors)
        plt.axis('off')
        plt.show(block=False)
        fig.canvas.draw()
        fig.canvas.flush_events()


if __name__ == '__main__':
    myNet = Network(iNodes_n = 3, oNodes_n=2)
    myNet.iNodes[0].val = 0.;
    myNet.iNodes[1].val = 0.;
    myNet.iNodes[2].val = 1.;
    
    myNet.oNodes[0].addInput(myNet.oNodes[0])
    myNet.oNodes[1].addInput(myNet.oNodes[1])
    
    myNet.oNodes[0].addInput(myNet.oNodes[1])
    myNet.oNodes[1].addInput(myNet.oNodes[0])

    for iconn in myNet.oNodes[0].iConn:
        print(iconn[1])

    print('mutate'); myNet = myNet.get_mutation()

    for iconn in myNet.oNodes[0].iConn:
        print(iconn[1])
