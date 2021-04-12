import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import transfer_to_transfer as ttf
import time

class TTFVisualizer:

    def __init__(self, ttfObject):
        self.fromNodes = []
        self.toNodes = []
        self.ttfObject = ttfObject

    def run_ttf(self):
        numberOfInteractions = 0
        G = nx.MultiDiGraph()
        colorMap=[]
        for i in range(0, self.ttfObject.numberOfAgents):
            if i==0:
                G.add_node(i)
                colorMap.append('red')
            else:
                G.add_node(i)
                colorMap.append('blue')
        interactions=[]
        while self.ttfObject.is_termination_configuration() != True:
            currentInteraction = self.ttfObject.next_interaction()
            print('Current interaction: ', currentInteraction)
            numberOfInteractions += 1
            print('Number of interactions: ', numberOfInteractions)
            print('TokenList: ', self.ttfObject.tokenList)
            edge_colors = []
            for i in interactions:
                edge_colors.append('black')
            interactions.append(currentInteraction[0])
            edge_colors.append('red')
            print("Interactions: ",interactions)
            G.add_edges_from(interactions)
            print('nodes',G.nodes)
            
            


            plt.figure(figsize=(8,8))
            
            nx.draw(G,with_labels=True, node_color = colorMap, edge_color = edge_colors)

            if self.ttfObject.is_termination_configuration() != True:
                plt.show(block=False)
                plt.pause(3)
                plt.close()
            else:
                plt.show()
