from source.manifold import *
from source.mdp import *
class problem(object):
    def __init__(self, **kwargs):
        self.obj_manifold=manifold()
        self.obj_solver=mdp()
        self.obj_manifold.set_environment_by_json()
        self.obj_solver.set_S(self.obj_manifold.manifold['X'])
        self.obj_solver.set_R({'1': 100})
        self.obj_solver.set_adjacency_list(self.obj_manifold.manifold['Topology'])
        self.obj_solver.set_U()
        self.obj_solver.set_action(['w', 'n', 'e', 's'])
        self.obj_solver.set_pi()
        self.obj_solver.set_T(self.obj_manifold.get_probability_nodes())
        self.obj_solver.start_mdp()
        self.obj_solver.visualize_network()

if __name__ == '__main__':
    obj = problem()
    print(obj.obj_manifold.manifold)