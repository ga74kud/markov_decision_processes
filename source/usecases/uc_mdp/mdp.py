import igraph as ig
import numpy as np
from scipy.cluster.vq import kmeans, vq
import source.util.data_input_loader as util_io

class mdp(object):
    def __init__(self, **kwargs):
        self.mdp_dict= {'S': None, # States
                   'action': None, # Action set
                   'adjacency_list': None, # Topology
                   'R': None, # Rewards
                   'gamma': None, # discount factor
                   'P': None # Positions
                    }
        self.mdp_dict['T']=None # Transition
        self.mdp_dict['pi']=None
        self.mdp_dict['multi_pi'] = {}
        self.mdp_dict['U'] = None
        self.param = {'n_optimal_trajectory': None, # optimal trajectory
                      }
        params=util_io.get_params()
        self.set_gamma(params["mdp"]["simulation"]["gamma"])
        self.set_limit_simulation(params["mdp"]["simulation"]["limit_counts"])

    def set_limit_simulation(self, value):
        self.param["n_optimal_trajectory"]=value

    def set_gamma(self, gamma):
        self.mdp_dict["gamma"]=gamma

    def set_position_list(self, position):
        self.mdp_dict['P']=position

    def set_T(self, transition):
        self.mdp_dict['T']=transition

    def set_U(self):
        self.mdp_dict['U'] = [0] * len(self.mdp_dict['S'])

    def set_action(self, action):
        self.mdp_dict['action']=action

    def set_init_pi(self):
        a={}
        for i in self.mdp_dict['S']:
            a[i]=self.mdp_dict['action'][i][0]
        self.mdp_dict['pi']=a

    def set_S(self, S):
        self.mdp_dict['S']=S

    def set_R(self, dictR):
        val=list(dictR.values())
        keys=dictR.keys()
        self.mdp_dict['R']=np.zeros(len(self.mdp_dict['S']))
        for idx, q in enumerate(keys):
            self.mdp_dict['R'][int(q)]=val[idx]

    def set_T(self, T):
        self.mdp_dict['T']=T
    def set_adjacency_list(self, list):
        new_list=[]
        for i in list:
            a = self.mdp_dict['S'].index(i[0])
            b = self.mdp_dict['S'].index(i[1])
            new_list.append((a, b))
            new_list.append((a, a))
            #new_list.append((b, a))
        self.mdp_dict['adjacency_list']=new_list

    def policy_evaluation(self):
            for kp, p in enumerate(self.mdp_dict['S']):
                state_action=(p, self.mdp_dict['pi'][p])
                prob_dict=self.mdp_dict['T'][state_action]
                bds=self.mdp_dict['gamma']*np.sum([a * b for a, b in zip(self.mdp_dict['U'], prob_dict)])
                idx=np.int(np.random.choice(len(self.mdp_dict['S']), 1, p=prob_dict))
                self.mdp_dict['U'][kp]=self.mdp_dict['R'][idx]+bds
            return self.mdp_dict['U']

    def policy_iteration(self):
            actual_U=self.policy_evaluation()
            for kp, p in enumerate(self.mdp_dict['S']):
                all_Us = np.zeros(len(self.mdp_dict['action'][p]))
                for ka, act_a in enumerate(self.mdp_dict['action'][p]):
                    state_action=(p, act_a)
                    prob_dict=self.mdp_dict['T'][state_action]
                    bds=self.mdp_dict['gamma']*np.sum([a * b for a, b in zip(actual_U, prob_dict)])
                    idx = np.int(np.random.choice(len(self.mdp_dict['S']), 1, p=prob_dict))
                    all_Us[ka]=self.mdp_dict['R'][idx] + bds
                self.get_new_policy(np.array(all_Us), kp)

    def get_new_policy(self, all_Us, act_node):
        idx=np.argmax(all_Us, axis=0)
        act_node_name=self.mdp_dict['S'][act_node]
        self.mdp_dict['pi'][act_node_name]=self.mdp_dict['action'][act_node_name][idx]

    def find_neighbours(self, act_node):
        return self.mdp_dict["action"][act_node]

    def get_value_of_nodes(self, nodes):
        group=[self.mdp_dict["U"][int(wlt)] for wlt in nodes]
        return group


    def get_all_policy_options(self):
        for act_node in self.mdp_dict['S']:
            act_value=float(self.get_value_of_nodes(act_node)[0]) # actual value function
            act_neighbours=self.find_neighbours(act_node) # actual neighbours
            act_values_by_group=self.get_value_of_nodes(act_neighbours) # actual value function of neighbours
            bool_group=list()
            for wlt in act_values_by_group:
                if(wlt>act_value):
                    bool_group.append(True)
                else:
                    bool_group.append(False)
            self.mdp_dict['multi_pi'][act_node]=list()
            for idx, act_bool in enumerate(bool_group):
                if(act_bool==True):
                    new_cand={"neighbour": act_neighbours[idx], "difference": float(act_values_by_group[idx]-act_value)}
                    self.mdp_dict['multi_pi'][act_node].append(new_cand)

    def start_mdp(self):
        count=0
        count2=0
        while(1):
            oldU=self.mdp_dict['U'][:]
            self.policy_iteration()
            if (np.sum(np.array(self.mdp_dict['U']))==0):
                count += 1
                continue
            if(np.sum(np.array(self.mdp_dict['U'])-np.array(oldU))<10e-9):
                count += 1
                count2+=1
            if(count2>10):
                print("Convergence")
                print(count)
                print(self.mdp_dict['pi'])
                print(self.mdp_dict['U'])
                break
            elif(count>1000):
                print("No Convergence")
                break

            count+=1
        return self.mdp_dict

    def visualize_network(self):
        g = ig.Graph(self.mdp_dict['adjacency_list'])
        g.vs["name"] = self.mdp_dict['S']
        g.vs["reward"]= self.mdp_dict['R']
        g.vs["label"] = g.vs["name"]
        vec=np.array(self.mdp_dict['U'])
        p=np.var(vec)
        if(p==0):
            print('error')
            exit()
        color_dict = {0: "blue", 1: "green", 2: "cyan", 3: "yellow", 4: "pink", 5: "orange", 6: "red"}
        codebook, _ = kmeans(vec, len(color_dict))
        cluster_indices, _ = vq(vec, codebook)
        sel=[]
        am_max_cluster=np.max(cluster_indices)
        for qrti in range(0, am_max_cluster+1):
            tre=qrti==cluster_indices
            new_candi=np.max(vec[tre])
            sel.append(new_candi)
        sel=np.array(sel)
        sort_idx=np.argsort(sel)
        new_cluster_indices=[np.nan]*len(cluster_indices)
        for count, qrt in enumerate(sort_idx):
            act_idx_bool=sort_idx[count]==cluster_indices
            act_idx=np.where(act_idx_bool)
            act_idx=act_idx[0].tolist()
            for t in act_idx:
                new_cluster_indices[t]=count
        col_r = np.round(np.linspace(255, 0, len(vec)))
        col_g = np.round(np.linspace(0, 255, len(vec)))
        col_b = np.zeros(len(vec))
        transp=np.ones(len(vec))
        allCol=np.transpose(np.vstack((col_r, col_g, col_b, transp)))
        colors = [color_dict[index] for index in new_cluster_indices]
        g.vs["color"] = colors
        P_2D=[(wlt[0], wlt[1]) for wlt in self.mdp_dict['P']]
        layout = ig.Layout(P_2D)
        g.vs["vertex_size"] = 20
        visual_style = {}
        visual_style["edge_curved"] = False
        ig.plot(g, layout=layout, **visual_style)

    def get_trajectory(self, R_dict):
        params=util_io.get_params()
        start_node=self.mdp_dict['S'][params["mdp"]["simulation"]["start_node"]]
        r_target_values=list(R_dict.keys())
        ideal_path=[]
        ideal_path.append(str(start_node))
        policy=self.mdp_dict['pi']
        count=0
        while(1):
            act_node=ideal_path[-1]
            action=policy[act_node]
            if(count>self.param['n_optimal_trajectory']):
                break
            if(act_node in r_target_values):
                break
            else:
                count+=1
            abc=self.mdp_dict['T']
            act_trans=abc[(act_node, action)]
            next_node=np.int(np.random.choice(len(self.mdp_dict['S']), 1, p=act_trans))
            ideal_path.append(self.mdp_dict['S'][next_node])
        print('ideal_path')
        print(ideal_path)
        self.visualize_network()
        return ideal_path



