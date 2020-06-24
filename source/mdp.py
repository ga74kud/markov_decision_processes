import igraph as ig


class mdp(object):
    def __init__(self, **kwargs):
        self.mdp= {'S': None, 'adjacency_list': None, 'R': None}

    def set_S(self, S):
        self.mdp['S']=S
    def set_R(self, R):
        self.mdp['R']=R
    def set_adjacency_list(self, list):
        new_list=[]
        for i in list:
            a = self.mdp['S'].index(i[0])
            b = self.mdp['S'].index(i[1])
            new_list.append((a,b))
        self.mdp['adjacency_list']=new_list

    def visualize_network(self):
        g = ig.Graph(self.mdp['adjacency_list'])
        g.vs["name"] = self.mdp['S']
        g.vs["reward"]= self.mdp['R']
        g.vs["label"] = g.vs["name"]
        color_dict = {0: "blue", 1: "green", 2: "cyan", 3: "yellow", 4: "pink", 5: "pink", 6: "pink", 7: "pink", 8: "pink", 9: "orange", 10: "red"}
        g.vs["color"] = [color_dict[r] for r in g.vs["reward"]]
        #[(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6)])
        ig.plot(g, bbox = (300, 300), margin = 20)

