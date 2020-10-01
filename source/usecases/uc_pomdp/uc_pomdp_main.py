from source.usecases.uc_pomdp.problem import *
class service_POMDP(object):
    def __init__(self, problem):
        self.problem=self.new_problem(problem)
    def show_graph(self):
        self.problem.obj_solver.visualize_network()

    def new_problem(self, problem_type):
        #problem_type={'type':'pomdp', 'rewards': {'24': 10}}
        obj=problem()
        obj.set_manifold()
        obj.set_solver(problem_type['type'])
        obj.start_mdp(problem_type['rewards'])
        return obj

if __name__ == '__main__':
    obj=service_POMDP()
    obj.show_graph()
