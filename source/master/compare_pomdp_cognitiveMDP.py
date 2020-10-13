from source.util.map_handling import *

from source.usecases.uc_pomdp.uc_pomdp_main import *
from source.usecases.uc_cognitive_mdp.uc_cognitive_mdp_main import *
from source.usecases.uc_scm.uc_scm_main import *

class service_handler(object):
    def __init__(self, **kwargs):
        None
    def get_map(self):
        obj=service_map_handling()
        obj.show_prob_example()
    def use_all_solvers(self):
        problem={'type': 'pomdp', 'rewards': {'24': 10}}
        service_POMDP(problem)
        problem_type = {'type': 'cognitive_mdp', 'rewards_body': {'24': 10}, 'rewards_cortex': {'52': 10}}
        service_CognitiveMDP(problem_type)
        problem_type = {'type': 'scm'}
        service_scmMDP(problem_type)

if __name__ == '__main__':
    obj=service_handler()
    #obj.get_map()
