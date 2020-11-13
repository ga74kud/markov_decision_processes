from source.usecases.uc_pomdp.uc_pomdp_main import *
from source.util.map_loader import *
from source.util.visualizer import *
import source.util.data_input_loader as util_io
from collections import OrderedDict

class service_handler(object):
    def __init__(self, **kwargs):
        None
    def get_kmeans_center_json(self):
        ROOT_DIR = "/home/michael/PycharmProjects/voting_reinforcement_learning/"
        ENVIRONMENT_DIR = ROOT_DIR + "input/environment/"
        FILE_DIR = ENVIRONMENT_DIR + "/a_puntigam_tram_station.json"
        return FILE_DIR
    def use_all_solvers(self, input_file):
        optimal_path_mdp=self.use_mdp(input_file)
        return optimal_path_mdp
    def use_cognitive_mdp(self):
        problem_type = {'type': 'cognitive_mdp', 'rewards_body': {'24': 10}, 'rewards_cortex': {'52': 10}}
        self.service_CognitiveMDP(problem_type)
    def use_scm(self):
        problem_type = {'type': 'scm'}
        self.service_scmMDP(problem_type)
    def use_mdp(self, input_file):
        problem={'type': 'pomdp', 'rewards': {'24': 1000}}
        obj_pomdp=service_POMDP()
        obj_pomdp.set_problem_type(problem)
        obj_pomdp.new_problem(input_file)
        ideal_path=obj_pomdp.start_mdp()

        return ideal_path

if __name__ == '__main__':
    # which environment model provided
    input_file = "/home/michael/ros/vifware_data_puntigam/pcd/map_v1_small_filtered_xyzrgb.pcd"
    input_file = "/home/michael/PycharmProjects/voting_reinforcement_learning/input/environment/reachable_meta_states.json"

    # object from visualizer class
    obj_visual = service_visualizer()
    obj_visual.init_plotter()
    obj_visual.show_grid()

    cmap=np.array(plt.get_cmap("plasma").colors)

    # object from environment class
    obj_map=map_loader()

    compressed_data=obj_map.preprocessing(input_file)

    # kmeans for large data
        #ref, daski=obj_map.classify_to_meta()
        #obj_map.save_semantic_kmeans(daski)

    # object for solver handling
    obj_service=service_handler()
    optimal_mdp=obj_service.use_all_solvers(input_file)


    # add map to queue
    new_queue = util_io.map_for_queue(compressed_data)
    obj_visual.add_queue(new_queue)


    new_queue=util_io.trajectory_for_queue(compressed_data, optimal_mdp)
    obj_visual.add_queue(new_queue)
    #new_queue = util_io.reach_for_queue(compressed_data, reach_mdp)
    #all_queue_to_plot.append(new_queue)




    obj_visual.show_plot()

