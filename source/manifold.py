import json
import numpy as np
from input import *
class manifold(object):
    def __init__(self, **kwargs):
        self.manifold= {'X': None, 'Topology': [], 'Atlas': None, 'Policy': None, 'Adjacency': None}
        self.set_environment_by_json()
    def set_environment(self):
        self.manifold['X']=['A', 'B', 'C']
        self.manifold['Topology'] = [('A', 'B'), ('A', 'C'), ('B', 'C')]
        #self.manifold['Atlas']= {'A': {'c': [0, 0], 'g':[[1, 0], [0, 1]]}, 'B': {'c': [1, 0], 'g':[[1, 0], [0, 1]]},
        #                                                                        'C': {'c': [0, 1], 'g':[[1, 0], [0, 1]]}}
    def check_new_cand(self, new_candidate):
        if (new_candidate in self.manifold['Topology']):
            None
        else:
            self.manifold['Topology'].append(new_candidate)
    def set_environment_by_json(self):
        f = open('../input/simpleGrid.json', "r")
        data = json.loads(f.read())
        self.manifold['X']=[str(x) for x in range(data['amount_states'])]
        for i in range(data['amount_states']):
            new_candidate=self.get_topology_west(i, data['xdir'])
            self.check_new_cand(new_candidate)
            new_candidate =self.get_topology_east(i, data['xdir'])
            self.check_new_cand(new_candidate)
            new_candidate =self.get_topology_south(i, data['xdir'], data['amount_states'])
            self.check_new_cand(new_candidate)
            new_candidate =self.get_topology_north(i, data['xdir'])
            self.check_new_cand(new_candidate)
        self.get_adjacency(data['amount_states'])
        a=1
            #nx, ny = (data['xdir'], data['ydir'])
        #x = np.linspace(0, 1, nx)
        #y = np.linspace(0, 1, ny)
        #xv, yv = np.meshgrid(x, y)
    def get_adjacency(self, am_nodes):
        self.manifold['Adjacency']=np.zeros((am_nodes, am_nodes), dtype=bool)
        for wlt in self.manifold['Topology']:
            self.manifold['Adjacency'][int(wlt[0])][int(wlt[1])]=True
        test_symmetry=np.allclose(self.manifold['Adjacency'], self.manifold['Adjacency'].T, rtol=1e-05, atol=1e-08)
        a=1

    def get_topology_west(self, num, xoffset):
        if ((num+1) % xoffset == 0):
            return (str(num), str(num))
        else:
            return (str(num), str(num+1))

    def get_topology_east(self, num, xoffset):
        if (num % xoffset == 0):
            return (str(num), str(num))
        else:
            return (str(num), str(num - 1))
    def get_topology_south(self, num, xoffset, amount_states):
        if (num > amount_states-xoffset-1):
            return (str(num), str(num))
        else:
            return (str(num), str(num + xoffset))
    def get_topology_north(self, num, xoffset):
        if (num < xoffset):
            return (str(num), str(num))
        else:
            return (str(num), str(num - xoffset))

        a=1




if __name__ == '__main__':
    obj=manifold()
    obj.set_environment()
    print(obj.manifold)