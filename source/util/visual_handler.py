import matplotlib.pyplot as plt


class visual_handler(object):
    def __init__(self, **kwargs):
        self.figures ={"interp_traj": plt.figure(figsize=(7, 7))}