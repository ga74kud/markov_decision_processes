from source.util.map_handling import *
from source.usecases.uc_pomdp.uc_pomdp_main import *
from source.util.map_loader import *

class service_handler(object):
    def __init__(self, **kwargs):
        None
    def use_all_solvers(self):
        self.use_mdp()
        b=2
    def use_cognitive_mdp(self):
        None
        # problem_type = {'type': 'cognitive_mdp', 'rewards_body': {'24': 10}, 'rewards_cortex': {'52': 10}}
        # service_CognitiveMDP(problem_type)
    def use_scm(self):
        None
        # problem_type = {'type': 'scm'}
        # service_scmMDP(problem_type)
    def use_mdp(self):
        problem={'type': 'pomdp', 'rewards': {'24': 10}}
        obj_pomdp=service_POMDP()
        obj_pomdp.set_problem_type(problem)
        obj_pomdp.new_problem()
        ideal_path=obj_pomdp.start_mdp()
        return ideal_path

if __name__ == '__main__':
    obj_map=map_loader()
    ref, daski=obj_map.classify_to_meta()
    obj_map.save_semantic_kmeans(daski)
    obj_service=service_handler()
    obj_service.use_all_solvers()
    obj_map.show_pyvista(ref, daski)
    obj_map.show_plot()

