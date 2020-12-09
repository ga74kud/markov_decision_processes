import igraph as ig
import numpy as np
from scipy.cluster.vq import kmeans, vq
import source.util.data_input_loader as util_io

class reachability(object):
    def __init__(self, **kwargs):
        self.reach_dict = {'S': None,  # States
                         'action': None,  # Action set
                         'adjacency_list': None,  # Topology
                         'R': None,  # Rewards
                         'gamma': None,  # discount factor
                         'P': None  # Positions
                         }
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

    def start_reach_algorithm(self):
        None #TODO: for implementation
    def visualize_network(self, folder_to_store):
        None #TODO: for implementation