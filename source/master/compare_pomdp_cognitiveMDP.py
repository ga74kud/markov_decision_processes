from source.util.map_handling import *
from source.usecases.uc_pomdp.uc_pomdp_main import *
from source.util.map_loader import *
from source.util.visualizer import *

class service_handler(object):
    def __init__(self, **kwargs):
        self.json_paths={"kmeans_center": self.get_kmeans_center_json()}
    def get_kmeans_center_json(self):
        ROOT_DIR = "/home/michael/PycharmProjects/voting_reinforcement_learning/"
        ENVIRONMENT_DIR = ROOT_DIR + "input/environment/"
        FILE_DIR = ENVIRONMENT_DIR + "/a_puntigam_tram_station.json"
        return FILE_DIR
    def use_all_solvers(self):
        optimal_path_mdp=self.use_mdp()
        return optimal_path_mdp
    def use_cognitive_mdp(self):
        None
        # problem_type = {'type': 'cognitive_mdp', 'rewards_body': {'24': 10}, 'rewards_cortex': {'52': 10}}
        # service_CognitiveMDP(problem_type)
    def use_scm(self):
        None
        # problem_type = {'type': 'scm'}
        # service_scmMDP(problem_type)
    def use_mdp(self):
        problem={'type': 'pomdp', 'rewards': {'24': 10}}
        obj_pomdp=service_POMDP()
        obj_pomdp.set_problem_type(problem)
        obj_pomdp.new_problem(self.json_paths["kmeans_center"])
        ideal_path=obj_pomdp.start_mdp()

        return ideal_path

if __name__ == '__main__':
    obj_visual=service_visualizer()
    obj_visual.init_plotter()
    obj_visual.show_grid()

    input_file="/home/michael/ros/vifware_data_puntigam/pcd/map_v1_small_filtered_xyzrgb.pcd"
    obj_map=map_loader()
    if(0):
        obj_map.preprocessing(input_file)
    ref, daski=obj_map.classify_to_meta()
    obj_map.save_semantic_kmeans(daski)
    obj_service=service_handler()
    optimal_mdp=obj_service.use_all_solvers()
    queue_to_plot=obj_map.pointcloud_with_kmeans(ref, daski, optimal_mdp)

    obj_visual.add_meshes_from_queue(queue_to_plot)
    obj_visual.show_plot()

