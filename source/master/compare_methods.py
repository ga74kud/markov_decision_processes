from source.usecases.uc_mdp.uc_mdp_main import *
from source.util.map_loader import *
from source.util.visualizer import *
from input.get_data import *

class service_handler(object):
    def __init__(self, **kwargs):
        self.visuals={"obj_visual": None, "obj_vectorfield": None, "obj_barplot": None}
        self.coordinates=None
        self.dict_mdp=None

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

    def get_all_visual_objects(self):

        # object from visualizer class
        self.visuals["obj_visual"] = service_visualizer()
        self.visuals["obj_visual"].init_plotter()
        self.visuals["obj_visual"].show_grid()

        # object from visualizer class
        self.visuals["obj_vectorfield"] = service_visualizer()
        self.visuals["obj_vectorfield"].init_plotter()
        self.visuals["obj_vectorfield"].show_grid()

        # object from visualizer class
        self.visuals["obj_barplot"] = service_visualizer()
        self.visuals["obj_barplot"].init_plotter()
        self.visuals["obj_barplot"].show_grid()

    def get_environmental_information(self, input_file):

        # object from environment class
        obj_map = map_loader()
        self.coordinates = obj_map.preprocessing(input_file)
    def get_solver_information(self, input_file):

        # object for solver handling
        obj_service = service_handler()
        self.dict_mdp = obj_service.use_all_solvers(input_file)
    def add_visuals_queue(self):

        # add map to queue
        new_queue = util_io.map_for_queue(self.coordinates)
        self.visuals["obj_visual"].add_queue(new_queue)

        new_queue = util_io.trajectory_for_queue(self.coordinates, self.dict_mdp["ideal_path"])
        self.visuals["obj_visual"].add_queue(new_queue)

    def add_vectorfield_queue(self):

        new_queue = util_io.map_for_queue(self.coordinates)
        self.visuals["obj_vectorfield"].add_queue(new_queue)

        self.visuals["obj_vectorfield"].add_queue_delauny(new_queue)

        new_queue = util_io.vectorfield_for_queue(self.coordinates, self.dict_mdp)
        self.visuals["obj_vectorfield"].add_queue_vectorfield(new_queue)
        self.visuals["obj_vectorfield"].add_queue_topology(new_queue)

        new_queue = util_io.optimal_path_for_queue(self.coordinates, self.dict_mdp)
        self.visuals["obj_vectorfield"].add_queue_optimalpath(new_queue)



if __name__ == '__main__':

    # object from data handler
    obj_data_handler = service_data()
    input_file = obj_data_handler.get_input_file()
    # object for solver handling
    obj_service = service_handler()

    # visualizer objects for plotting results
    obj_service.get_all_visual_objects()

    # environmental information
    obj_service.get_environmental_information(input_file)

    # solver
    obj_service.get_solver_information(input_file)

    # add visual plot
    obj_service.add_visuals_queue()
    obj_service.visuals["obj_visual"].show_plot()

    # add vectorfield plot
    obj_service.add_vectorfield_queue()
    obj_service.visuals["obj_vectorfield"].show_plot()

    # add barplot for value function
    obj_service.add_vectorfield_queue()
    obj_service.visuals["obj_barplot"].show_plot()

    # get result trajectories
    util_io.get_result_trajectories_mdp(obj_service.dict_mdp["ideal_path"], obj_service.coordinates)
