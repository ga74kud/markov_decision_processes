from source.usecases.uc_reachability.problem import *
import source.util.data_input_loader as util_io
class service_reach(object):
    def __init__(self):
        self.problem_type={"type": None, "rewards": None}
        self.obj=None
    def set_rewards_by_param(self):
        param=util_io.get_params()
        self.problem_type["rewards"]=param["mdp"]["simulation"]["rewards"]
    def new_problem(self, FILE_DIR):
        self.obj=problem()
        self.obj.set_manifold(FILE_DIR)
        self.obj.set_solver()
    def start_reach(self, folder_to_store):
        dict_reach=self.obj.start_reachability(folder_to_store)

        return dict_reach

if __name__ == '__main__':
    obj=service_reach()