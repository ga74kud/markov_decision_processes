import pyvista as pv

class service_visualizer(object):
    def __init__(self, **kwargs):
        self.p=None
    def init_plotter(self):
        self.p = pv.Plotter(off_screen=True)
    def add_queue(self, queue):
        for wlt in range(0, len(queue)):
            to_plot=queue[wlt]
            if(to_plot.get("type")==None):
                a=pv.PolyData(to_plot["to_plot"])
            elif(to_plot["type"]=="sphere"):
                a=pv.Sphere(radius=0.4, center=to_plot["to_plot"])
            elif (to_plot["type"] == "cone"):
                a = pv.Cone(center=to_plot["to_plot"])
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

    def add_queue_optimalpath(self, queue):
        for wlt in range(0, len(queue)):
            to_plot = queue[wlt]
            a = pv.Arrow(start=to_plot["start"], direction=to_plot["direction"], tip_radius=0.2, shaft_radius=0.1)
            b = 1
            c = to_plot["color"]
            self.p.add_mesh(a, opacity=b, color=c)

    def add_queue_delaunay(self, queue):
        to_plot=[queue[wlt]["to_plot"] for wlt in range(0, len(queue))]
        a=pv.PolyData(to_plot)
        delaunay_plot=a.delaunay_2d()
        self.p.add_mesh(delaunay_plot, opacity=0.5)

    def add_queue_topology(self, queue):
        for wlt in range(0, len(queue)):
            to_plot = queue[wlt]
            a = pv.Line(pointa=to_plot["pointa"], pointb=to_plot["pointb"])
            b = to_plot["opacity"]
            c = "black"
            d = to_plot["point_size"]
            e = to_plot["render_points_as_spheres"]
            self.p.add_mesh(a, opacity=b, color=c, point_size=d, render_points_as_spheres=e)
    def show_grid(self):
        self.p.show_grid()
    def show_plot(self, path):
        self.p.show(screenshot=path)
