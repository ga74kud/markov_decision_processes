import numpy as np
import source.util.data_input_loader as util_io



class service_data(object):
    def __init__(self, **kwargs):
        self.input_file=None
    def get_input_file(self):
        # which environment model provided
        input_file = "/home/michael/ros/vifware_data_puntigam/pcd/map_v1_small_filtered_xyzrgb.pcd"
        input_file = "/home/michael/PycharmProjects/voting_reinforcement_learning/input/environment/reachable_meta_states.json"
        input_file = self.get_meshgrid_points()
        self.set_input_file(input_file)
        return input_file
        # input_file = "/home/michael/PycharmProjects/voting_reinforcement_learning/input/environment/regular_grid.json"
    def set_input_file(self, input_file):
        self.input_file=input_file
    def get_meshgrid_points(self):
        tst=util_io.get_params()
        xgrid = np.linspace(-10, 10, tst["grid"]["xgrid_dim"])
        ygrid = np.linspace(-10, 10, tst["grid"]["ygrid_dim"])
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


