from source.uc_scm.manifold import *
from source.uc_scm.scm import *

class problem(object):
    def __init__(self, **kwargs):
        self.obj_manifold=None
        self.obj_solver=None
    def set_manifold(self):
        self.obj_manifold=manifold()
        self.obj_manifold.scm_import_json()

        #self.obj_manifold.get_topology_by_scm()

    def set_solver(self):
        self.obj_solver=scm_class()



if __name__ == '__main__':
    obj = problem()
    print(obj.obj_manifold.manifold)