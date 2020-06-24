

class manifold(object):
    def __init__(self, **kwargs):
        self.manifold= {'X': None, 'Topology': None, 'Atlas': None, 'Rewards': None}
    def set_environment(self):
        self.manifold['X']=['A', 'B', 'C', 'D']
        self.manifold['Topology'] = [('A', 'B'), ('A', 'C'), ('C', 'D'), ('A', 'D')]
        self.manifold['Atlas']= {'A': {'c': [0, 0], 'g':[[1, 0], [0, 1]]}, 'B': {'c': [1, 0], 'g':[[1, 0], [0, 1]]},
                                                                                'C': {'c': [0, 1], 'g':[[1, 0], [0, 1]]},
                                                                                      'D': {'c': [1, 1], 'g':[[1, 0], [0, 1]]}}
        self.manifold['Rewards']=[3, 2, 1, 4]

if __name__ == '__main__':
    obj=manifold()
    obj.set_environment()
    print(obj.manifold)