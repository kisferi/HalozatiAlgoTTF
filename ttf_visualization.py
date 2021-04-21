import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import transfer_to_transfer as ttf
import time
from matplotlib.widgets import Button

class TTFVisualizer:
    index = 0

    def __init__(self, ttfObject):
        self.ttfObject = ttfObject
        self.index = 0


    def run_ttf(self):
        #setThe graph
        G = nx.MultiDiGraph()
        G.add_nodes_from(range(0,self.ttfObject.numberOfAgents))
        #set the node colors and positions
        node_colors=['blue' for x in range(self.ttfObject.numberOfAgents)]
        node_colors[0]='red'
        node_positions = nx.circular_layout(G)
        #turn on pyplot interactive mode
        plt.ion()
        i = 0
        interactions = []
        while self.ttfObject.is_termination_configuration() != True:
            interactions.append(self.ttfObject.next_interaction())
            interaction = (interactions[i][0][0], interactions[i][0][1])

            G.add_edge(interactions[i][0][0], interactions[i][0][1])

            print('Current interaction: ', interactions[i])
            print('Number of interactions: ', i)

            i += 1
            nx.draw(G,with_labels=True, node_color = node_colors, pos = node_positions)
            if not self.ttfObject.is_termination_configuration():
                plt.pause(1)
                plt.show()
                plt.clf()
            else:
                plt.show(block=True)
    
            
        