from source.uc_scm.problem import *
class visualizer(object):
    def __init__(self, **kwargs):
        self.problem=self.new_problem()

    def new_problem(self):
        obj=problem()
        obj.set_manifold()
        obj.set_solver()
        return obj
    def show_graph(self):
        self.problem.obj_solver.visualize_network(self.problem.obj_manifold)

if __name__ == '__main__':
    obj=visualizer()
    obj.show_graph()