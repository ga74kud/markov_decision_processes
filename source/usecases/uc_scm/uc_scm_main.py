from source.usecases.uc_scm.problem import *
class service_scmMDP(object):
    def __init__(self, problem):
        self.problem=self.new_problem(problem)

    def new_problem(self, problem_type):
        obj = problem()
        obj.set_manifold()
        obj.set_solver(problem_type['type'])
        return obj

    def set_problem(self, problem):
        self.problem=problem

    def show_graph(self):
        self.problem.obj_solver.visualize_network()

if __name__ == '__main__':
    problem_type = {'type': 'scm'}
    obj=service_scmMDP(problem_type)
    #init_problem=obj.new_problem()
    #obj.set_problem(init_problem)
    #obj.new_problem()
    obj.show_graph()