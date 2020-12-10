import igraph as ig
import numpy as np
from scipy.cluster.vq import kmeans, vq
import source.util.data_input_loader as util_io

class reachability(object):
    def __init__(self, **kwargs):
        self.reach_dict = {'S': None,  # States
                         'action': None,  # Action set
                         'adjacency_list': None,  # Topology
                         'P': None  # Positions
                         }
        self.reach_dict['multi_pi'] = {}
    def set_S(self, S):
        self.reach_dict['S']=S
    def set_adjacency_list(self, list):
        new_list=[]
        for i in list:
            a = self.reach_dict['S'].index(i[0])
            b = self.reach_dict['S'].index(i[1])
            new_list.append((a, b))
            new_list.append((a, a))
            #new_list.append((b, a))
        self.reach_dict['adjacency_list']=new_list
    def set_position_list(self, position):
        self.reach_dict['P']=position

    def set_T(self, transition):
        self.reach_dict['T']=transition
    def set_action(self, action):
        self.reach_dict['action']=action

    """
    Find neighbours
    """
    def find_neighbours(self, act_node):
        return self.reach_dict["action"][act_node]

    """
    Get all policy options
    """
    def get_all_policy_options(self):
        for act_node in self.reach_dict['S']:
            act_neighbours = self.find_neighbours(act_node)  # actual neighbours
            self.reach_dict['multi_pi'][act_node] = list()
            new_cand = {"neighbour": act_neighbours}
            self.reach_dict['multi_pi'][act_node].append(new_cand)

    """
    Get all neighbours for each node to perform later reachability analysis
    """
    def start_reach_algorithm(self):
        self.get_all_policy_options()

    """
    Visualize reachability analysis
    """
    def visualize_network(self, folder_to_store):
        params = util_io.get_params()
        act_node = self.reach_dict['S'][params["general"]["start_node"]]
        g = ig.Graph(self.reach_dict['adjacency_list'])
        g.vs["name"] = self.reach_dict['S']
        g.vs["label"] = g.vs["name"]
        color_dict = {0: "blue", 1: "green", 2: "cyan", 3: "yellow", 4: "pink", 5: "orange", 6: "red"}
        P_2D = [(wlt[0], wlt[1]) for wlt in self.reach_dict['P']]
        layout = ig.Layout(P_2D)
        g.vs["vertex_size"] = 20
        visual_style = {}
        visual_style["edge_curved"] = False
        ig.plot(g, folder_to_store + "reach_igraph.pdf", layout=layout, **visual_style)
