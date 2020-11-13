import json
import numpy as np
def get_from_json(input_file):
    f = open(input_file, "r")
    data = json.loads(f.read())
    return data
def read_json_dictionary(input_dictionary):
    return np.array([i for i in input_dictionary.values()])

def map_for_queue(map):
    queue_list = []
    for idx, wlt in enumerate(map):
        queue_list.append({"actor_name": "map"+str(idx), "to_plot": wlt,
                           "opacity": .6, "point_size": 6, "render_points_as_spheres": True, "color": "red"})
    return queue_list

def trajectory_for_queue(map, trajectory):
    queue_list=[]
    for wlt in range(0, len(trajectory)):
        act_idx=trajectory[wlt]
        new_point=map[act_idx, :]
        queue_list.append({"actor_name": "mdp_traj"+str(wlt), "to_plot": new_point, "opacity": 1, "point_size": 12, "render_points_as_spheres": True, "color": "blue"})
    return queue_list