from source.usecases.uc_mdp.manifold import *
from source.usecases.uc_mdp.mdp import *

class problem(object):
    def __init__(self, **kwargs):
        self.obj_manifold=None
        self.obj_solver=None
    def set_manifold(self, FILE_DIR):
        self.obj_manifold=manifold()
        self.obj_manifold.set_environment_by_json(FILE_DIR)

    def set_solver(self):
        self.obj_solver=mdp()
        self.obj_solver.set_S(self.obj_manifold.manifold['X'])
        self.obj_solver.set_adjacency_list(self.obj_manifold.manifold['Topology'])
        self.obj_solver.set_position_list(self.obj_manifold.manifold['Position'])
        self.obj_solver.set_U()
        self.obj_solver.set_action(self.obj_manifold.manifold["Actions"])
        self.obj_solver.set_init_pi()
        abc=self.obj_manifold.get_probability_nodes()
        self.obj_solver.set_T(abc)
    def start_mdp_solver(self, rewards, folder_to_store):
        R_dict = rewards
        self.obj_solver.set_R(R_dict)
        dict_mdp = self.obj_solver.start_mdp_algorithm()
        self.obj_solver.get_all_policy_options()
        self.obj_solver.visualize_network(folder_to_store)
        return dict_mdp

if __name__ == '__main__':
    obj = problem()
    print(obj.obj_manifold.manifold)