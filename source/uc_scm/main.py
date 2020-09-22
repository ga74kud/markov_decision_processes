from source.uc_scm.problem import *
class visualizer(object):
    def __init__(self, **kwargs):
        self.problem=None

    def set_problem(self, problem):
        self.problem=problem
    def new_problem(self):
        self.problem.set_manifold()
        self.problem.set_solver()
    def show_graph(self):
        self.problem.obj_solver.visualize_network()

if __name__ == '__main__':
    obj=visualizer()
    init_problem=problem()
    obj.set_problem(init_problem)
    obj.new_problem()
    obj.show_graph()