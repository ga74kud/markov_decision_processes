from source.usecases.uc_reachability.reachability import *
from source.usecases.uc_reachability.manifold import *
class problem(object):
    def __init__(self, **kwargs):
        self.obj_manifold=None
        self.obj_solver=None
    def set_manifold(self, FILE_DIR):
        self.obj_manifold=manifold()
        self.obj_manifold.set_environment_by_json(FILE_DIR)

    def set_solver(self):
        self.obj_solver=reachability()
        self.obj_solver.set_S(self.obj_manifold.manifold['X'])
        self.obj_solver.set_adjacency_list(self.obj_manifold.manifold['Topology'])
        self.obj_solver.set_position_list(self.obj_manifold.manifold['Position'])
        self.obj_solver.set_action(self.obj_manifold.manifold["Actions"])
        self.obj_solver.set_T(self.obj_manifold.get_probability_nodes())
    def start_reach_solver(self, folder_to_store):
        dict_reach = self.obj_solver.start_reach_algorithm()
        self.obj_solver.visualize_network(folder_to_store)
        return dict_reach

if __name__ == '__main__':
    obj = problem()
    print(obj.obj_manifold.manifold)