import json
import numpy as np
from input import *
class manifold(object):
    def __init__(self, **kwargs):
        self.manifold= {'X': None, 'Topology': [], 'Atlas': None, 'Policy': None, 'Adjacency': None, 'amount_states': None,
                        'Actions': {}}

    def check_new_cand(self, new_candidate):
        if (new_candidate in self.manifold['Topology']):
            None
        else:
            self.manifold['Topology'].append(new_candidate)
    def set_environment_by_json(self):
        f = open('../input/puntigam.json', "r")
        data = json.loads(f.read())
        self.manifold['amount_states']=len(data['points'])
        self.manifold['X']=[qrt for qrt in data['points']]
        self.manifold['Topology']=[tuple(data['topology'][qrt]) for qrt in data['topology']]
        self.get_adjacency(self.manifold['amount_states'])
        self.set_neighbour_actions()
    def set_neighbour_actions(self):
        for wlt in range(0, np.size(self.manifold['Adjacency'], 1)):
            abc=self.manifold['Adjacency'][:, wlt]
            all_actions=[self.manifold['X'][idx] for idx, qrt in enumerate(abc) if abc[idx] == True]
            self.manifold['Actions'].update({self.manifold['X'][wlt]: all_actions})
    def get_probability_nodes(self):
        maxProb=.7
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
                prob[vec]=.3
                act_type=(topSet[qrt][0], topSet[qrt][1])
                prob[int(topSet[qrt][1])]=maxProb
                prob=prob/prob.sum()
                if(np.allclose(sum(prob), 1.0, rtol=1e-05, atol=1e-08)):
                    #print('valid')
                    newdict={act_type: prob}
                    transition.update(newdict)
                else:
                    None
                    #print('error')
        return transition

    def get_adjacency(self, am_nodes):
        self.manifold['Adjacency']=np.zeros((am_nodes, am_nodes), dtype=bool)
        for wlt in self.manifold['Topology']:
            self.manifold['Adjacency'][int(wlt[0])][int(wlt[1])]=True
            #self.manifold['Adjacency'][int(wlt[1])][int(wlt[0])] = True
        test_symmetry=np.allclose(self.manifold['Adjacency'], self.manifold['Adjacency'].T, rtol=1e-05, atol=1e-08)
        print('symmetry')
        print(test_symmetry)

    def get_topology_west(self, num, xoffset):
        if ((num+1) % xoffset == 0):
            return (str(num), str(num), 'w')
        else:
            return (str(num), str(num+1), 'w')

    def get_topology_east(self, num, xoffset):
        if (num % xoffset == 0):
            return (str(num), str(num), 'e')
        else:
            return (str(num), str(num - 1), 'e')
    def get_topology_south(self, num, xoffset, amount_states):
        if (num > amount_states-xoffset-1):
            return (str(num), str(num), 's')
        else:
            return (str(num), str(num + xoffset), 's')
    def get_topology_north(self, num, xoffset):
        if (num < xoffset):
            return (str(num), str(num), 'n')
        else:
            return (str(num), str(num - xoffset), 'n')

        a=1




if __name__ == '__main__':
    obj=manifold()
    obj.set_environment()
    print(obj.manifold)