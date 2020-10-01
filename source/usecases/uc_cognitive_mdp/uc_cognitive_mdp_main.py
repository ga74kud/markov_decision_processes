from source.usecases.uc_cognitive_mdp.problem import *
class service_CognitiveMDP(object):
    def __init__(self, problem):
        self.problem=self.new_problem(problem)
    def show_graph(self):
        self.problem.obj_solver.visualize_network_cortex()
        self.problem.obj_solver.visualize_network_body()

    def new_problem(self, problem_type):
        #problem_type={'rewards_body': {'24': 10}, 'rewards_cortex': {'52': 10}}
        obj=problem()
        obj.set_manifold()
        obj.set_solver()
        obj.start_mbmdp_process(problem_type)
        return obj

if __name__ == '__main__':
    obj=service_CognitiveMDP()
    obj.show_graph()
