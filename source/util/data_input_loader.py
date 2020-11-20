import json
import numpy as np
from matplotlib import cm
import cairo
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
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

def delaunay_map_for_queue(map):
    queue_list = []
    cloud = pv.PolyData(points)
    for idx, wlt in enumerate(map):
        queue_list.append({"actor_name": "map" + str(idx), "to_plot": wlt,
                           "opacity": .5, "point_size": 10, "render_points_as_spheres": True, "color": "red"})
    return queue_list

def get_direction(act_idx, act_coord, map, mpd_dict):
    act_node=mpd_dict["S"][act_idx]
    act_multi_pi=mpd_dict["multi_pi"][act_node]
    act_neighbours=[wlt["neighbour"] for wlt in act_multi_pi]
    act_difference = [wlt["difference"] for wlt in act_multi_pi]
    all_directions=[tuple(map[int(wlt),:]-act_coord) for wlt in act_neighbours]
    a=np.max(act_difference)
    scale_vec=act_difference/a
    return all_directions, act_difference, scale_vec


def vectorfield_for_queue(map, mpd_dict):
    queue_list = []
    for idx, wlt in enumerate(map):
        all_directions, act_difference, scale_vec=get_direction(idx, wlt, map, mpd_dict)
        for idx, qrt in enumerate(all_directions):
            queue_list.append({"actor_name": "map" + str(idx), "start": wlt, "direction": qrt,
                           "opacity": .5, "point_size": 10, "render_points_as_spheres": True, "color": "red",
                               "scale": scale_vec[idx]})
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
    k=param["program"]["simulation"]["amount_sections"]
    chunklist = chunks(optimal_mdp[1:-1], k)
    act_traj=list()
    act_traj.append((coordinates[optimal_mdp[0], 0], coordinates[optimal_mdp[0], 1]))
    for wlt in chunklist:
        x = np.mean(coordinates[wlt, 0])
        y = np.mean(coordinates[wlt, 1])
        act_traj.append((x,y))
    act_traj.append((coordinates[optimal_mdp[-1], 0], coordinates[optimal_mdp[-1], 1]))
    plot_traj(act_traj)
def plot_traj(act_traj):
    x = [wlt[0] for wlt in act_traj]
    y = [wlt[1] for wlt in act_traj]
    points=np.vstack((x,y)).T
    # Linear length along the line:
    distance = np.cumsum(np.sqrt(np.sum(np.diff(points, axis=0) ** 2, axis=1)))
    distance = np.insert(distance, 0, 0) / distance[-1]

    # Interpolation for different methods:
    interpolations_methods = ['slinear', 'quadratic', 'cubic']
    alpha = np.linspace(0, 1, 75)

    interpolated_points = {}
    for method in interpolations_methods:
        interpolator = interp1d(distance, points, kind=method, axis=0)
        interpolated_points[method] = interpolator(alpha)
    # Graph:
    plt.figure(figsize=(7, 7))
    for method_name, curve in interpolated_points.items():
        plt.plot(*curve.T, '-', label=method_name)

    plt.plot(*points.T, 'ok', label='original points')
    plt.axis('equal')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()