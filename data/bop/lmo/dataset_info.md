# BOP DATASET: Linemod-Occluded [2]


## Dataset parameters

* Objects: 15
* Object models: Mesh models with surface color and normals.
* Training images: 19695 rendered images (1313 per object)
* Test images: 18273
* Distribution of the ground truth poses in test images:
    * Range of object distances: 346 - 1500 mm (only 3 instances below 400 mm)
    * Azimuth range: 0 - 360 deg
    * Elevation range: -14 - 89 deg (only a few instances below 0 deg)


## Training images

The training images were obtained by rendering the object models from a
densely sampled view sphere with the radius of 400 mm (there are only 3 object
occurrences in the test images closer than 400 mm) and the elevation range of
0 - 90 deg (i.e. views from the upper hemisphere).

Note that in [1] the object models were rendered at multiple distances (using
view spheres of multiple radii).

One can use this script to render more training images:
https://github.com/thodan/sixd_toolkit/blob/master/tools/render_train_imgs.py


## Extra ground truth

Brachmann et al. [2] provided extra ground truth poses for the Benchvise test
sequence, which is scene 2 in the new format. The extra ground truth is included
in test/02/gt.yml together with the ground truth poses for Benchvise.


## Dataset format

General information about the dataset format can be found in:
https://github.com/thodan/bop_toolkit/blob/master/docs/bop_datasets_format.md


## References

[1] Hinterstoisser et al., "Model based training, detection and pose estimation
    of texture-less 3d objects in heavily cluttered scenes", ACCV 2012,
    web: http://campar.in.tum.de/Main/StefanHinterstoisser

[2] Brachmann et al., "Learning 6d object pose estimation using 3d object
    coordinates", ECCV 2014,
    web: http://cvlab-dresden.de/iccv2015-occlusion-challenge
