from source.usecases.uc_mdp.problem import *
class service_MDP(object):
    def __init__(self):
        self.problem_type={"type": None, "rewards": None}
        self.obj=None
    def show_graph(self):
        self.problem.obj_solver.visualize_network()
    def set_problem_type(self, problem_type):
        self.problem_type["type"]=problem_type['type']
        self.problem_type["rewards"]=problem_type['rewards']
    def new_problem(self, FILE_DIR):
        self.obj=problem()
        self.obj.set_manifold(FILE_DIR)
        self.obj.set_solver(self.problem_type["type"])
    def start_mdp(self, problem):
        dict_mdp=self.obj.start_mdp_solver(problem)
        return dict_mdp

if __name__ == '__main__':
    obj=service_MDP()
    obj.show_graph()
