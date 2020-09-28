from nilearn import datasets

dataset = datasets.fetch_atlas_harvard_oxford('cort-maxprob-thr25-2mm')
atlas_filename = dataset.maps

print('Atlas ROIs are located at: %s' % atlas_filename)

from nilearn import plotting

plotting.plot_roi(atlas_filename, title="Harvard Oxford atlas")
plotting.show()