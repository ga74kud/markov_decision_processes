import igraph as ig
import numpy as np
from scipy.cluster.vq import kmeans, vq
class mdp(object):
    def __init__(self, **kwargs):
        self.mdp_dict= {'S': None, #States
                   'action': None, #Action set
                   'adjacency_list': None, #Topology
                   'R': None, #Rewards
                   'gamma': 0.9}
        self.mdp_dict['T']=None
        self.mdp_dict['pi']=None
        self.mdp_dict['U'] = None
        self.param = {'n_optimal_trajectory': 30, # optimal trajectory
                      'N': 2, #Time Horizont
                      }
    def set_T(self, Transition):
        self.mdp_dict['T']=Transition
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
        for k in range(1, self.param['N']):
            for kp, p in enumerate(self.mdp_dict['S']):
                state_action=(p, self.mdp_dict['pi'][p])
                prob_dict=self.mdp_dict['T'][state_action]
                bds=self.mdp_dict['gamma']*np.sum([a * b for a, b in zip(self.mdp_dict['U'], prob_dict)])
                idx=np.int(np.random.choice(len(self.mdp_dict['S']), 1, p=prob_dict))
                self.mdp_dict['U'][kp]=self.mdp_dict['R'][idx]+bds
            return self.mdp_dict['U']

    def policy_iteration(self):
        for k in range(1, self.param['N']):
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
      


    def start_mdp(self):
        count=0
        while(1):
            oldU=self.mdp_dict['U'][:]
            self.policy_iteration()
            if (np.sum(np.array(self.mdp_dict['U']))==0):
                continue
            if(np.sum(np.array(self.mdp_dict['U'])-np.array(oldU))<10e-9):

                print("Convergence")
                print(count)
                print(self.mdp_dict['pi'])
                print(self.mdp_dict['U'])
                break
            elif(count>1000):
                print("No Convergence")
                break

            count+=1

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
        for qrti in range(0, len(color_dict.keys())):
            tre=qrti==cluster_indices
            sel.append(np.max(vec[tre]))
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
        #g.vs["color"]=[color_dict[r] for r in cluster_indices]
        #palette = ig.ClusterColoringPalette(len(vec))
        colors = [color_dict[index] for index in new_cluster_indices]
        g.vs["color"] = colors
        layout=g.layout("large_graph")

        ig.plot(g, margin = 20,bbox = (3000, 3000), layout=layout)
    def get_trajectory(self):
        start_node=self.mdp_dict['S'][0]
        ideal_path=[]
        ideal_path.append(str(start_node))
        policy=self.mdp_dict['pi']
        count=0
        while(1):
            act_node=ideal_path[-1]
            action=policy[act_node]
            if(count>self.param['n_optimal_trajectory']):
                break
            else:
                count+=1
            abc=self.mdp_dict['T']
            act_trans=abc[(act_node, action)]
            next_node=np.int(np.random.choice(len(self.mdp_dict['S']), 1, p=act_trans))
            ideal_path.append(self.mdp_dict['S'][next_node])
        print('ideal_path')
        print(ideal_path)
        return ideal_path



