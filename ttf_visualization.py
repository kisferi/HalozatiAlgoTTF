import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import transfer_to_transfer as ttf
import time
from matplotlib.widgets import Button

class TTFVisualizer:
    index = 0
    node_colors = []
    node_labels = {}
    edeg_colors = []
    edges = []
    interactions = []

    def __init__(self, ttfObject):
        self.ttfObject = ttfObject

    def run_ttf(self):
        #setThe graph
        G = nx.Graph()
        G.add_nodes_from(range(0,self.ttfObject.numberOfAgents))
        node_positions = nx.spring_layout(G)
        
        #add all edges to the graph
        for i in range(self.ttfObject.numberOfAgents):
            for j in range(self.ttfObject.numberOfAgents):
                if(i<j):
                    G.add_edge(i,j)
                    self.edges.append((i,j))
                    self.edeg_colors.append('black')

        #turn on pyplot interactive mode
        plt.ion()
        while self.ttfObject.is_termination_configuration() != True:
            self.interactions.append(self.ttfObject.next_interaction())
            print('Current interaction: ', self.interactions[self.index])
            print('Number of interactions: ', self.index)
            
            #set the node colors
            self.set_node_colors()
            self.set_node_labels()
            self.set_sender_reciver_colors(self.index)
            self.set_interaction_edge_color(self.index)

            nx.draw(G, with_labels=True, node_color = self.node_colors, pos = node_positions, labels = self.node_labels, edge_color = self.edeg_colors)

            if not self.ttfObject.is_termination_configuration():
                plt.pause(0.5)
                plt.show()
                plt.clf()
            else:
                print("Done")
                plt.show(block=True)
            #increase the interactions number
            self.index += 1

    def set_node_colors(self):
        #set the node colors and positions
        self.node_colors = []
        self.node_colors=['blue' for x in range(self.ttfObject.numberOfAgents)]
        for i in range(len(self.ttfObject.tokenList)):
            if self.ttfObject.tokenList[i] == 0:
                self.node_colors[i] = 'gray'
        self.node_colors[0]='red'

    def set_sender_reciver_colors(self, interactionIndex):
        self.node_colors[self.interactions[interactionIndex][0][1]] = 'yellow'
        self.node_colors[self.interactions[interactionIndex][0][0]] = 'green'

    def set_node_labels(self):
        #set the node lables
        k=0
        self.node_labels = {}
        for el  in self.ttfObject.tokenList:
            self.node_labels[k] = el
            k +=1
    
    def set_interaction_edge_color(self, interactionIndex):
        self.edeg_colors[0:] = ['black'] * len(self.edeg_colors)
        sender, reciver, communication = self.interactions[interactionIndex][0][1],self.interactions[interactionIndex][0][0], self.interactions[interactionIndex][1]
        index = -1
        if (sender, reciver) in self.edges:
            index = self.edges.index((sender,reciver))
        else:
            index = self.edges.index((reciver,sender))
        if communication:
            self.edeg_colors[index]= 'blue'
        else:
            self.edeg_colors[index] = 'red'        
