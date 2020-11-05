from source.usecases.uc_pomdp.problem import *
class service_POMDP(object):
    def __init__(self):
        self.problem_type={"type": None, "Rewards": None}
        self.obj=None
    def show_graph(self):
        self.problem.obj_solver.visualize_network()
    def set_problem_type(self, problem_type):
        self.problem_type["type"]=problem_type['type']
        self.problem_type["rewards"]=problem_type['rewards']
    def new_problem(self, FILE_DIR):
        self.obj=problem()
        self.obj.set_manifold(FILE_DIR)
        self.obj.set_solver(self.problem_type["type"])
    def start_mdp(self):
        R_dict={"24": 10}
        ideal_path=self.obj.start_mdp_solver(R_dict)
        ideal_path = np.array([np.int(ideal_path[i]) for i in range(0, len(ideal_path))])
        return ideal_path

if __name__ == '__main__':
    obj=service_POMDP()
    obj.show_graph()
