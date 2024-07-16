# biig-ants 🪲🐜🦗🐞🪰🦗

A silly project we ran as part of the [BIIG](https://www.ucl.ac.uk/lmcb/ucl-biig) Hackathon 2024.

To run, execute the following command from the root folder:
```
blender --python /biig_ants/main.py
```

This is an unfinished project! 🏗️ (the best kind :P)

## What does it do?
The script generates a random landscape object, and defines a particle system of bugs that walk on this terrain towards an emitter.

The next steps would be to define a virtual camera that looks to the particle system top-down. Then we can render the different passes of the scene and export them as OpenEXR files that we can analyse with Python.

The idea is that using Blender's passes we can easily generate synthetic training data for segmentation, optic flow estimation or tracking (but we didn't get that far).

## Data
The script expects a bug mesh called `Eleodes_spec_cleaned.fbx` to located at a `data` directory, two-levels up from this file.  

This mesh can be downloaded from [this link](https://drive.google.com/file/d/1E4XHMiHWTNKg5Kj-i_5Dfha8AeP1qZ9R/view?usp=drive_link)

The data comes from this cool paper:
> Plum, F., & Labonte, D. (2021). scAnt—an open-source platform for the creation of 3D models of arthropods (and other small objects). PeerJ, 9, e11155.

## Contributors
This project was done in collaboration with @K-Meech, @ruaridhg and @WhoIsJack, thanks for all the great contributions!

## Inspo
- This very cool piece of work https://github.com/evo-biomech/replicAnt 
- Some snippets from https://github.com/sfmig/hawk-eyes