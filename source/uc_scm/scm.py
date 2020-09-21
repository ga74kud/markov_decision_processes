import igraph as ig

from source.uc_pomdp.pomdp import *

class scm_class(object):
    def __init__(self, **kwargs):
        None

    def set_adjacency_list(self, nodes, list):
        new_list = []
        for i in list:
            a = nodes.index(i[0])
            b = nodes.index(i[1])
            new_list.append((a, b))
            #new_list.append((a, a))
            # new_list.append((b, a))
        return new_list
    def visualize_network(self, obj):
        nodes=obj.manifold['X']
        adjacency=self.set_adjacency_list(nodes, obj.manifold['Topology'])
        g = ig.Graph(adjacency)
        g.vs["name"] = nodes
        g.vs["label"] = g.vs["name"]
        g.vs["vertex_size"] = 20
        visual_style = {}
        visual_style["edge_curved"] = False
        ig.plot(g, **visual_style)#margin = 20,bbox = (3000, 3000), layout=layout,


