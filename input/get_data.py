



class service_data(object):
    def __init__(self, **kwargs):
        self.input_file=None
    def get_input_file(self):
        # which environment model provided
        input_file = "/home/michael/ros/vifware_data_puntigam/pcd/map_v1_small_filtered_xyzrgb.pcd"
        input_file = "/home/michael/PycharmProjects/voting_reinforcement_learning/input/environment/reachable_meta_states.json"
        self.set_input_file(input_file)
        return input_file
        # input_file = "/home/michael/PycharmProjects/voting_reinforcement_learning/input/environment/regular_grid.json"
    def set_input_file(self, input_file):
        self.input_file=input_file