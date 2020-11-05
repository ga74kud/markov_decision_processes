from source.usecases.uc_pomdp.manifold import *
from source.usecases.uc_pomdp.pomdp import *
from source.usecases.uc_pomdp.reachability import *

class problem(object):
    def __init__(self, **kwargs):
        self.obj_manifold=None
        self.obj_solver=None
    def set_manifold(self, FILE_DIR):
        self.obj_manifold=manifold()
        self.obj_manifold.set_environment_by_json(FILE_DIR)

    def set_solver(self, type):
        if(type=='pomdp'):
            self.obj_solver=pomdp_class()
        elif(type=='reachability'):
            self.obj_solver = reachability()
        self.obj_solver.set_S(self.obj_manifold.manifold['X'])
        self.obj_solver.set_adjacency_list(self.obj_manifold.manifold['Topology'])
        self.obj_solver.set_position_list(self.obj_manifold.manifold['Position'])
        self.obj_solver.set_U()
        self.obj_solver.set_action(self.obj_manifold.manifold["Actions"])
        self.obj_solver.set_init_pi()
        self.obj_solver.set_T(self.obj_manifold.get_probability_nodes())
    def start_mdp_solver(self, R_dict):
        self.obj_solver.set_R(R_dict)
        self.obj_solver.start_mdp()
        ideal_path=self.obj_solver.get_trajectory()
        return ideal_path

if __name__ == '__main__':
    obj = problem()
    print(obj.obj_manifold.manifold)