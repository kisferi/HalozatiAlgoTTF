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
            G.add_node(i)
            if i==0:
                colorMap.append('red')
            else:
                colorMap.append('blue')

        pos = nx.circular_layout(G)
        plt.ion()
        interactions=[]
        while self.ttfObject.is_termination_configuration() != True:
            currentInteraction = self.ttfObject.next_interaction()
            print('Current interaction: ', currentInteraction)
            numberOfInteractions += 1
            print('Number of interactions: ', numberOfInteractions)
            print('TokenList: ', self.ttfObject.tokenList)

            print("Interactions: ",interactions)

            G.add_edge(currentInteraction[0][0], currentInteraction[0][1])
            
            nx.draw(G,with_labels=True, node_color = colorMap, pos= pos)
            if not self.ttfObject.is_termination_configuration():
                plt.pause(0.1)
                plt.show()
                plt.clf()
                
           
