import pyvista as pv

class service_visualizer(object):
    def __init__(self, **kwargs):
        self.p=None
    def init_plotter(self):
        self.p = pv.Plotter()
    def add_queue(self, queue):
        for wlt in range(0, len(queue)):
            to_plot=queue[wlt]
            a=pv.PolyData(to_plot["to_plot"])
            b=to_plot["opacity"]
            c = to_plot["color"]
            d = to_plot["point_size"]
            e = to_plot["render_points_as_spheres"]
            self.p.add_mesh(a, opacity=b, color=c, point_size=d, render_points_as_spheres=e)
    def add_queue_vectorfield(self, queue):
        for wlt in range(0, len(queue)):
            to_plot=queue[wlt]
            arrow_1 = to_plot["scale"]
            a=pv.Arrow(start=to_plot["start"], direction=to_plot["direction"], scale=arrow_1)
            b=to_plot["opacity"]
            c = to_plot["color"]
            d = to_plot["point_size"]
            e = to_plot["render_points_as_spheres"]
            self.p.add_mesh(a, opacity=b, color=c, point_size=d, render_points_as_spheres=e)
    def show_grid(self):
        self.p.show_grid()
    def show_plot(self):
        self.p.show()
