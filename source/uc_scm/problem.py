from source.uc_scm.manifold import *
from source.uc_scm.scm import *

class problem(object):
    def __init__(self, **kwargs):
        self.obj_manifold=None
        self.obj_solver=None
    def set_manifold(self):
        self.obj_manifold=manifold()
        self.obj_manifold.set_environment_by_json()

    def set_solver(self, type):
        self.obj_solver=scm_class()

    def start_mdp(self, R_dict):
        self.obj_solver.set_R(R_dict)
        self.obj_solver.start_mdp()
        self.obj_solver.get_trajectory()

if __name__ == '__main__':
    obj = problem()
    print(obj.obj_manifold.manifold)