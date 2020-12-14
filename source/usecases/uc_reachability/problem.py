# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Reachability Analysis on Topological Spaces
#
# (C) 2020 Michael Hartmann, Graz, Austria
# Released under TODO: find a release license
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------

from source.usecases.uc_reachability.reachability import *
from source.usecases.uc_reachability.manifold import *
class problem(object):
    def __init__(self, **kwargs):
        self.obj_manifold=None
        self.obj_solver=None

    """
    Set manifold
    """
    def set_manifold(self, FILE_DIR):
        self.obj_manifold=manifold()
        self.obj_manifold.set_environment_by_json(FILE_DIR)

    """
    Set solver information
    """
    def set_solver(self):
        self.obj_solver=reachability()
        self.obj_solver.set_S(self.obj_manifold.manifold['X'])
        self.obj_solver.set_adjacency_list(self.obj_manifold.manifold['Topology'])
        self.obj_solver.set_position_list(self.obj_manifold.manifold['Position'])
        self.obj_solver.set_action(self.obj_manifold.manifold["Actions"])
        self.obj_solver.set_T(self.obj_manifold.get_probability_nodes())

    """
    Reachability Analysis and visualization on igraph
    """
    def start_reach_solver(self, folder_to_store, storyline):
        params=util_io.get_params()

        self.obj_solver.start_reach_algorithm()
        all_reach_list=[]
        for wlt in range(1, params["reachability"]["amount_cycles"]+1):
            new_set=set(self.obj_solver.start_getting_reach_list(wlt, storyline))
            new_list=list(new_set)
            all_reach_list.append(new_list)
        self.obj_solver.visualize_network(folder_to_store, all_reach_list)
        return all_reach_list

if __name__ == '__main__':
    obj = problem()
    print(obj.obj_manifold.manifold)