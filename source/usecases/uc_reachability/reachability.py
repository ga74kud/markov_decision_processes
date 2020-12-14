# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Reachability Analysis (RA)
#
# (C) 2020 Michael Hartmann, Graz, Austria
# Released under TODO: find a release license
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------

import igraph as ig
import numpy as np
from scipy.cluster.vq import kmeans, vq
import source.util.data_input_loader as util_io


"""
Class for reachability analysis
"""
class reachability(object):
    def __init__(self, **kwargs):
        self.reach_dict = {'S': None,  # States
                         'action': None,  # Action set
                         'adjacency_list': None,  # Topology
                         'P': None  # Positions
                         }
        self.reach_dict['multi_pi'] = {}

    """
    Set states 
    """
    def set_S(self, S):
        self.reach_dict['S']=S

    """
    Set adjacency list
    """
    def set_adjacency_list(self, list):
        new_list=[]
        for i in list:
            a = self.reach_dict['S'].index(i[0])
            b = self.reach_dict['S'].index(i[1])
            new_list.append((a, b))
            new_list.append((a, a))
            #new_list.append((b, a))
        self.reach_dict['adjacency_list']=new_list

    """
    Set position list
    """
    def set_position_list(self, position):
        self.reach_dict['P']=position

    """
    Set transition list
    """
    def set_T(self, transition):
        self.reach_dict['T']=transition

    """
    Set action list
    """
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

    def get_reach_in_list(self, reach_list):
        for qrt in range(0,len(reach_list)-1):
            act_elem=list(reach_list[qrt])
            act_elem=util_io.union_of_lists(act_elem, reach_list[qrt+1])
        return act_elem
    def one_reach_cycle(self, inp):
        all_ref = []
        for qrt in inp:
            act_neigh = self.reach_dict['multi_pi'][qrt][0]["neighbour"]
            all_ref = util_io.union_of_lists(act_neigh, all_ref)
        return all_ref
    def get_reach_list(self, start_point, depth):
        reach_list=[]
        reach_list.append(start_point)
        for qrt in range(0, depth):
            all_ref=self.one_reach_cycle(reach_list[-1])
            reach_list.append(all_ref)
        reach_list=self.get_reach_in_list(reach_list)
        return reach_list

    def start_getting_reach_list(self, depth):
        params = util_io.get_params()
        act_node = self.reach_dict['S'][params["general"]["start_node"]]
        reach_list = self.get_reach_list(act_node, depth)
        return reach_list
    """
    Visualize reachability analysis
    """
    def visualize_network(self, folder_to_store, all_reach_list):
        for wlt in range(0, len(all_reach_list)):
            reach_list=all_reach_list[wlt]#self.start_getting_reach_list(wlt)
            g = ig.Graph(self.reach_dict['adjacency_list'])
            g.vs["name"] = self.reach_dict['S']
            g.vs["label"] = g.vs["name"]
            color_dict = {0: "green", 1: "blue", 2: "red"}
            P_2D = [(wlt[0], wlt[1]) for wlt in self.reach_dict['P']]
            layout = ig.Layout(P_2D)
            g.vs["vertex_size"] = 20
            colors=[]
            for index in self.reach_dict['S']:
                if(index in reach_list):
                    colors.append(color_dict[0])
                else:
                    colors.append(color_dict[2])

            g.vs["color"] = colors
            visual_style = {}
            visual_style["edge_curved"] = False
            ig.plot(g, folder_to_store + "reach_igraph_"+str(wlt+1)+".pdf", layout=layout, **visual_style)
