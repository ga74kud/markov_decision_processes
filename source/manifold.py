

class manifold(object):
    def __init__(self, **kwargs):
        self.manifold= {'X': None, 'Topology': None, 'Atlas': None, 'Policy': None}
    def set_environment(self):
        self.manifold['X']=['A', 'B', 'C']
        self.manifold['Topology'] = [('A', 'B'), ('A', 'C'), ('B', 'C')]
        self.manifold['Atlas']= {'A': {'c': [0, 0], 'g':[[1, 0], [0, 1]]}, 'B': {'c': [1, 0], 'g':[[1, 0], [0, 1]]},
                                                                                'C': {'c': [0, 1], 'g':[[1, 0], [0, 1]]}}



if __name__ == '__main__':
    obj=manifold()
    obj.set_environment()
    print(obj.manifold)