from source.usecases.uc_mdp.uc_mdp_main import *
from source.usecases.uc_scm.uc_scm_main import *
from source.util.map_loader import *
from source.util.visualizer import *
from source.util.visual_handler import *
from input.get_data import *


class service_handler(object):
    def __init__(self, **kwargs):
        self.visuals={"obj_visual": None, "obj_vectorfield": None, "obj_barplot": None}
        self.coordinates=None
        self.dict_mdp=None

    def use_cognitive_mdp(self):
        problem_type = {'type': 'cognitive_mdp', 'rewards_body': {'24': 10}, 'rewards_cortex': {'52': 10}}
        self.service_CognitiveMDP(problem_type)

    def use_scm_on_interpolated_line(self, folder_to_store, interpolated_points, points, cum_dist):
        interpolated_points=interpolated_points["quadratic"]
        obj = service_scmMDP(folder_to_store)
        obj.show_graph(folder_to_store)
        x_v_a=[0, 1, 1.295]
        mean_val_list={"interpolated_point": [], "cum_dist": [], "mean_val": [], "interpol_idx": []}
        idx=0
        mean_val_list["mean_val"].append(x_v_a)
        mean_val_list["cum_dist"].append(cum_dist[idx])
        mean_val_list["interpolated_point"].append(interpolated_points[idx,:])
        mean_val_list["interpol_idx"].append(idx)
        for wlt in range(0, 1000):
            x_v_a= obj.problem.obj_solver.get_scm_function_mean(obj.problem.obj_solver.data, x_v_a)
            x=x_v_a[0]
            l=list((cum_dist-x)**2)
            idx=l.index(min(l))
            mean_val_list["mean_val"].append(x_v_a)
            mean_val_list["cum_dist"].append(cum_dist[idx])
            mean_val_list["interpolated_point"].append(interpolated_points[idx, :])
            mean_val_list["interpol_idx"].append(idx)
            if (x_v_a[0]>cum_dist[-1]):
                break
        return mean_val_list

    def use_reach(self):
        None

    def use_monte_carlo(self):
        None

    def use_mdp(self, input_file, folder_to_store):
        obj_mdp=service_MDP()
        obj_mdp.set_rewards_by_param()
        obj_mdp.new_problem(input_file)
        dict_mdp=obj_mdp.start_mdp(folder_to_store)
        return dict_mdp

    def get_all_visual_objects(self):
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

    def set_dict_mdp(self, dict_mdp):
        self.dict_mdp=dict_mdp
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

        new_queue, optimal_path_list = util_io.optimal_path_for_queue(self.coordinates, self.dict_mdp)
        self.visuals["obj_vectorfield"].add_queue_optimalpath(new_queue)

        return optimal_path_list


def use_mdp_optimal_vectorfield(obj_service, obj_data_handler, input_file):
    # solver
    new_dict_mdp = obj_service.use_mdp(input_file, obj_data_handler.folder_to_store)
    obj_service.set_dict_mdp(new_dict_mdp)
    # add vectorfield plot
    optimal_path_list = obj_service.add_vectorfield_queue()
    obj_service.visuals["obj_vectorfield"].show_plot(obj_data_handler.folder_to_store + "vectorfield.png")

    # write optimal path to tmp.json
    obj_data_handler.update_json_with_dictionary(optimal_path_list)

    # get result trajectories with spline interpolation
    interpolated_points, points=util_io.get_result_trajectories_mdp(optimal_path_list["act_node"], obj_service.coordinates,
                                        obj_data_handler.folder_to_store)
    cum_dist=util_io.get_cumultative_distance(obj_data_handler.folder_to_store, interpolated_points)
    return interpolated_points, cum_dist, points
def pre_processing():
    # object from data handler
    obj_data_handler = service_data()
    obj_data_handler.set_initial_folder()
    obj_data_handler.set_initial_json()
    # obj_data_handler.update_json_with_dictionary({"abc": "123"})

    input_file = obj_data_handler.get_input_file()
    # object for solver handling
    obj_service = service_handler()

    # visualizer objects for plotting results
    obj_service.get_all_visual_objects()

    # environmental information
    obj_service.get_environmental_information(input_file)
    return obj_service, obj_data_handler, input_file
def use_scm_for_velocity(obj_visual, interpolated_points, cum_dist, points):
    mean_val_list = obj_service.use_scm_on_interpolated_line(obj_data_handler.folder_to_store, interpolated_points,
                                                             points, cum_dist)
    util_io.plot_mean_value(obj_data_handler.folder_to_store, mean_val_list)
    util_io.plot_traj(obj_visual, interpolated_points, points, obj_data_handler.folder_to_store, mean_val_list)
if __name__ == '__main__':
    obj_visual=visual_handler()
    obj_service, obj_data_handler, input_file=pre_processing()
    interpolated_points, cum_dist, points=use_mdp_optimal_vectorfield(obj_service, obj_data_handler, input_file)
    use_scm_for_velocity(obj_visual.figures["interp_traj"], interpolated_points, cum_dist, points)

