from source.usecases.uc_scm.problem import *
class service_scmMDP(object):
    def __init__(self):
        self.problem=self.new_problem()

    def new_problem(self):
        obj = problem()
        obj.set_manifold()
        obj.set_solver()
        return obj

    def set_problem(self, problem):
        self.problem=problem

    def show_graph(self):
        self.problem.obj_solver.visualize_network()

if __name__ == '__main__':
    obj=service_scmMDP()
    obj.show_graph()

    t = obj.problem.obj_solver.get_scm_function(obj.problem.obj_solver.data, [Normal('x', 1.295, 0.273), Normal('v', 1.295, 0.273), Normal('v', 1.295, 0.273)])
    print(t)
    t = obj.problem.obj_solver.get_scm_function(obj.problem.obj_solver.data,
                                                [3, 4,
                                                 Normal('v', 1.295, 0.273)])
    print(t)