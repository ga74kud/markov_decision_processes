import pyvista as pv

class service_visualizer(object):
    def __init__(self, **kwargs):
        self.p=None
    def init_plotter(self):
        self.p = pv.Plotter()
    def add_meshes_from_queue(self, queue_to_plot):
        self.add_queue(queue_to_plot["km_center"])
        self.add_queue(queue_to_plot["point_cloud_kmeans"])
    def add_queue(self, queue):
        for wlt in range(0, len(queue)):
            self.p.add_mesh(queue[wlt]["to_plot"], opacity=queue[wlt]["opacity"])
    def show_grid(self):
        self.p.show_grid()
    def show_plot(self):
        self.p.show(screenshot='city3.png')
