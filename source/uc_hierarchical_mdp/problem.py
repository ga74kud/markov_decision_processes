from source.uc_hierarchical_mdp.manifold import *
from source.uc_hierarchical_mdp.hierarchical_mdp import *

class problem(object):
    def __init__(self, **kwargs):
        self.obj_manifold_environment=None
        self.obj_manifold_cortex = None
        self.obj_solver=None
    def set_manifold(self):
        self.obj_manifold_environment=manifold()
        self.obj_manifold_cortex=manifold()
        self.obj_manifold_environment.set_environment_by_json()
        self.obj_manifold_cortex.set_environment_by_json()

    def set_solver(self):
        self.obj_solver=hierarchical_mdp()
        #environment states
        self.obj_solver.set_S(self.obj_manifold_environment.manifold['X'])
        #cortex states
        self.obj_solver.set_C(self.obj_manifold_cortex.manifold['X'])

        #environment topology
        self.obj_solver.set_adjacency_body(self.obj_manifold_environment.manifold['Topology'])
        #cortex topology
        self.obj_solver.set_adjacency_cortex(self.obj_manifold_cortex.manifold['Topology'])
        #position
        self.obj_solver.set_position_body(self.obj_manifold_environment.manifold['Position'])
        #position
        self.obj_solver.set_position_cortex(self.obj_manifold_cortex.manifold['Position'])

        self.obj_solver.set_U()

        #body actions
        self.obj_solver.set_action_body(self.obj_manifold_environment.manifold["Actions"])
        #cortex actions
        self.obj_solver.set_action_cortex(self.obj_manifold_cortex.manifold["Actions"])
        #policy body
        self.obj_solver.set_init_pi_body()
        #policy cortex
        self.obj_solver.set_init_pi_cortex()


        #body transition
        self.obj_solver.set_T_body(self.obj_manifold_environment.get_probability_nodes())
        #cortex transition
        self.obj_solver.set_T_cortex(self.obj_manifold_cortex.get_probability_nodes())

    def start_mbmdp_process(self, R_dict):
        self.obj_solver.set_R_cortex(R_dict['rewards_cortex'])
        self.obj_solver.set_R_body(R_dict['rewards_body'])
        self.obj_solver.start_mbmdp()
        self.obj_solver.get_trajectory_body()
        self.obj_solver.get_trajectory_cortex()


if __name__ == '__main__':
    obj = problem()
    print(obj.obj_manifold.manifold)