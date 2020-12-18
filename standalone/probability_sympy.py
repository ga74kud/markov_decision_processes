import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mlt
import matplotlib.pyplot as plt
from matplotlib import cm

class causal_probabilistic_vector_field(object):
    def __init__(self, **kwargs):
        self.ax=None
    def mahalabonis_dist(self, x, mu, Sigma):
        return -0.5*np.transpose(x-mu)*np.linalg.inv(Sigma)*(x-mu)
    def multivariate_gaussian_distribution(self, x, mu, Sigma):
        factor_A=1/np.sqrt((2*np.pi)**2*np.linalg.det(Sigma))
        factor_B=np.exp(self.mahalabonis_dist(x, mu, Sigma))
        erg=factor_A*factor_B
        return erg[0]
    def visualize_multivariate_gaussian(self, mu, Sigma):
        fig = plt.figure()
        self.ax = fig.add_subplot(projection='3d')
        Z=np.zeros((np.size(self.X, 0), np.size(self.X, 1)))
        for idx_A in range(0, np.size(self.X, 0)):
            for idx_B in range(0, np.size(self.X, 1)):
                x = np.matrix([[self.X[idx_A, idx_B]], [self.Y[idx_A, idx_B]]])
                Z[idx_A, idx_B]=self.multivariate_gaussian_distribution(x, mu, Sigma)
        self.ax.plot_surface(self.X, self.Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('p(x,y)')
    def show(self):
        #plt.ion()
        plt.show()
    def set_fixed_domain(self):
        N = 16
        X = np.linspace(-3, 3, N)
        Y = np.linspace(-3, 4, N)
        self.X, self.Y = np.meshgrid(X, Y)
        self.x_rav = np.ravel(X)
        self.y_rav = np.ravel(Y)
    def plot_arrow(self, mu, w, v):
        Q=self.ax.quiver(mu[0], mu[1], 0, v[0,0], v[0, 1], 0, color="red")

    def plot_eigen_vectors_Sigma(self, mu, Sigma):
        w, v = np.linalg.eigh(Sigma)
        for idx, wlt in enumerate(v):
            self.plot_arrow(mu, w[idx], wlt)



if __name__ == '__main__':
    mlt.use('Qt5Agg')
    mu = np.matrix([[0.], [1.]])
    Sigma = np.matrix([[.3, 0.], [-1., 1.]])
    w,v=np.linalg.eigh(Sigma)
    obj_causal=causal_probabilistic_vector_field()
    obj_causal.set_fixed_domain()
    obj_causal.visualize_multivariate_gaussian(mu, Sigma)
    obj_causal.plot_eigen_vectors_Sigma(mu,Sigma)
    obj_causal.show()

