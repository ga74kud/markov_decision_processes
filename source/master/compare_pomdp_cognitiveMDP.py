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
        dict_mdp=self.use_mdp(input_file)
        return dict_mdp
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
        dict_mdp=obj_mdp.start_mdp(problem)

        return dict_mdp

def get_all_visual_objects():
    # object from visualizer class
    obj_visual = service_visualizer()
    obj_visual.init_plotter()
    obj_visual.show_grid()

    # object from visualizer class
    obj_vectorfield = service_visualizer()
    obj_vectorfield.init_plotter()
    obj_vectorfield.show_grid()
    return obj_visual, obj_vectorfield

def get_data_handlers():
    # object from data handler
    obj_data_handler = service_data()
    input_file = obj_data_handler.get_input_file()
    return obj_data_handler, input_file

def get_environmental_information(input_file):
    # object from environment class
    obj_map = map_loader()

    coordinates = obj_map.preprocessing(input_file)
    return coordinates
if __name__ == '__main__':
    obj_data_handler, input_file=get_data_handlers()

    #visualizer objects for plotting results
    obj_visual, obj_vectorfield=get_all_visual_objects()

    coordinates=get_environmental_information(input_file)

    # object for solver handling
    obj_service=service_handler()
    dict_mdp=obj_service.use_all_solvers(input_file)


    # add map to queue
    new_queue = util_io.map_for_queue(coordinates)
    obj_visual.add_queue(new_queue)


    new_queue=util_io.trajectory_for_queue(coordinates, dict_mdp["ideal_path"])
    obj_visual.add_queue(new_queue)
    #new_queue = util_io.reach_for_queue(coordinates, reach_mdp)
    #all_queue_to_plot.append(new_queue)

    obj_visual.show_plot()

    new_queue = util_io.map_for_queue(coordinates)
    obj_vectorfield.add_queue(new_queue)
    obj_vectorfield.show_plot()

    #get result trajectories
    util_io.get_result_trajectories_mdp(dict_mdp["ideal_path"], coordinates)
