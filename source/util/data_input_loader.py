import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import cairo
def get_from_json(input_file):
    f = open(input_file, "r")
    data = json.loads(f.read())
    return data
def read_json_point_list(input_dictionary):
    return np.array([i for i in input_dictionary.values()])

def map_for_queue(map):
    queue_list = []
    for idx, wlt in enumerate(map):
        queue_list.append({"actor_name": "map"+str(idx), "to_plot": wlt,
                           "opacity": .5, "point_size": 10, "render_points_as_spheres": True, "color": "red"})
    return queue_list

def trajectory_for_queue(map, trajectory):
    queue_list=[]
    cmap=get_colormap("cividis")
    col_idx=np.floor(np.linspace(0, np.size(cmap, 0)-1, len(trajectory)))
    ball_size=np.linspace(12, 40, len(trajectory))
    for wlt in range(0, len(trajectory)):
        act_idx=trajectory[wlt]
        new_point=map[act_idx, :]
        crow=np.int(col_idx[wlt])
        queue_list.append({"actor_name": "mdp_traj"+str(wlt), "to_plot": new_point, "opacity": .8,
                           "render_points_as_spheres": True, "point_size": ball_size[wlt], "color": cmap[crow,:]})
    return queue_list

def get_colormap(colmap):
    cmap=plt.get_cmap(colmap).colors
    return np.array(cmap)


def write_to_json(input_file, input_data):
    json_object = json.dumps(input_data)
    with open(input_file, "w") as outfile:
        outfile.write(json_object)

def get_params():
    dirs=get_from_json("../../input/config/special_paths.json")
    FILE_DIR=dirs["ROOT_DIR"]+dirs["PARAMS"]
    return get_from_json(FILE_DIR)

def chunks(input, k):
    n=int(np.floor(len(input)/k))
    test=[np.array(input[i:i+n]) for i in range(0, len(input), n)]
    return test

def get_result_trajectories_mdp(optimal_mdp, coordinates):
    param=get_params()
    k=param["result_traj"]["amount_sections"]
    act_traj=list()
    act_traj.append(optimal_mdp[0])
    chunklist=chunks(optimal_mdp[1:-1], k)
    abc=[int(np.random.choice(wlt, 1)) for wlt in chunklist]
    for x in abc:
        act_traj.append(x)
    act_traj.append(optimal_mdp[-1])
    plot_cairo(act_traj, coordinates)
def plot_cairo(act_traj, coordinates):
    sel_coord=coordinates[act_traj, 0:1]
    test=1