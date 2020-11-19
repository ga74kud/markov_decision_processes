from source.usecases.uc_mdp.uc_mdp_main import *
from source.util.map_loader import *
from source.util.visualizer import *
import source.util.data_input_loader as util_io
from input.get_data import *
from collections import OrderedDict


class service_handler(object):
    def __init__(self, **kwargs):
        None
    def use_all_solvers(self, input_file):
        optimal_path_mdp=self.use_mdp(input_file)
        return optimal_path_mdp
    def use_cognitive_mdp(self):
        problem_type = {'type': 'cognitive_mdp', 'rewards_body': {'24': 10}, 'rewards_cortex': {'52': 10}}
        self.service_CognitiveMDP(problem_type)
    def use_scm(self):
        problem_type = {'type': 'scm'}
        self.service_scmMDP(problem_type)
    def use_reach(self):
        None
    def use_monte_carlo(self):
        None
    def use_mdp(self, input_file):
        problem={'type': 'mdp', 'rewards': {'95': 100000}}
        obj_mdp=service_MDP()
        obj_mdp.set_problem_type(problem)
        obj_mdp.new_problem(input_file)
        ideal_path=obj_mdp.start_mdp(problem)

        return ideal_path

if __name__ == '__main__':
    # object from data handler
    obj_data_handler=service_data()
    input_file=obj_data_handler.get_input_file()
    obj_data=service_data()
    # object from visualizer class
    obj_visual = service_visualizer()
    obj_visual.init_plotter()
    obj_visual.show_grid()

    # object from visualizer class
    obj_vectorfield = service_visualizer()
    obj_vectorfield.init_plotter()
    obj_vectorfield.show_grid()

    cmap=np.array(plt.get_cmap("plasma").colors)

    # object from environment class
    obj_map=map_loader()

    coordinates=obj_map.preprocessing(input_file)

    # kmeans for large data
        #ref, daski=obj_map.classify_to_meta()
        #obj_map.save_semantic_kmeans(daski)

    # object for solver handling
    obj_service=service_handler()
    optimal_mdp=obj_service.use_all_solvers(input_file)


    # add map to queue
    new_queue = util_io.map_for_queue(coordinates)
    obj_visual.add_queue(new_queue)


    new_queue=util_io.trajectory_for_queue(coordinates, optimal_mdp)
    obj_visual.add_queue(new_queue)
    #new_queue = util_io.reach_for_queue(coordinates, reach_mdp)
    #all_queue_to_plot.append(new_queue)

    obj_visual.show_plot()

    new_queue = util_io.map_for_queue(coordinates)
    obj_vectorfield.add_queue(new_queue)
    obj_vectorfield.show_plot()

    #get result trajectories
    util_io.get_result_trajectories_mdp(optimal_mdp, coordinates)
