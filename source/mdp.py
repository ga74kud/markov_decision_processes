import igraph as ig
import numpy as np

class mdp(object):
    def __init__(self, **kwargs):
        self.mdp= {'S': ['A', 'B', 'C'], 'action': ['s', 'g'], 'adjacency_list': None, 'R': [30, 2, 1], 'N': 2, 'gamma': 0.9}
        self.mdp['T'] = {('A', 's'): [0.8, 0.1, 0.1],
                         ('B', 's'): [0.1, 0.8, 0.1],
                         ('C', 's'): [0.1, 0.1, 0.8],
                         ('A', 'g'): [0.0, 0.8, 0.2],
                         ('B', 'g'): [0.2, 0.0, 0.8],
                         ('C', 'g'): [0.8, 0.2, 0.0]}
        self.mdp['pi'] = {'A': 's', 'B': 's', 'C': 'g'}
        self.mdp['U'] = [0] * len(self.mdp['S'])

    def set_S(self, S):
        self.mdp['S']=S
    def set_R(self, R):
        self.mdp['R']=R
    def set_T(self, T):
        self.mdp['T']=T
    def set_adjacency_list(self, list):
        new_list=[]
        for i in list:
            a = self.mdp['S'].index(i[0])
            b = self.mdp['S'].index(i[1])
            new_list.append((a,b))
        self.mdp['adjacency_list']=new_list

    def policy_evaluation(self):
        for k in range(1, self.mdp['N']):
            for kp, p in enumerate(self.mdp['S']):
                state_action=(p, self.mdp['pi'][p])
                prob_dict=self.mdp['T'][state_action]
                bds=self.mdp['gamma']*np.sum([a * b for a, b in zip(self.mdp['U'], prob_dict)])
                idx=np.int(np.random.choice(len(self.mdp['S']), 1, p=prob_dict))
                self.mdp['U'][kp]=self.mdp['R'][idx]+bds
            return self.mdp['U']

    def policy_iteration(self):
        for k in range(1, self.mdp['N']):
            actual_U=self.policy_evaluation()
            all_Us=np.zeros((len(self.mdp['action']), len(self.mdp['S'])))
            for ka, act_a in enumerate(self.mdp['action']):
                for kp, p in enumerate(self.mdp['S']):
                    state_action=(p, act_a)
                    prob_dict=self.mdp['T'][state_action]
                    bds=self.mdp['gamma']*np.sum([a * b for a, b in zip(actual_U, prob_dict)])
                    idx = np.int(np.random.choice(len(self.mdp['S']), 1, p=prob_dict))
                    all_Us[ka][kp]=self.mdp['R'][idx] + bds
            self.get_new_policy(np.array(all_Us))
    def get_new_policy(self, all_Us):
        idx=np.argmax(all_Us, axis=0)
        for ka, qrt in enumerate(self.mdp['pi'].keys()):
            self.mdp['pi'][qrt]=self.mdp['action'][idx[ka]]
      


    def start_mdp(self):
        count=1
        while(1):
            oldU=self.mdp['U'][:]
            self.policy_iteration()
            if(np.sum(np.array(self.mdp['U'])-np.array(oldU))<10e-3):
                print("Convergence")
                print(count)
                print(self.mdp['pi'])
                print(self.mdp['U'])
                break
            elif(count>1000):
                print("No Convergence")
                break

            count+=1

    def visualize_network(self):
        g = ig.Graph(self.mdp['adjacency_list'])
        g.vs["name"] = self.mdp['S']
        g.vs["reward"]= self.mdp['R']
        g.vs["label"] = g.vs["name"]
        color_dict = {0: "blue", 1: "green", 2: "cyan", 3: "yellow", 4: "pink", 5: "pink", 6: "pink", 7: "pink", 8: "pink", 9: "orange", 10: "red"}
        g.vs["color"] = [color_dict[r] for r in g.vs["reward"]]
        #[(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6)])
        ig.plot(g, bbox = (300, 300), margin = 20)

