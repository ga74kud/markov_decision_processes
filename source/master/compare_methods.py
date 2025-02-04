# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Markov Decision Process (MDP) + Structural Causal Model (SCM) and Reachability Analysis (RA)
#
# (C) 2020 Michael Hartmann, Graz, Austria
# Released under TODO: find a release license
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------
from source.usecases.uc_mdp.uc_mdp_main import *
from source.usecases.uc_scm.uc_scm_main import *
from source.usecases.uc_reachability.uc_reach_main import *
from source.util.map_loader import *
from source.util.visualizer import *
from source.util.visual_handler import *
from source.util.causal_prob import *
from input.get_data import *

"""
Main class for Markov Decision Process (MDP) + SCM + Reachabiltiy Analysis (RA)
"""
class service_handler(object):
    def __init__(self, **kwargs):
        # visual objects
        self.visuals={"obj_visual": None, "obj_vectorfield": None, "obj_barplot": None}
        # coordinates
        self.coordinates=None
        # dictionary for mdp results
        self.dict_mdp=None
        # dictionary for reachability analysis results
        self.dict_reach=None
        # rewards
        self.dict_rewards=None

    """
    MDP provides an optimal trajectory and on the trajectory the structural causal model (SCM) computes the velocity
    """
    def use_scm_on_interpolated_line(self, x_v_a, folder_to_store, interpolated_points, cum_dist, with_intervention):
        interpolated_points=interpolated_points["quadratic"]
        obj = service_scmMDP(folder_to_store)
        obj.show_graph(folder_to_store)
        mean_val_list={"interpolated_point": [], "cum_dist": [], "mean_val": [], "interpol_idx": []}
        intervention_list = {"interpolated_point": [], "cum_dist": [], "mean_val": [], "interpol_idx": []}
        idx=0
        mean_val_list["mean_val"].append(x_v_a)
        mean_val_list["cum_dist"].append(cum_dist[idx])
        mean_val_list["interpolated_point"].append(interpolated_points[idx,:])
        mean_val_list["interpol_idx"].append(idx)
        for wlt in range(0, 1000):
            x_v_a= obj.problem.obj_solver.get_scm_function_mean(obj.problem.obj_solver.data, x_v_a)
            x=x_v_a[0]
            if(with_intervention and wlt>24):
                intervention_list["mean_val"].append(x_v_a)
                intervention_list["cum_dist"].append(cum_dist[idx])
                intervention_list["interpolated_point"].append(interpolated_points[idx, :])
                intervention_list["interpol_idx"].append(idx)
                x_v_a[3]=2
            l=list((cum_dist-x)**2)
            idx=l.index(min(l))
            mean_val_list["mean_val"].append(x_v_a)
            mean_val_list["cum_dist"].append(cum_dist[idx])
            mean_val_list["interpolated_point"].append(interpolated_points[idx, :])
            mean_val_list["interpol_idx"].append(idx)
            if (x_v_a[0]>cum_dist[-1]):
                break
        return mean_val_list, intervention_list

    """
    Object for reachability analysis 
    """
    def use_reach(self, input_file, folder_to_store, storyline):
        obj_reach=service_reach()
        obj_reach.new_problem(input_file)
        all_reach_list=obj_reach.start_reach(folder_to_store, storyline)
        return all_reach_list

    """
    Markov Decision Process 
    """
    def use_mdp(self, input_file, folder_to_store, storyline):
        obj_mdp=service_MDP()
        obj_mdp.set_rewards(storyline["rewards"])
        obj_mdp.new_problem(input_file)
        dict_mdp=obj_mdp.start_mdp(folder_to_store)
        return dict_mdp


    """
    Start visualizer objects for illustration in PyVista
    """
    def get_all_visual_objects(self):
        # object from visualizer class
        self.visuals["obj_vectorfield"] = service_visualizer()
        self.visuals["obj_vectorfield"].init_plotter()
        self.visuals["obj_vectorfield"].show_grid()

        # object from visualizer class
        self.visuals["obj_barplot"] = service_visualizer()
        self.visuals["obj_barplot"].init_plotter()
        self.visuals["obj_barplot"].show_grid()


    """
    Get new reward for probability distribution. Idea is the probability distribution over the map is changing
    over time due to an intervention. TODO: Name of the function is inadequate
    """
    def get_environmental_information(self, input_file, prob_reward):

        # object from environment class
        obj_map = map_loader()
        #get the coordinates of the map
        self.coordinates = obj_map.preprocessing(input_file)
        #causal prob object
        obj_causal=causal_prob()
        #Normal distribution of
        obj_causal.set_mu(prob_reward["mu"])
        obj_causal.set_Sigma(prob_reward["Sigma"])
        # Get the probabilities for the positions
        probs=obj_causal.get_probabilities_position(self.coordinates)
        rewards=[{str(idx): wlt*1000} for idx, wlt in enumerate(probs) if wlt*1000>1]
        return rewards[0]
    """
    Fill the dictionary of MDP with information
    """
    def set_dict_mdp(self, dict_mdp):
        self.dict_mdp=dict_mdp

    """
    Fill the dictionary of Reachability with information
    """
    def set_dict_reach(self, dict_reach):
        self.dict_reach = dict_reach

    """
    Illustration of vectorfield in PyVista
    """
    def add_vectorfield_queue(self, storyline):

        new_queue = util_io.map_for_queue(self.coordinates)
        self.visuals["obj_vectorfield"].add_queue(new_queue)

        self.visuals["obj_vectorfield"].add_queue_delaunay(new_queue)

        new_queue = util_io.vectorfield_for_queue(self.coordinates, self.dict_mdp)
        self.visuals["obj_vectorfield"].add_queue_vectorfield(new_queue)
        self.visuals["obj_vectorfield"].add_queue_topology(new_queue)

        new_queue, optimal_path_list = util_io.optimal_path_for_queue(self.coordinates, self.dict_mdp, storyline)
        self.visuals["obj_vectorfield"].add_queue_optimalpath(new_queue)

        return optimal_path_list

    """
    Illustration of barplot in PyVista
    """
    def add_barplot_queue(self):

        new_queue = util_io.reach_for_queue(self.coordinates, self.dict_reach, self.dict_mdp)
        self.visuals["obj_barplot"].add_queue(new_queue)
        self.visuals["obj_barplot"].add_queue_delaunay(new_queue)



    """
    MDP to compute optimal vectorfield
    """
    def use_mdp_optimal_vectorfield(self, obj_data_handler, input_file, storyline):
        # solver
        new_dict_mdp = self.use_mdp(input_file, obj_data_handler.folder_to_store, storyline)
        self.set_dict_mdp(new_dict_mdp)
        # add vectorfield plot
        optimal_path_list = self.add_vectorfield_queue(storyline)
        self.visuals["obj_vectorfield"].show_plot(obj_data_handler.folder_to_store + "vectorfield.png")

        # write optimal path to tmp.json
        obj_data_handler.update_json_with_dictionary(optimal_path_list)

        # get result trajectories with spline interpolation
        interpolated_points, points=util_io.get_result_trajectories_mdp(optimal_path_list["act_node"], obj_service.coordinates,
                                        obj_data_handler.folder_to_store)
        cum_dist=util_io.get_cumultative_distance(obj_data_handler.folder_to_store, interpolated_points)
        return interpolated_points, cum_dist, points, optimal_path_list

    """
    Reachability Analysis for visualization on PyVista
    """
    def use_reach_on_visual(self, obj_data_handler, input_file, storyline):
        # solver
        new_dict_reach = self.use_reach(input_file, obj_data_handler.folder_to_store, storyline)
        self.set_dict_reach(new_dict_reach)
        self.add_barplot_queue()
        self.visuals["obj_barplot"].show_plot(obj_data_handler.folder_to_store + "barplot.png")




    """
        Structural causal model for velocity computation
    """
    def use_scm_for_velocity(self, x_v_a, obj_visual, interpolated_points, cum_dist, points, with_intervention, obj_data_handler):
        mean_val_list, intervention_list = obj_service.use_scm_on_interpolated_line(x_v_a, obj_data_handler.folder_to_store, interpolated_points,
                                                             cum_dist, with_intervention)
        mean_vals = mean_val_list["mean_val"]
        velocs = [wlt[1] for wlt in mean_vals]
        max_vel=np.max(velocs)
        util_io.plot_traj(intervention_list, obj_visual, interpolated_points, points, obj_data_handler.folder_to_store, mean_val_list, with_intervention)
        x_v_a[1]=max_vel
        return x_v_a


    """
        One algorithmic cycle where trajectories are computed by MDP
    """
    def one_algorithmic_cycle(self, x_v_a, storyline, obj_data_handler):

        interpolated_points, cum_dist, points, optimal_path_list=self.use_mdp_optimal_vectorfield(obj_data_handler, input_file, storyline)
        self.use_reach_on_visual(obj_data_handler, input_file, storyline)
        with_intervention=False
        x_v_a=self.use_scm_for_velocity(x_v_a, obj_visual.figures["interp_traj_no_interv"], interpolated_points, cum_dist, points, with_intervention, obj_data_handler)
        with_intervention = True
        x_v_a=self.use_scm_for_velocity(x_v_a, obj_visual.figures["interp_traj_with_interv"], interpolated_points, cum_dist, points, with_intervention, obj_data_handler)
        storyline["trajectory"]=optimal_path_list
        return x_v_a, storyline
    """
        Reset the visual names (set to None)
    """
    def reset_visuals(self):
        self.visuals["obj_visual"]= None
        self.visuals["obj_vectorfield"]=None
        self.visuals["obj_barplot"] = None
        plt.close('all')
