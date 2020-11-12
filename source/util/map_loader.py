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
import json
import os
import sys


class map_loader(object):
    def __init__(self, **kwargs):
        None
    def preprocessing(self, input_file):
        #input_file="/home/michael/ros/vifware_data_puntigam/pcd/puntigam_v1.pcd"
        cloud = PyntCloud.from_file(input_file)
        converted_triangle_mesh = cloud.to_instance("pyvista", mesh=True)
        abc=np.array(converted_triangle_mesh.points)
        dataset = pd.DataFrame({'x': abc[:, 0], 'y': abc[:, 1], 'z': abc[:, 2]})
        #bd=sp.spatial.distance.cdist(abc, [[35, 50, 0]])<20

        #compressed_data=[abc[i] for i in range(0, len(abc)) if bd[i]==True]
        compressed_data=abc
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
        self.write_pickle(dict, 'important')
    def write_pickle(self, data, file_name):
        file = open(file_name, 'wb')
        cPickle.dump(data, file)
        file.close()


    def load_semantic_dataset(self):
        ref, km=self.classify_to_meta()
        return km

    def save_semantic_kmeans(self, km):
        ROOT_DIR = "/home/michael/PycharmProjects/voting_reinforcement_learning/"
        ENVIRONMENT_DIR = ROOT_DIR + "input/environment/"
        FILE_DIR=ENVIRONMENT_DIR+"/a_puntigam_tram_station.json"
        abc=list(km[0].cluster_centers_)
        d=dict()
        for a,b in enumerate(abc):
            d['%03d' % a]=b.tolist()
        data_input={"points": d}
        with open(FILE_DIR, 'w') as f:
            json.dump(data_input, f)

    def classify_to_meta(self):
        saved_data=self.open_preprocessed_data()
        data = saved_data["data"]
        semantic_label = saved_data["label"]
        km = saved_data["kmeans"]
        dask_data=saved_data["dask_data"]
        npdata=np.array([(data[i][0], data[i][1], data[i][2]) for i in range(0, len(data))])
        ref=np.array([(npdata[i,:], semantic_label[i]) for i in range(0, len(npdata)) if npdata[i,2]>-1000.0 and npdata[i,2]<1400])
        daski=(km, dask_data)
        return ref, daski
    def open_preprocessed_data(self):
        file = open('/home/michael/PycharmProjects/voting_reinforcement_learning/tmp/important', 'rb')
        saved_data = cPickle.load(file)
        file.close()
        return saved_data
    def find_data_by_idx(self, a, b, idx):
        da.where(a==b[idx])
    def pointcloud_with_kmeans(self, ref, dask_input, optimal_mdp):
        to_mesh= {"km_center": [], "point_cloud_kmeans": []}
        km=dask_input[0]
        data=dask_input[1].compute()
        semantic_label = km.labels_
        single_classes=np.unique(semantic_label.compute())
        #self.p.add_mesh(km.cluster_centers_, opacity=1, point_size=12, render_points_as_spheres=True, color="red")

        for wlt in range(0, 100):

            sel_idx=da.where(semantic_label==wlt)[0].compute()
            new_dat=np.array([(data[i][0], data[i][1], data[i][2]) for i in sel_idx])
            reducedMesh = pv.PolyData(new_dat)
            if(wlt in optimal_mdp):
                highlight_flag=True
            else:
                highlight_flag = False

            to_mesh["km_center"].append({"actor_name": str(wlt), "to_plot": km.cluster_centers_[wlt],
                                         "opacity": 1, "point_size": 12, "render_points_as_spheres": True,
                                         "color": "red",
                                         "highlighted": highlight_flag})
            to_mesh["point_cloud_kmeans"].append({"actor_name": str(wlt), "to_plot": reducedMesh,
                                                  "opacity": 0.05, "color": np.random.randn(3), "highlighted": highlight_flag})
            #self.p.add_mesh(reducedMesh, opacity=0.05, point_size=3,render_points_as_spheres=True, color=np.random.randn(3))
        #self.p.show_grid()
        return to_mesh

    def show_single(self):
        input_file = "haltestelle.ply"
        cloud = PyntCloud.from_file(input_file)
        converted_triangle_mesh = cloud.to_instance("pyvista", mesh=True)
        #p = pv.Plotter()
        #p.add_mesh(converted_triangle_mesh, show_edges=True, color=np.random.rand(3), opacity=0.5)
        #p.show_grid()
        #p.show(screenshot='red.png')

if __name__ == '__main__':
    obj=map_loader()
    input_file="/home/michael/ros/vifware_data_puntigam/pcd/map_v1_small_filtered_xyzrgb.pcd"
    if(1):
        obj.preprocessing(input_file)
    #obj.show_semantic_dataset()