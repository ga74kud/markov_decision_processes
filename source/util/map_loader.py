import pyvista as pv
from pyntcloud import PyntCloud
import numpy as np
import scipy as sp
import _pickle as cPickle
from array import array
import pandas as pd
import dask.array as da
import dask_ml.cluster as daml
from dask.distributed import Client
import matplotlib.pyplot as plt
def preprocessing():
    input_file="/home/michael/ros/vifware_data_puntigam/pcd/puntigam_v1.pcd"
    cloud = PyntCloud.from_file(input_file)
    converted_triangle_mesh = cloud.to_instance("pyvista", mesh=True)
    abc=np.array(converted_triangle_mesh.points)
    dataset = pd.DataFrame({'x': abc[:, 0], 'y': abc[:, 1], 'z': abc[:, 2]})

    #fig, ax = plt.subplots()
    #ax.scatter(x[::10000, 0], x[::10000, 1], marker='.', c=km.labels_[::10000],
    #           cmap='viridis', alpha=0.25)
    bd=sp.spatial.distance.cdist(abc, [[35, 50, 0]])<20

    compressed_data=[abc[i] for i in range(0, len(abc)) if bd[i]==True]
    x = da.from_array(compressed_data, chunks=(18000, 3))
    km = daml.KMeans(n_clusters=100)
    km.fit(x)
    if(0):
        fig, ax = plt.subplots()
        ax.scatter(x[:, 0], x[:, 1], marker='.', c=km.labels_[:],
               cmap='viridis', alpha=0.1)
    #plt.show()
    newSelObject=pv.PolyData(compressed_data)
    pv.save_meshio("new.ply", newSelObject)
    output_file = open('file.bin', 'wb')
    float_array = array('d', np.random.rand(3))
    float_array.tofile(output_file)
    output_file.close()
    data_segmentation = {"point": np.array(compressed_data), "label_to_names": None}

    dict = {"data": compressed_data, "label": np.ones((np.size(compressed_data, 0), 1)), "scores": None, "dask_data": x, "kmeans": km}
    write_pickle(dict, 'important')
def write_pickle(data, file_name):
    file = open(file_name, 'wb')
    cPickle.dump(data, file)
    file.close()


def show_semantic_dataset():
    ref, km=classify_to_meta()
    show_pyvista(ref, km)

def classify_to_meta():
    saved_data=open_preprocessed_data()
    data = saved_data["data"]
    semantic_label = saved_data["label"]
    km = saved_data["kmeans"]
    dask_data=saved_data["dask_data"]
    npdata=np.array([(data[i][0], data[i][1], data[i][2]) for i in range(0, len(data))])
    ref=np.array([(npdata[i,:], semantic_label[i]) for i in range(0, len(npdata)) if npdata[i,2]>-1000.0 and npdata[i,2]<1400])
    #D=sp.spatial.distance.cdist(ref, ref)
    #scores = saved_data["scores"]
    daski=(km, dask_data)
    return ref, daski
def open_preprocessed_data():
    file = open('/home/michael/PycharmProjects/voting_reinforcement_learning/source/util/important', 'rb')
    saved_data = cPickle.load(file)
    file.close()
    return saved_data
def find_data_by_idx(a, b, idx):
    da.where(a==b[idx])
def show_pyvista(ref, dask_input):
    km=dask_input[0]
    data=dask_input[1].compute()
    p = pv.Plotter()
    semantic_label = km.labels_
    single_classes=np.unique(semantic_label.compute())


    #test=reducedMesh.compute_normals(inplace=True)  # this activates the normals as well
    p.add_mesh(km.cluster_centers_, opacity=1, point_size=12, render_points_as_spheres=True, color="red")
    for wlt in range(0, 100):
        sel_idx=da.where(semantic_label==wlt)[0].compute()
        new_dat=np.array([(data[i][0], data[i][1], data[i][2]) for i in sel_idx])
        reducedMesh = pv.PolyData(new_dat)
        #reducedMesh["elevation"] = new_dat[:,2]
        #volume = reducedMesh.delaunay_3d()
        # Extract some grade of the volume
        #ore = volume.threshold_percent(20)
        #reducedMesh_voxel = pv.voxelize(ore, density=reducedMesh.length / 200, check_surface=False)
        p.add_mesh(reducedMesh, opacity=0.5, point_size=3,render_points_as_spheres=True, color=np.random.randn(3))
        #p.add_mesh(reducedMesh_voxel, opacity=0.2, color="black")
    p.show_grid()
    p.show(screenshot='city2.png')

def show_single():
    input_file = "haltestelle.ply"
    cloud = PyntCloud.from_file(input_file)
    converted_triangle_mesh = cloud.to_instance("pyvista", mesh=True)
    p = pv.Plotter()
    p.add_mesh(converted_triangle_mesh, show_edges=True, color=np.random.rand(3), opacity=0.5)
    p.show_grid()
    p.show(screenshot='red.png')

if __name__ == '__main__':
    if(0):
        preprocessing()
    show_semantic_dataset()