import numpy as np
import source.util.data_input_loader as util_io
from datetime import datetime
import os
import json

class service_data(object):
    def __init__(self, **kwargs):
        self.input_file=None
        self.folder_to_store=None

    def set_initial_json(self):
        data = {"storage_folder": self.folder_to_store}
        with open(self.folder_to_store+"tmp.json", 'w') as f:
            json.dump(data, f)

    def update_json_with_dictionary(self, input_dict):
        with open(self.folder_to_store+"tmp.json", "r+") as file:
            json.dump(input_dict, file)

    def set_initial_folder(self, storyline):
        params=util_io.get_special_paths()
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d_%H/")
        folder_to_store_A=params["ROOT_DIR"]+params["OUTPUT_DIR"]+dt_string
        folder_to_store_B=params["ROOT_DIR"]+params["OUTPUT_DIR"]+dt_string+storyline["name"]+"/"
        for wlt in [folder_to_store_A, folder_to_store_B]:
            path=wlt
            try:
                os.mkdir(path)
            except OSError:
                print("Creation of the directory %s failed" % path)
            else:
                print("Successfully created the directory %s " % path)
        self.folder_to_store=folder_to_store_B

    def get_input_file(self):
        # which environment model provided
        #input_file = "/home/michael/ros/vifware_data_puntigam/pcd/map_v1_small_filtered_xyzrgb.pcd"
        #input_file = "/home/michael/PycharmProjects/voting_reinforcement_learning/input/environment/reachable_meta_states.json"
        t=util_io.get_params()
        if(t["mdp"]["select_grid"]=="regular"):
            input_file = self.get_meshgrid_points()
        elif (t["mdp"]["select_grid"] == "random"):
            input_file = self.get_random_grid_points()
        self.set_input_file(input_file)
        return input_file
        # input_file = "/home/michael/PycharmProjects/voting_reinforcement_learning/input/environment/regular_grid.json"

    def set_input_file(self, input_file):
        self.input_file=input_file


    def get_random_grid_points(self):
        tst = util_io.get_params()
        xgrid = np.linspace(-10, 10, tst["environment"]["regular"]["grid"]["xgrid_dim"])
        ygrid = np.linspace(-10, 10, tst["environment"]["regular"]["grid"]["ygrid_dim"])
        X, Y = np.meshgrid(xgrid, ygrid)
        x = np.ravel(X)
        y = np.ravel(Y)
        x=util_io.perturb_by_random_vector(x, 1.3)
        y=util_io.perturb_by_random_vector(y, 1.2)
        z = .0082*x*x + .007 * y*x + .0043 * x*y + 0.0068 * y*y
        z=z+util_io.perturb_by_random_vector(z, .7)
        dict_pnts = {}
        points = np.transpose(np.vstack((x, y, z))).tolist()
        for idx, act_point in enumerate(points):
            dict_pnts[str(idx)] = act_point
        input_file = "/home/michael/PycharmProjects/voting_reinforcement_learning/input/environment/tesi.json"

        data_to_json = {"type": "point_list", "points": dict_pnts}
        util_io.write_to_json(input_file, data_to_json)
        return input_file
    def get_meshgrid_points(self):
        tst=util_io.get_params()
        xgrid = np.linspace(-10, 10, tst["environment"]["regular"]["grid"]["xgrid_dim"])
        ygrid = np.linspace(-10, 10, tst["environment"]["regular"]["grid"]["ygrid_dim"])
        X, Y=np.meshgrid(xgrid,ygrid)
        x=np.ravel(X)
        y=np.ravel(Y)
        z=0*y
        dict_pnts={}
        points=np.transpose(np.vstack((x, y, z))).tolist()
        for idx, act_point in enumerate(points):
            dict_pnts[str(idx)]=act_point
        input_file = "/home/michael/PycharmProjects/voting_reinforcement_learning/input/environment/tesi.json"

        data_to_json={"type": "point_list", "points": dict_pnts}
        util_io.write_to_json(input_file, data_to_json)
        return input_file


