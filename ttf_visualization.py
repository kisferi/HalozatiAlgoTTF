import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import transfer_to_transfer as ttf
import time
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox

class TTFVisualizer:
    index = 0
    node_colors = []
    node_labels = {}
    node_positions = []
    interactions = []
    G = nx.MultiGraph()
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

    def run_ttf(self):
        #turn on pyplot interactive mode

        fig, axes = plt.subplots(nrows=2, ncols=1, gridspec_kw={'height_ratios': [20, 1]})
        self.ax = axes.flatten()
        self.ax[1].set_axis_off()
        plt.tight_layout()
        #set the node colors
        self.set_node_colors()
        self.set_node_labels()
        nx.draw(self.G, ax = self.ax[0] ,with_labels=True, node_color = self.node_colors, pos = self.node_positions, labels = self.node_labels, linewidths=4, font_size=12,node_size=500,  width=2)

        for i in range(self.ttfObject.numberOfAgents):
            for j in range(self.ttfObject.numberOfAgents):
                source, target = i,j
                arrowprops=dict(arrowstyle="<|-", color="black",
                                shrinkA=15, shrinkB=15,
                                patchA=None, patchB=None,
                                connectionstyle="arc3,rad=0.1",
                                )
                self.ax[0].annotate("",
                            xy=self.node_positions[source],
                            xytext=self.node_positions[target],
                            arrowprops=arrowprops
                        )

        #run button
        axcut = plt.axes([0.01, 0.002, 0.1, 0.075])
        self.run_btn = Button(axcut, 'Run')
        self.run_btn.on_clicked(self.run)

        #next button
        axcut = plt.axes([0.12, 0.002, 0.1, 0.075])
        self.next_btn = Button(axcut, 'Next')
        self.next_btn.on_clicked(self.next)

        # #next data transfer button
        # axcut = plt.axes([0.23, 0.002, 0.2, 0.075])
        # self.next_trans_btn = Button(axcut, 'Next Transfer')
        # self.next_trans_btn.on_clicked(self.run)

        #add text with time and energy consumed
        axcut = plt.axes([0.63, 0.002, 0.1, 0.075])
        self.text_box1 = TextBox(axcut, "Time: ")
        self.text_box1.set_val(str(self.index))
        axcut = plt.axes([0.83, 0.002, 0.1, 0.075])
        self.text_box2 = TextBox(axcut, "Energy: ")
        self.text_box2.set_val(str(self.ttfObject.numberOfDataTransitions))
        plt.show()

    def run(self, event):
        while self.ttfObject.is_termination_configuration() != True:
            self.ax[0].clear()
            self.interactions.append(self.ttfObject.next_interaction())
            print('Current interaction: ', self.interactions[self.index])
            print('Number of interactions: ', self.index+1)

            #set the node colors
            self.set_node_colors()
            self.set_node_labels()
            self.set_sender_reciver_colors(self.index)
            self.set_interaction_edge_color(self.index)

            nx.draw(self.G, ax = self.ax[0] ,with_labels=True, node_color = self.node_colors, pos = self.node_positions, labels = self.node_labels, linewidths=4, font_size=12,node_size=500,  width=2)

            if not self.ttfObject.is_termination_configuration():
                plt.pause(0.2)
                self.text_box2.set_val(str(self.ttfObject.numberOfDataTransitions))
            # #increase the interactions number
                self.index += 1

                self.text_box1.set_val(str(self.index))
                plt.show()
            else:
                print("Done")
                self.index += 1
                self.text_box1.set_val(str(self.index))
                self.text_box2.set_val(str(self.ttfObject.numberOfDataTransitions))
                plt.show()
                #f=open("test_ttf.txt", "a+")
                #f.write("Time = " + str(self.index) + "      Energy = " + str(self.ttfObject.numberOfDataTransitions) + '\n')
                #f.close()
                plt.show(block=True)


    def next(self, event):
        if not self.ttfObject.is_termination_configuration():
            self.ax[0].clear()
            self.interactions.append(self.ttfObject.next_interaction())
            print('Current interaction: ', self.interactions[self.index])
            print('Number of interactions: ', self.index+1)
            print('Number of transitions: ', self.ttfObject.numberOfDataTransitions)

            #set the node colors
            self.set_node_colors()
            self.set_node_labels()
            self.set_sender_reciver_colors(self.index)
            self.set_interaction_edge_color(self.index)

            nx.draw(self.G, ax = self.ax[0] ,with_labels=True, node_color = self.node_colors, pos = self.node_positions, labels = self.node_labels, linewidths=4, font_size=12,node_size=500,  width=2)

            self.text_box2.set_val(str(self.ttfObject.numberOfDataTransitions))
            self.index += 1
            self.text_box1.set_val(str(self.index))
            plt.show()
    
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
        if self.ttfObject.is_termination_configuration():
            self.node_colors[0] = 'green'


    def set_node_labels(self):
        #set the node lables
        k=0
        self.node_labels = {}
        for el  in self.ttfObject.tokenList:
            self.node_labels[k] = chr(ord('a')+k) + '(' + str(el)+')'
            k +=1

    def set_interaction_edge_color(self, interactionIndex):
        for i in range(self.ttfObject.numberOfAgents):
                for j in range(self.ttfObject.numberOfAgents):
                    source, target = i,j
                    color = 'black'
                    if source == self.interactions[self.index][0][1] and target == self.interactions[self.index][0][0]:
                        if self.interactions[self.index][1]:
                            color= 'green'
                        else:
                            color = 'red'
                    arrowprops=dict(arrowstyle="<|-", color=color,
                                    shrinkA=15, shrinkB=15,
                                    patchA=None, patchB=None,
                                    connectionstyle="arc3,rad=0.1",
                                    )
                    self.ax[0].annotate('',
                                xy=self.node_positions[source],
                                xytext=self.node_positions[target],
                                arrowprops=arrowprops
                            )
