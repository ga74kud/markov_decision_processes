import igraph as ig
import sympy
from sympy.stats import *
from sympy.utilities.lambdify import *
from source.uc_pomdp.pomdp import *
import json


class scm_class(object):
    def __init__(self, **kwargs):
        self.manifold=None
        self.data=None
    def set_manifold(self, manifold):
        self.manifold=manifold.manifold

    def set_adjacency_list(self, nodes, list):
        new_list = []
        for i in list:
            a = nodes.index(i[0])
            b = nodes.index(i[1])
            new_list.append((a, b))
        return new_list
    def scm_import_json(self):
        f = open('../../input/structuralCausalModels.json', "r")
        self.data = json.loads(f.read())
        self.manifold['amount_states'] = len(self.data['scm'])
        self.manifold['X'] = [qrt for qrt in self.data['scm']]
        self.manifold['Topology']=self.get_topology_by_scm(self.data)
        t=self.get_scm_function(self.data, [Normal('M', 2, 1), Normal('N', 3, 1), Normal('O', 4, 1)])
        print(t)
        self.get_adjacency(self.manifold['amount_states'])
        self.set_neighbour_actions()
    def get_topology_by_scm(self, data):
        scm=data["scm"]
        dictionary=data["variables"]
        abc_keys = list(scm.keys())
        abc = list(scm.values())
        topology=[]
        for idx, qrt in enumerate(abc):
            for idx2, qrt2 in enumerate(abc):
                if (idx == 3 and idx2==1):
                    b = 1
                check_val=dictionary[abc_keys[idx]]
                check_str=qrt2.find(check_val)
                if (check_str != -1):
                    topology.append([abc_keys[idx], abc_keys[idx2]])
        return topology

    def odl(self):
        f = open('../../input/structuralCausalModels.json', "r")
        data = json.loads(f.read())
        self.manifold['amount_states'] = len(data['scm'])
        self.manifold['X'] = [qrt for qrt in data['scm']]
        self.manifold['Topology']=self.get_topology_by_scm(data)
        t=self.get_scm_function(data, [Normal('M', 2, 1), Normal('N', 3, 1), Normal('O', 4, 1)])
        print(t)
        self.get_adjacency(self.manifold['amount_states'])
        self.set_neighbour_actions()

    def get_scm_function(self, input, values):
        all_exp=[]
        all_var = []
        scms=list(input["scm"].values())
        dictionary = input["variables"]
        symb=sympy.symbols(list(dictionary.values()))
        scm_sympy = sympy.sympify(scms)
        for q, qi in enumerate(scm_sympy):
            expectation_scm, variance_scm=self.get_expected_val_scm(input, q, qi, symb, values)
            all_exp.append(expectation_scm)
            all_var.append(variance_scm)
        return all_exp
    def get_expected_val_scm(self, input, q, qi, symb, values):
        a = sympy.symbols('a')
        new_fun=implemented_function('scm_'+str(q), lambda inp: qi.subs([(symb[i], inp[i]) for i in range(0, len(inp))]))
        lam_f=lambdify(a, new_fun(a))
        erg=lam_f(values)
        return E(erg), variance(erg)
    def set_neighbour_actions(self):
        for wlt in range(0, np.size(self.manifold['Adjacency'], 1)):
            abc=self.manifold['Adjacency'][:, wlt]
            all_actions=[self.manifold['X'][idx] for idx, qrt in enumerate(abc) if abc[idx] == True]
            self.manifold['Actions'].update({self.manifold['X'][wlt]: all_actions})
    def get_adjacency(self, am_nodes):
        self.manifold['Adjacency']=np.eye(am_nodes, dtype=bool)
        for wlt in self.manifold['Topology']:
            self.manifold['Adjacency'][int(wlt[1])][int(wlt[0])] = True
        test_symmetry=np.allclose(self.manifold['Adjacency'], self.manifold['Adjacency'].T, rtol=1e-05, atol=1e-08)
        print('symmetry')
        print(test_symmetry)

    def visualize_network(self):
        nodes=self.manifold['X']
        nodes_name=[self.data['variables'][i] for i in nodes]
        adjacency=self.set_adjacency_list(nodes, self.manifold['Topology'])
        g = ig.Graph(adjacency, directed=True)
        g.vs["name"] = nodes_name
        g.vs["label"] = g.vs["name"]
        g.vs["vertex_size"] = 20
        visual_style = {}
        visual_style["edge_curved"] = False
        ig.plot(g, **visual_style)#margin = 20,bbox = (3000, 3000), layout=layout,


