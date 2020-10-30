import pyvista as pv
from pyntcloud import PyntCloud
import numpy as np
import scipy as sp
import _pickle as cPickle
from array import array


def preprocessing():
    input_file="/home/michael/ros/vifware_data_puntigam/pcd/puntigam_v1.pcd"
    cloud = PyntCloud.from_file(input_file)
    converted_triangle_mesh = cloud.to_instance("pyvista", mesh=True)
    abc=np.array(converted_triangle_mesh.points)
    bd=sp.spatial.distance.cdist(abc, [[35, 50, 0]])<40
    compressed_data=[abc[i] for i in range(0, len(abc)) if bd[i]==True]
    newSelObject=pv.PolyData(compressed_data)
    pv.save_meshio("new.ply", newSelObject)
    output_file = open('file.bin', 'wb')
    float_array = array('d', np.random.rand(3))
    float_array.tofile(output_file)
    output_file.close()
    data_segmentation = {"point": np.array(compressed_data), "label_to_names": None}

    dict = {"data": compressed_data, "label": np.ones((np.size(compressed_data, 0), 1)), "scores": None}
    write_pickle(dict, 'important')
def write_pickle(data, file_name):
    file = open(file_name, 'wb')
    cPickle.dump(data, file)
    file.close()


def show_semantic_dataset():
    ref=classify_to_meta()
    show_pyvista(ref)

def classify_to_meta():
    saved_data=open_preprocessed_data()
    data = saved_data["data"]
    semantic_label = saved_data["label"]
    npdata=np.array([(data[i][0], data[i][1], data[i][2]) for i in range(0, len(data))])
    ref=np.array([(npdata[i,:], semantic_label[i]) for i in range(0, len(npdata)) if npdata[i,2]>1.0 and npdata[i,2]<14])
    #D=sp.spatial.distance.cdist(ref, ref)
    #scores = saved_data["scores"]
    return ref
def open_preprocessed_data():
    file = open('important', 'rb')
    saved_data = cPickle.load(file)
    file.close()
    return saved_data

def show_pyvista(ref):
    data=ref[:,0]
    semantic_label=ref[:,1]
    p = pv.Plotter()
    single_classes = np.unique(semantic_label)
    #test=reducedMesh.compute_normals(inplace=True)  # this activates the normals as well

    for wlt in range(0, len(single_classes)):
        sel_idx=np.where(semantic_label==single_classes[wlt])
        new_dat=np.array([(data[i][0], data[i][1], data[i][2]) for i in sel_idx[0]])
        reducedMesh = pv.PolyData(new_dat)
        reducedMesh["elevation"] = new_dat[:,2]
        volume = reducedMesh.delaunay_3d()

        # Extract some grade of the volume
        ore = volume.threshold_percent(20)
        reducedMesh_voxel = pv.voxelize(ore, density=reducedMesh.length / 200, check_surface=False)
        p.add_mesh(reducedMesh, opacity=0.5, point_size=1,render_points_as_spheres=True)
        p.add_mesh(reducedMesh_voxel, opacity=0.2, color="black")
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
    if(1):
        preprocessing()
    show_semantic_dataset()