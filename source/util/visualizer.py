import pyvista as pv

class service_visualizer(object):
    def __init__(self, **kwargs):
        self.p=None
    def init_plotter(self):
        self.p = pv.Plotter()
    def add_meshes_from_queue(self, queue_to_plot):
        for wlt in range(0, len(queue_to_plot)):
            self.p.add_mesh(queue_to_plot[wlt]["to_plot"], opacity=queue_to_plot[wlt]["opacity"])
    def show_grid(self):
        self.p.show_grid()
    def show_plot(self):
        self.p.show(screenshot='city3.png')
