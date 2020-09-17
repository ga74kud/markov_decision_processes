import json
import numpy as np
import sympy
from sympy.stats import *
from input import *
from sympy.utilities.lambdify import *

class manifold(object):
    def __init__(self, **kwargs):
        self.manifold= {'X': None, 'Topology': [], 'Atlas': None, 'Policy': None, 'Adjacency': None, 'amount_states': None,
                        'Actions': {}, 'Position': None}
        self.param={'option_topology': 'const_neigh', 'neighbour_distance': 1.2}

    def check_new_cand(self, new_candidate):
        if (new_candidate in self.manifold['Topology']):
            None
        else:
            self.manifold['Topology'].append(new_candidate)
    def set_environment_by_json(self):
        f = open('../../input/scm_easy.json', "r")
        data = json.loads(f.read())
        self.manifold['amount_states']=len(data['states'])
        self.manifold['X']=[qrt for qrt in data['states']]
        self.get_topology_by_scm(data['states'])
        self.get_adjacency(self.manifold['amount_states'])
        self.set_neighbour_actions()
    def get_topology_by_scm(self, data):
        x, y, nx, ny, inp=sympy.symbols('x y nx ny inp')
        r=Normal(x, 0, 1)
        y=x
        print(E(r))
        f=implemented_function('scm_1', lambda inp: inp[0]+inp[1])
        lam_f=lambdify(inp, f(inp))
        print(lam_f([2, 3]))
        b=1


    def set_neighbour_actions(self):
        for wlt in range(0, np.size(self.manifold['Adjacency'], 1)):
            abc=self.manifold['Adjacency'][:, wlt]
            all_actions=[self.manifold['X'][idx] for idx, qrt in enumerate(abc) if abc[idx] == True]
            self.manifold['Actions'].update({self.manifold['X'][wlt]: all_actions})
    def get_probability_nodes(self):
        transition = {}
        for wlt in range(0, np.size(self.manifold['Adjacency'],1)):
            allActions=self.manifold['Actions'][self.manifold['X'][wlt]]
            topSet=[(self.manifold['X'][wlt], i) for i in allActions]
            vec=self.manifold['Adjacency'][:, wlt]
            count=0
            for tlw in range(0, len(vec)):
                if(vec[tlw]):
                    count+=1
            for qrt in range(0, np.size(topSet,0)):
                prob = np.zeros(len(vec))
                prob[vec]=1/count
                act_type=(topSet[qrt][0], topSet[qrt][1])
                prob=prob/prob.sum()
                if(np.allclose(sum(prob), 1.0, rtol=1e-05, atol=1e-08)):
                    newdict={act_type: prob}
                    transition.update(newdict)
                else:
                    None
        return transition

    def get_adjacency(self, am_nodes):
        self.manifold['Adjacency']=np.eye(am_nodes, dtype=bool)
        for wlt in self.manifold['Topology']:
            self.manifold['Adjacency'][int(wlt[1])][int(wlt[0])] = True
        test_symmetry=np.allclose(self.manifold['Adjacency'], self.manifold['Adjacency'].T, rtol=1e-05, atol=1e-08)
        print('symmetry')
        print(test_symmetry)

if __name__ == '__main__':
    obj=manifold()
    obj.set_environment()
    print(obj.manifold)