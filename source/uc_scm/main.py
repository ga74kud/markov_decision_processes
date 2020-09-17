from source.uc_scm.problem import *
class visualizer(object):
    def __init__(self, **kwargs):
        self.problem=self.new_problem()

    def new_problem(self):
        obj=problem()
        obj.set_manifold()

        return obj

if __name__ == '__main__':
    obj=visualizer()