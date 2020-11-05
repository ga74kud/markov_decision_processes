from source.util.map_handling import *
from source.usecases.uc_pomdp.uc_pomdp_main import *
from source.util.map_loader import *

class service_handler(object):
    def __init__(self, **kwargs):
        None
    def use_all_solvers(self):
        problem={'type': 'pomdp', 'rewards': {'24': 10}}
        obj_pomdp=service_POMDP()
        obj_pomdp.set_problem_type(problem)
        obj_pomdp.new_problem()
        ideal_path=obj_pomdp.start_mdp()
        b=2
        #problem_type = {'type': 'cognitive_mdp', 'rewards_body': {'24': 10}, 'rewards_cortex': {'52': 10}}
        #service_CognitiveMDP(problem_type)
        #problem_type = {'type': 'scm'}
        #service_scmMDP(problem_type)

if __name__ == '__main__':
    km=load_semantic_dataset()
    save_semantic_kmeans(km)
    obj=service_handler()
    obj.use_all_solvers()

