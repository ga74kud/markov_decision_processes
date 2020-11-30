import json
import numpy as np
import warnings
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

def perturb_by_random_vector(vec, scale_val):
    pertub_vec=np.random.rand(len(vec))*scale_val
    new_vec=vec+pertub_vec
    return new_vec

def delaunay_map_for_queue(map):
    queue_list = []
    for idx, wlt in enumerate(map):
        queue_list.append({"actor_name": "map" + str(idx), "to_plot": wlt,
                           "opacity": .5, "point_size": 10, "render_points_as_spheres": True, "color": "red"})
    return queue_list

def get_direction(act_idx, act_coord, map, mdp_dict):
    FLAG_IS_VALID=False
    act_node=mdp_dict["S"][act_idx]
    act_multi_pi=mdp_dict["multi_pi"][act_node]
    act_neighbours=[wlt["neighbour"] for wlt in act_multi_pi]
    if(len(act_neighbours)==0):
        return 0, 0, 0, 0, FLAG_IS_VALID
    act_difference = [wlt["difference"] for wlt in act_multi_pi]
    all_directions=[tuple(map[int(wlt),:]-act_coord) for wlt in act_neighbours]
    try:
        a=np.max(act_difference)
        scale_vec=act_difference/a
    except:
        warnings.warn(str(act_neighbours)+str(act_difference), Warning)

    neigh_idx=[mdp_dict["S"].index(act_neighbours[idx]) for idx in range(0, len(act_neighbours))]
    end_points=[tuple(map[qrt, :]) for qrt in neigh_idx]
    FLAG_IS_VALID=True
    return all_directions, act_difference, scale_vec, end_points, FLAG_IS_VALID


def get_next_node(act_idx, map, mdp_dict):
    act_node_idx=mdp_dict["S"].index(act_idx)
    start_point=map[act_node_idx, :]
    act_multi_pi=mdp_dict["multi_pi"][act_idx]
    act_neighbours=[wlt["neighbour"] for wlt in act_multi_pi]
    act_difference = [wlt["difference"] for wlt in act_multi_pi]
    max_idx=act_difference.index(max(act_difference))
    neigh_idx=[mdp_dict["S"].index(act_neighbours[idx]) for idx in range(0, len(act_neighbours))]
    all_end_points=[tuple(map[qrt, :]) for qrt in neigh_idx]
    best_end_point=all_end_points[max_idx]
    best_end_idx=neigh_idx[max_idx]
    return start_point, all_end_points, best_end_point, best_end_idx

def vectorfield_for_queue(map, mdp_dict):
    queue_list = []
    for idx, wlt in enumerate(map):
        all_directions, act_difference, scale_vec, end_points, FLAG_IS_VALID=get_direction(idx, wlt, map, mdp_dict)
        if(FLAG_IS_VALID):
            for idx, qrt in enumerate(all_directions):
                queue_list.append({"actor_name": "vecfld_" + str(idx), "start": wlt, "direction": qrt,
                           "opacity": .5, "point_size": 10, "render_points_as_spheres": True, "color": "red",
                               "scale": scale_vec[idx], "pointa": wlt, "pointb": end_points[idx]})
        else:
            continue
    return queue_list

def optimal_path_for_queue(map, mdp_dict):
    params = get_params()
    act_node = mdp_dict['S'][params["mdp"]["simulation"]["start_node"]]
    queue_list = []
    start_point_list=[]
    act_node_list=[]
    for idx in range(0, params["mdp"]["simulation"]["number_cycles_to_reach_target"]):
        start_point, all_end_points, best_end_point, next_node=get_next_node(act_node, map, mdp_dict)
        start_point_list.append(start_point.tolist())
        act_node_list.append(int(act_node))
        act_node=mdp_dict["S"][next_node]
        act_difference=np.array(best_end_point) - start_point
        queue_list.append({"actor_name": "vecfld_" + str(idx), "start": start_point, "direction": act_difference,
                           "opacity": .5, "point_size": 10, "render_points_as_spheres": True, "color": "blue",
                       "scale": 3})

    new_act_node_list=[]
    new_start_point_list=[]
    count=0
    for idx, val in enumerate(act_node_list):
        if(act_node_list[idx]==act_node_list[idx+1]):
            count+=1
        new_act_node_list.append(val)
        new_start_point_list.append(start_point_list[idx])
        if(count>=1):
            break
    optimal_path_list = {"start_point": new_start_point_list, "act_node": new_act_node_list}
    return queue_list, optimal_path_list

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
    dirs=get_special_paths()
    FILE_DIR=dirs["ROOT_DIR"]+dirs["PARAMS"]
    return get_from_json(FILE_DIR)

def get_special_paths():
    return get_from_json("../../input/config/special_paths.json")

def chunks(input, k):
    n=int(np.floor(len(input)/k))
    test=[np.array(input[i:i+n]) for i in range(0, len(input), n)]
    return test

def get_result_trajectories_mdp(optimal_mdp, coordinates):
    param=get_params()
    k=param["mdp"]["simulation"]["amount_sections"]
    chunklist = chunks(optimal_mdp[1:-1], k)
    act_traj=list()
    act_traj.append((coordinates[optimal_mdp[0], 0], coordinates[optimal_mdp[0], 1]))
    for wlt in chunklist:
        x = np.mean(coordinates[wlt, 0])
        y = np.mean(coordinates[wlt, 1])
        act_traj.append((x,y))
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