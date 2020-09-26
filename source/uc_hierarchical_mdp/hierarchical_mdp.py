import igraph as ig
import numpy as np
from scipy.cluster.vq import kmeans, vq
class hierarchical_mdp(object):
    def __init__(self, **kwargs):
        self.mdp_dict= {'S': None,  #Body States
                        'C': None,  # Cortex States
                   'action_body': None,  #Body Action set
                   'action_cortex': None,  # Cortex Action set
                   'adjacency_body': None,  #Topology environment
                   'adjacency_cortex': None,  # Topology
                   'R_body': None,  #Rewards
                   'R_cortex': None,  # Rewards
                   'gamma_body': 0.95,  #discount factor
                   'gamma_cortex': 0.85,  # discount factor
                   'P_body': None,  # Positions
                   'P_cortex': None  #Positions
                        }
        self.mdp_dict['T_body']=None
        self.mdp_dict['T_cortex'] = None
        self.mdp_dict['pi_cortex']=None
        self.mdp_dict['pi_body'] = None
        self.mdp_dict['U'] = None
        self.param = {'n_optimal_trajectory': 40, # optimal trajectory
                      }
    def set_position_cortex(self, position):
        self.mdp_dict['P_cortex']=position
    def set_position_body(self, position):
        self.mdp_dict['P_body']=position
    def set_T_body(self, transition):
        self.mdp_dict['T_body']=transition
    def set_T_cortex(self, transition):
        self.mdp_dict['T_cortex']=transition
    def set_U(self):
        self.mdp_dict['U'] = [[0] * len(self.mdp_dict['S']), [0] * len(self.mdp_dict['C'])]
    def set_action(self, action_body):
        self.mdp_dict['action_body']=action_body
    def set_action_body(self, action_body):
        self.mdp_dict['action_body']=action_body
    def set_action_cortex(self, action_cortex):
        self.mdp_dict['action_cortex']=action_cortex
    def set_init_pi_body(self):
        a={}
        for i in self.mdp_dict['S']:
            a[i]=self.mdp_dict['action_body'][i][0]
        self.mdp_dict['pi_body']=a
    def set_init_pi_cortex(self):
        a={}
        for i in self.mdp_dict['C']:
            a[i]=self.mdp_dict['action_cortex'][i][0]
        self.mdp_dict['pi_cortex']=a
    def set_S(self, S):
        self.mdp_dict['S']=S
    def set_C(self, C):
        self.mdp_dict['C']=C
    def set_R_body(self, dictR):
        val=list(dictR.values())
        keys=dictR.keys()
        self.mdp_dict['R_body']=np.zeros(len(self.mdp_dict['S']))
        for idx, q in enumerate(keys):
            self.mdp_dict['R_body'][int(q)]=val[idx]
    def set_R_cortex(self, dictR):
        val=list(dictR.values())
        keys=dictR.keys()
        self.mdp_dict['R_cortex']=np.zeros(len(self.mdp_dict['C']))
        for idx, q in enumerate(keys):
            self.mdp_dict['R_cortex'][int(q)]=val[idx]
    def set_T(self, T):
        self.mdp_dict['T']=T
    def set_adjacency_body(self, list):
        new_list=[]
        for i in list:
            a = self.mdp_dict['S'].index(i[0])
            b = self.mdp_dict['S'].index(i[1])
            new_list.append((a, b))
            new_list.append((a, a))
            #new_list.append((b, a))
        self.mdp_dict['adjacency_body']=new_list
    def set_adjacency_cortex(self, list):
        new_list=[]
        for i in list:
            a = self.mdp_dict['C'].index(i[0])
            b = self.mdp_dict['C'].index(i[1])
            new_list.append((a, b))
            new_list.append((a, a))
            #new_list.append((b, a))
        self.mdp_dict['adjacency_cortex']=new_list

    def policy_evaluation_cortex(self):
            for kp, p in enumerate(self.mdp_dict['C']):
                state_action=(p, self.mdp_dict['pi_cortex'][p])
                prob_dict=self.mdp_dict['T_cortex'][state_action]
                bds=self.mdp_dict['gamma_cortex']*np.sum([a * b for a, b in zip(self.mdp_dict['U'][1], prob_dict)])
                idx=np.int(np.random.choice(len(self.mdp_dict['C']), 1, p=prob_dict))
                self.mdp_dict['U'][1][kp]=self.mdp_dict['R_cortex'][idx]+bds
    def policy_evaluation_body(self):
            for kp, p in enumerate(self.mdp_dict['S']):
                state_action=(p, self.mdp_dict['pi_body'][p])
                prob_dict=self.mdp_dict['T_body'][state_action]
                bds=self.mdp_dict['gamma_body']*np.sum([a * b for a, b in zip(self.mdp_dict['U'][0], prob_dict)])
                idx=np.int(np.random.choice(len(self.mdp_dict['S']), 1, p=prob_dict))
                self.mdp_dict['U'][0][kp]=self.mdp_dict['R_body'][idx]+bds


    def policy_iteration_body(self):
            self.policy_evaluation_body()
            for kp, p in enumerate(self.mdp_dict['S']):
                all_Us = np.zeros(len(self.mdp_dict['action_body'][p]))
                for ka, act_a in enumerate(self.mdp_dict['action_body'][p]):
                    state_action=(p, act_a)
                    prob_dict=self.mdp_dict['T_body'][state_action]
                    bds=self.mdp_dict['gamma_body']*np.sum([a * b for a, b in zip(self.mdp_dict['U'][0], prob_dict)])
                    idx = np.int(np.random.choice(len(self.mdp_dict['S']), 1, p=prob_dict))
                    all_Us[ka]=self.mdp_dict['R_body'][idx] + bds
                self.get_new_policy_body(np.array(all_Us), kp)
    def policy_iteration_cortex(self):
            self.policy_evaluation_cortex()
            for kp, p in enumerate(self.mdp_dict['S']):
                all_Us = np.zeros(len(self.mdp_dict['action_cortex'][p]))
                for ka, act_a in enumerate(self.mdp_dict['action_cortex'][p]):
                    state_action=(p, act_a)
                    prob_dict=self.mdp_dict['T_cortex'][state_action]
                    bds=self.mdp_dict['gamma_cortex']*np.sum([a * b for a, b in zip(self.mdp_dict['U'][1], prob_dict)])
                    idx = np.int(np.random.choice(len(self.mdp_dict['C']), 1, p=prob_dict))
                    all_Us[ka]=self.mdp_dict['R_cortex'][idx] + bds
                self.get_new_policy_cortex(np.array(all_Us), kp)
    def get_new_policy_body(self, all_Us, act_node):
        idx=np.argmax(all_Us, axis=0)
        act_node_name=self.mdp_dict['S'][act_node]
        self.mdp_dict['pi_body'][act_node_name]=self.mdp_dict['action_body'][act_node_name][idx]
    def get_new_policy_cortex(self, all_Us, act_node):
        idx=np.argmax(all_Us, axis=0)
        act_node_name=self.mdp_dict['S'][act_node]
        self.mdp_dict['pi_cortex'][act_node_name]=self.mdp_dict['action_cortex'][act_node_name][idx]
      


    def start_mbmdp(self):
        count=0
        count2=0
        while(1):
            oldUBody=self.mdp_dict['U'][0][:]
            oldUCortex = self.mdp_dict['U'][1][:]
            self.policy_iteration_body()
            self.policy_iteration_cortex()
            if (np.sum(np.array(self.mdp_dict['U'][0]))==0 or np.sum(np.array(self.mdp_dict['U'][1]))==0):
                count += 1
                continue
            if(np.sum(np.array(self.mdp_dict['U'][0])-np.array(oldUBody))+np.sum(np.array(self.mdp_dict['U'][1])-np.array(oldUCortex))<10e-9):
                count += 1
                count2+=1
            if(count2>10):
                print("Convergence")
                print(count)
                print(self.mdp_dict['pi_cortex'])
                print(self.mdp_dict['pi_body'])
                print(self.mdp_dict['U'][0])
                print(self.mdp_dict['U'][1])
                break
            elif(count>1000):
                print("No Convergence")
                break

            count+=1

    def visualize_network_cortex(self):
        g = ig.Graph(self.mdp_dict['adjacency_cortex'])
        g.vs["name"] = self.mdp_dict['C']
        g.vs["reward"]= self.mdp_dict['R_cortex']
        g.vs["label"] = g.vs["name"]
        vec=np.array(self.mdp_dict['U'][1])
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

        layout = ig.Layout(self.mdp_dict['P_cortex'])
        g.vs["vertex_size"] = 20

        visual_style = {}
        visual_style["edge_curved"] = False
        out=ig.plot(g, layout=layout, **visual_style)
        out.save('../../output/cortex.png')

    def visualize_network_body(self):
        g = ig.Graph(self.mdp_dict['adjacency_body'])
        g.vs["name"] = self.mdp_dict['C']
        g.vs["reward"]= self.mdp_dict['R_body']
        g.vs["label"] = g.vs["name"]
        vec=np.array(self.mdp_dict['U'][0])
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

        layout = ig.Layout(self.mdp_dict['P_body'])
        g.vs["vertex_size"] = 20

        visual_style = {}
        visual_style["edge_curved"] = False
        out=ig.plot(g, layout=layout, **visual_style)
        out.save('../../output/body.png')

    def get_trajectory_body(self):
        start_node=self.mdp_dict['S'][0]
        ideal_path=[]
        ideal_path.append(str(start_node))
        policy_body=self.mdp_dict['pi_body']
        count=0
        while(1):
            act_node=ideal_path[-1]
            action=policy_body[act_node]
            if(count>self.param['n_optimal_trajectory']):
                break
            else:
                count+=1
            abc=self.mdp_dict['T_body']
            act_trans=abc[(act_node, action)]
            next_node=np.int(np.random.choice(len(self.mdp_dict['S']), 1, p=act_trans))
            ideal_path.append(self.mdp_dict['S'][next_node])
        print('ideal_path')
        print(ideal_path)
        return ideal_path

    def get_trajectory_cortex(self):
        start_node=self.mdp_dict['C'][0]
        ideal_path=[]
        ideal_path.append(str(start_node))
        policy_cortex=self.mdp_dict['pi_cortex']
        count=0
        while(1):
            act_node=ideal_path[-1]
            action=policy_cortex[act_node]
            if(count>self.param['n_optimal_trajectory']):
                break
            else:
                count+=1
            abc=self.mdp_dict['T_cortex']
            act_trans=abc[(act_node, action)]
            next_node=np.int(np.random.choice(len(self.mdp_dict['C']), 1, p=act_trans))
            ideal_path.append(self.mdp_dict['C'][next_node])
        print('ideal_path_cortex')
        print(ideal_path)
        return ideal_path


