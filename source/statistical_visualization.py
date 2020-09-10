import seaborn as sns
from source.problem import *

class visualizer(object):
    def __init__(self, **kwargs):
        self.problem=self.new_problem()
    def show_graph(self):
        self.problem.obj_solver.visualize_network()

    def new_problem(self):
        obj=problem()
        obj.set_manifold()
        obj.set_solver()
        obj.start_mdp({'24': 10})
        return obj

if __name__ == '__main__':
    obj=visualizer()
    obj.show_graph()
