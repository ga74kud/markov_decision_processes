import matplotlib.pyplot as plt


class visual_handler(object):
    def __init__(self, **kwargs):
        self.figures ={"interp_traj_no_interv": plt.figure(figsize=(7, 7)),
                       "interp_traj_with_interv": plt.figure(figsize=(7, 7))}