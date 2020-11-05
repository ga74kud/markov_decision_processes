import json
import numpy as np
from input import *
class manifold(object):
    def __init__(self, **kwargs):
        self.manifold= {'X': None, 'Topology': [], 'Atlas': None, 'Policy': None, 'Adjacency': None, 'amount_states': None,
                        'Actions': {}, 'Position': None}
        self.param={'option_topology': 'const_neigh', 'neighbour_distance': 12}

    def check_new_cand(self, new_candidate):
        if (new_candidate in self.manifold['Topology']):
            None
        else:
            self.manifold['Topology'].append(new_candidate)
    def set_environment_by_json(self, FILE_DIR):
        f = open(FILE_DIR, "r")
        data = json.loads(f.read())
        self.manifold['amount_states']=len(data['points'])
        self.manifold['X']=[qrt for qrt in data['points']]
        if('topology' in data):
            self.manifold['Topology']=[tuple(data['topology'][qrt]) for qrt in data['topology']]
        elif(self.param['option_topology']=='norm2 distance'):
            self.get_topology_by_norm2_distance(data['points'])
        elif (self.param['option_topology'] == 'const_neigh'):
            self.get_topology_by_neighbors(data['points'])
        self.get_adjacency(self.manifold['amount_states'])
        self.set_neighbour_actions()
    def get_topology_by_neighbors(self, dictDat):
        abc_keys=list(dictDat.keys())
        abc=list(dictDat.values())
        self.manifold['Position']=[tuple(abc[i]) for i in range(0, len(abc))]
        x = np.array([pt[0] for pt in abc])
        y = np.array([pt[1] for pt in abc])
        d=np.sqrt(np.square(x - x.reshape(-1, 1)) + np.square(y - y.reshape(-1, 1)))
        for idx in range(0, np.size(d,1)):
            dbd=np.argsort(d[:, idx])
            my_idx=abc_keys[idx]
            self.manifold['Topology'].append((my_idx, my_idx))
            for st_idx in range(1, 4):
                st=dbd[st_idx]
                self.manifold['Topology'].append((my_idx, abc_keys[st]))
                self.manifold['Topology'].append((abc_keys[st], my_idx))
    def get_topology_by_norm2_distance(self, dictDat):
        abc=list(dictDat.keys())

        for k, qrt in enumerate(dictDat):
            for k2 in range(k+1, len(dictDat)):
                a=abc[k]
                b=abc[k2]
                val1=np.array(dictDat[a])
                val2=np.array(dictDat[b])
                diff=val1-val2
                dist = np.linalg.norm(diff)
                if(dist<=self.param['neighbour_distance']):
                    self.manifold['Topology'].append((a, b))
                    self.manifold['Topology'].append((b, a))

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