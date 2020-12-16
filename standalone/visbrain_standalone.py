import numpy as np

from visbrain.objects import BrainObj, ColorbarObj, SceneObj, SourceObj
from visbrain.io import download_file, read_stc
KW = dict(title_size=14., zoom=1.2)
# Scene creation
sc = SceneObj(bgcolor='black', size=(1400, 1000))
# Colorbar default arguments. See `visbrain.objects.ColorbarObj`
CBAR_STATE = dict(cbtxtsz=12, txtsz=10., width=.1, cbtxtsh=3.,
                  rect=(-.3, -2., 1., 4.))
# Download the annotation file of the left hemisphere lh.aparc.a2009s.annot
path_to_file1_LH = download_file('lh.aparc.a2009s.annot', astype='example_data')

# Download the annotation file of the left hemisphere lh.aparc.a2009s.annot
path_to_file1_RH = download_file('rh.aparc.a2009s.annot', astype='example_data')
# Define the brain object (now you should know how to do it)
b_obj_parl = BrainObj('inflated', hemisphere='left', translucent=False)
# Print parcellates included in the file
# print(b_obj_parl.get_parcellates(path_to_file1))
# Finally, parcellize the brain and add the brain to the scene

b_obj_parl.parcellize(path_to_file1_LH)
sc.add_to_subplot(b_obj_parl, row=0, col=0, rotate="left",
                  title='Desikan Atlas', **KW)

sc.preview()