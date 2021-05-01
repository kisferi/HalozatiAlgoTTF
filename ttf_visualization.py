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
    outter_node_lables = {}
    outter_node_lable_pos = {}
    node_positions = []
    edeg_colors = []
    edges = []
    interactions = []
    G = nx.Graph()
    ax = []
    run_btn = {}
    next_trans_btn = {}
    next_btn = {}

    def __init__(self, ttfObject):
        self.index = 0
        self.ttfObject = ttfObject
        #set the graph
        self.G.add_nodes_from(range(0,self.ttfObject.numberOfAgents))
        self.node_positions = nx.spring_layout(self.G)
        #add all edges to the graph
        for i in range(self.ttfObject.numberOfAgents):
            for j in range(self.ttfObject.numberOfAgents):
                if(i<j):
                    self.G.add_edge(i,j)
                    self.edges.append((i,j))
                    self.edeg_colors.append('black')
        self.set_node_outter_lables()

    def run_ttf(self):
        #turn on pyplot interactive mode

        fig, axes = plt.subplots(nrows=2, ncols=1, gridspec_kw={'height_ratios': [9, 1]})
        self.ax = axes.flatten()
        self.ax[1].set_axis_off()
        plt.tight_layout()
        #set the node colors
        self.set_node_colors()
        self.set_node_labels()
        nx.draw(self.G, ax = self.ax[0] ,with_labels=True, node_color = self.node_colors, pos = self.node_positions, labels = self.node_labels, edge_color = self.edeg_colors, linewidths=4, font_size=16,node_size=250,  width=2)
        nx.draw_networkx_labels(self.G,ax= self.ax[0], pos = self.outter_node_lable_pos, labels=self.outter_node_lables)

        #run button
        axcut = plt.axes([0.01, 0.1, 0.1, 0.075])
        self.run_btn = Button(axcut, 'Run')
        self.run_btn.on_clicked(self.run)

        #next button
        axcut = plt.axes([0.12, 0.1, 0.1, 0.075])
        self.next_btn = Button(axcut, 'Next')
        self.next_btn.on_clicked(self.next)

        #next data transfer button
        axcut = plt.axes([0.23, 0.1, 0.2, 0.075])
        self.next_trans_btn = Button(axcut, 'Next Transfer')
        self.next_trans_btn.on_clicked(self.run)

        plt.show()

    def run(self, event):
        while self.ttfObject.is_termination_configuration() != True:
            self.ax[0].clear()
            self.interactions.append(self.ttfObject.next_interaction())
            print('Current interaction: ', self.interactions[self.index])
            print('Number of interactions: ', self.index)
            
            #set the node colors
            self.set_node_colors()
            self.set_node_labels()
            self.set_sender_reciver_colors(self.index)
            self.set_interaction_edge_color(self.index)

            nx.draw(G=self.G,ax = self.ax[0] ,with_labels=True, node_color = self.node_colors, pos = self.node_positions, labels = self.node_labels, edge_color = self.edeg_colors, linewidths=4, font_size=16,node_size=250,  width=2)
            nx.draw_networkx_labels(self.G,ax= self.ax[0], pos = self.outter_node_lable_pos, labels=self.outter_node_lables)

            if not self.ttfObject.is_termination_configuration():
                plt.pause(0.5)
                plt.show()
            else:
                print("Done")
                plt.show(block=True)
            # #increase the interactions number
            self.index += 1
            

    def next(self, event):
        if not self.ttfObject.is_termination_configuration():
            self.ax[0].clear()
            self.interactions.append(self.ttfObject.next_interaction())
            print('Current interaction: ', self.interactions[self.index])
            print('Number of interactions: ', self.index)

            #set the node colors
            self.set_node_colors()
            self.set_node_labels()
            self.set_sender_reciver_colors(self.index)
            self.set_interaction_edge_color(self.index)

            nx.draw(self.G,ax = self.ax[0] ,with_labels=True, node_color = self.node_colors, pos = self.node_positions, labels = self.node_labels, edge_color = self.edeg_colors, linewidths=4, font_size=16,node_size=250,  width=2)
            nx.draw_networkx_labels(self.G,ax= self.ax[0], pos = self.outter_node_lable_pos, labels=self.outter_node_lables)
            plt.show()
            self.index += 1

    def set_node_outter_lables(self):
        self.outter_node_lable_pos = {}
        for node, coords in self.node_positions.items():
            self.outter_node_lable_pos[node] = (coords[0], coords[1] - 0.09)
        node_attrs = self.G.nodes
        self.outter_node_lables = {}
        for node in node_attrs:
            self.outter_node_lables[node] = chr(ord('a')+node)

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
        self.node_colors[self.interactions[interactionIndex][0][0]] = 'orange'

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
            self.edeg_colors[index]= 'green'
        else:
            self.edeg_colors[index] = 'red'
