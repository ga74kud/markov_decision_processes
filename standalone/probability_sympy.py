import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
def mahalabonis_dist(x, mu, Sigma):
    return -0.5*np.transpose(x-mu)*np.linalg.inv(Sigma)*(x-mu)
def multivariate_gaussian_distribution(x, mu, Sigma):
    factor_A=1/np.sqrt((2*np.pi)**2*np.linalg.det(Sigma))
    factor_B=np.exp(mahalabonis_dist(x, mu, Sigma))
    erg=factor_A*factor_B
    return erg[0]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x=np.matrix([[0.], [1.]])
mu=np.matrix([[0.], [1.]])
Sigma=np.matrix([[1., -0.5], [-0.5, 1.5]])
N = 60
X = np.linspace(-3, 3, N)
Y = np.linspace(-3, 4, N)
X, Y = np.meshgrid(X, Y)
X=np.ravel(X)
Y=np.ravel(Y)
Z=np.zeros((len(X)))
for idx, wlt in enumerate(X):
    x = np.matrix([[X[idx]], [Y[idx]]])
    Z[idx]=multivariate_gaussian_distribution(x, mu, Sigma)
    ax.scatter(X[idx], Y[idx], Z[idx], cmap=cm.viridis)



ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('p(x,y)')
plt.show()


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z)