"""
    Some preprocessing to store the data appropriate    
"""
def pre_processing(storyline, prob_reward):
    # object from data handler
    obj_data_handler = service_data()
    obj_data_handler.set_initial_folder(storyline)
    obj_data_handler.set_initial_json()
    # obj_data_handler.update_json_with_dictionary({"abc": "123"})
    input_file = "/home/michael/PycharmProjects/voting_reinforcement_learning/input/environment/storyline.json"
    obj_data_handler.set_input_file(input_file)

    # visualizer objects for plotting results
    obj_service.get_all_visual_objects()

    # environmental information
    rewards=obj_service.get_environmental_information(input_file, prob_reward)
    return obj_data_handler, input_file, rewards



if __name__ == '__main__':

    x_v_a = [0, 1, 1.295, 0]
    obj_visual=visual_handler()
    # object for solver handling
    obj_service = service_handler()
    prob_reward={"mu": np.matrix([[0.], [0.]]), "Sigma": np.matrix([[1., 0.], [0, 1.]])}
    storyline={"name": "000", "start_node": "0", "rewards": None, "trajectory": None}
    # to generate a folder and store every information
    obj_data_handler, input_file, rewards = pre_processing(storyline, prob_reward)
    storyline["rewards"]= {"14": 1000}
    # one algorithmic cycle
    x_v_a, storyline=obj_service.one_algorithmic_cycle(x_v_a, storyline, obj_data_handler)
    #obj_service.reset_visuals()
    storyline = {"name": "001", "start_node": str(storyline["trajectory"]["act_node"][2]), "trajectory": None}
    prob_reward = {"mu": np.matrix([[4.], [3.]]), "Sigma": np.matrix([[1., 0.], [0, 1.]])}
    obj_data_handler, input_file, rewards = pre_processing(storyline, prob_reward)
    storyline["rewards"]= {"20": 1000}
    x_v_a, storyline=obj_service.one_algorithmic_cycle(x_v_a, storyline, obj_data_handler)

    """ 
        Function for pre-processing: initial json-files and environmental information
        """




