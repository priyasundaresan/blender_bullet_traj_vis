# Blender/PyBullet Trajectory Visualizations

[Installation](#install)<br />
[Usage](#usage)<br />

<a name="install"></a>
## Installation
### Install Python dependencies
```
conda env create -f environment.yml
pip install networkx==2.5
```

### Install Blender 2.93
* Download Blender 2.93.4 for your OS from https://www.blender.org/download/lts/2-93/
* Alias `blender` in your `~/.bashrc` (mine looks like the following:)
```
alias blender="/Applications/Blender.app/Contents/MacOS/Blender"
```
* After this, run `source ~/.bashrc`


<a name="usage"></a>
## Usage
* Playback the input trajectory `traj.npy` and save Franka URDF poses
```
python pybullet_replay.py --joint_angles_file traj.npy
```
* Render images of the trajectory into a directory called `images` # Note, this is slow on CPU, so try to subsample your trajectories to length 20-30 poses; (TODO: add support for CUDA rendering)
```
blender -b -P render.py 
```
* Composite multiple frames to create a trajectory visualization (saves to `result.png`)
```
python overlay_traj.py
```
