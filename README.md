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
### Example Renderings
<p float="left">
 <img src="https://https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/master/images/000.png" height="200">
 <img src="https://https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/master/images/010.png" height="200">
 <img src="https://https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/master/images/020.png" height="200">
</p>
<p float="left">
 <img src="https://https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/master/images_waypoints/000.png" height="200">
 <img src="https://https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/master/images_waypoints/010.png" height="200">
 <img src="https://https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/master/images_waypoints/020.png" height="200">
</p>
* Composite multiple frames to create a trajectory visualization (saves to `result.png`)
```
python overlay_traj.py
```
### Example Overlays
<p float="left">
 <img src="https://https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/master/result.png" height="200">
 <img src="https://https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/master/result_waypoints.png" height="200">
</p>
