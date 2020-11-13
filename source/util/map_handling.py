import igraph as ig
import sympy as sp
import json
import numpy as np
import pandas as pd
from sympy.stats import *
from sympy.utilities.lambdify import *
from scipy.spatial import distance


class service_map_handling(object):
    def __init__(self, **kwargs):
        None
    def show_prob_example(self):
        self.load_map()
    def reference_points(self):
        f = open('../../input/environment/simple_environment.json', "r")
        data = json.loads(f.read())
        return data

    def preprocess_data(self, arr):
        if(len(arr[1])==1):
            dub=arr[1][0]
            return pd.DataFrame({'c': arr[0], 'px': dub[0], 'py': dub[1]}, index=[0])
        else:
            val=self.spline_of_points(arr[1], 4, 30)
            tap=[arr[0] for i in range(0, len(val))]
            btc=pd.concat([pd.DataFrame({'c': tap, 'px': i[0], 'py': i[1]}) for i in val])
            return btc

    def load_map(self):
        reference=self.reference_points()
        x_grid=np.linspace(0, 5, 20)
        y_grid=np.linspace(0, 5, 20)
        X,Y=np.meshgrid(x_grid,y_grid)
        P=[[[np.ravel(X)[i], np.ravel(Y)[i]]] for i in range(0, len(np.ravel(X)))]
    def spline_of_points(self, data, spline_degree, amount_points):
        DataPointsDomain = np.linspace(0, 1, len(data))
        DataPointsRangeX = [i[0] for i in data]
        DataPointsRangeY = [i[1] for i in data]
        x, y = sp.symbols('x y')
        f = [sp.interpolating_spline(spline_degree, x, DataPointsDomain, DataPointsRangeX),
             sp.interpolating_spline(spline_degree, x, DataPointsDomain, DataPointsRangeY)]
        val=[[f[0].subs({x:i}), f[1].subs({x:i})] for i in np.linspace(0, 1, amount_points)]
        return val


if __name__ == '__main__':
    obj=service_map_handling()
