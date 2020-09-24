import seaborn as sns
from source.uc_hierarchical_mdp.problem import *
class visualizer(object):
    def __init__(self, **kwargs):
        self.problem=self.new_problem()
    def show_graph(self):
        self.problem.obj_solver.visualize_network_cortex()
        self.problem.obj_solver.visualize_network_body()

    def new_problem(self):
        problem_type={'rewards_body': {'24': 10}, 'rewards_cortex': {'10': 10}}
        obj=problem()
        obj.set_manifold()
        obj.set_solver()
        obj.start_mbmdp_process(problem_type)
        return obj

if __name__ == '__main__':
    obj=visualizer()
    obj.show_graph()
