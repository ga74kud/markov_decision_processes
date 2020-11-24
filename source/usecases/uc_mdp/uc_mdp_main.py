from source.usecases.uc_mdp.problem import *
import source.util.data_input_loader as util_io
class service_MDP(object):
    def __init__(self):
        self.problem_type={"type": None, "rewards": None}
        self.obj=None
    def show_graph(self):
        self.problem.obj_solver.visualize_network()
    def set_rewards_by_param(self):
        param=util_io.get_params()
        self.problem_type["rewards"]=param["mdp"]["simulation"]["rewards"]
    def new_problem(self, FILE_DIR):
        self.obj=problem()
        self.obj.set_manifold(FILE_DIR)
        self.obj.set_solver()
    def start_mdp(self):
        dict_mdp=self.obj.start_mdp_solver(self.problem_type["rewards"])
        return dict_mdp

if __name__ == '__main__':
    obj=service_MDP()
    obj.show_graph()
