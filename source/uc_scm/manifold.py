import json
import numpy as np
import sympy
from sympy.stats import *
from input import *
from sympy.utilities.lambdify import *

class manifold(object):
    def __init__(self, **kwargs):
        self.manifold= {'X': None, 'Topology': [], 'Adjacency': None, 'amount_states': None,
                        'Actions': {}, 'Position': None}
        self.param={'option_topology': 'const_neigh', 'neighbour_distance': 1.2}

    def check_new_cand(self, new_candidate):
        if (new_candidate in self.manifold['Topology']):
            None
        else:
            self.manifold['Topology'].append(new_candidate)

    def get_scm_function(self, input):
        inp=sympy.symbols('r')
        scm = input["scm"]
        scms=list(scm.values())
        dictionary = input["variables"]
        abc = list(input.values())
        symb=list(dictionary.values())
        symb=sympy.symbols(symb)
        scm_1 = sympy.sympify(scms[0])
        scm_2 = sympy.sympify(scms[1])
        f=[implemented_function('scm_1', lambda inp: scm_1.subs([((symb[0]), inp[0]), ((symb[1]), inp[1])])),
           implemented_function('scm_2', lambda inp: scm_2.subs([((symb[0]), inp[0]), ((symb[1]), inp[1])]))]
        lam_f=lambdify(inp, [f[0](inp), f[1](inp)])
        print(lam_f([symb[0], 3]))
        erg=lam_f([8, 3])
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

    def get_topology_by_scm(self, data):
        scm=data["scm"]
        dictionary=data["variables"]
        abc_keys = list(scm.keys())
        abc = list(scm.values())
        topology=[]
        for idx, qrt in enumerate(abc):
            for idx2, qrt2 in enumerate(abc):
                if dictionary[abc_keys[idx]] in qrt2:
                    topology.append([abc_keys[idx], abc_keys[idx2]])
        return topology
    def split_by_delim(self, dat):
        first = dat.split('+')
        second = [s.split('-') for s in first]
    def scm_import_json(self):
        f = open('../../input/structuralCausalModels.json', "r")
        data = json.loads(f.read())
        self.manifold['amount_states'] = len(data['scm'])
        self.manifold['X'] = [qrt for qrt in data['scm']]
        self.manifold['Topology']=self.get_topology_by_scm(data)
        self.get_scm_function(data)
        self.get_adjacency(self.manifold['amount_states'])
        self.set_neighbour_actions()
    def old2(self, dictDat, edges):
        abc_keys = list(dictDat.keys())
        abc = list(dictDat.values())
        self.manifold['Position'] = [tuple(abc[i]) for i in range(0, len(abc))]
        x = np.array([pt[0] for pt in abc])
        y = np.array([pt[1] for pt in abc])
        self.manifold['Topology'] = [tuple(edges[i]) for i in range(0, len(edges))]
    def get_adjacency(self, am_nodes):
        self.manifold['Adjacency']=np.eye(am_nodes, dtype=bool)
        for wlt in self.manifold['Topology']:
            self.manifold['Adjacency'][int(wlt[1])][int(wlt[0])] = True
        test_symmetry=np.allclose(self.manifold['Adjacency'], self.manifold['Adjacency'].T, rtol=1e-05, atol=1e-08)
        print('symmetry')
        print(test_symmetry)
    def set_neighbour_actions(self):
        for wlt in range(0, np.size(self.manifold['Adjacency'], 1)):
            abc=self.manifold['Adjacency'][:, wlt]
            all_actions=[self.manifold['X'][idx] for idx, qrt in enumerate(abc) if abc[idx] == True]
            self.manifold['Actions'].update({self.manifold['X'][wlt]: all_actions})

if __name__ == '__main__':
    obj=manifold()
    obj.set_environment()
    print(obj.manifold)