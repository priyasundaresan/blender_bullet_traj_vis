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
# Note, see the settings at line 249 for different modes of visualizing
blender -b -P render.py 
```

### Example Renderings
<p float="left">
 <img src="https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/main/images_traj/000.png" height="200">
 <img src="https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/main/images_traj/015.png" height="200">
 <img src="https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/main/images_traj/020.png" height="200">
</p>

* Composite multiple frames to create a trajectory visualization (saves to `result.png`)
```
python overlay_traj.py
```
### Example Overlays
<p float="left">
 <img src="https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/main/result.png" height="250">
 <img src="https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/main/result_waypoints.png" height="250">
</p>
* You can use tools like https://ezgif.com/maker to upload images and create gifs:
<p float="left">
 <img src="https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/main/gifs/traj.gif" height="250">
 <img src="https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/main/gifs/traj_poses.gif" height="250">
 <img src="https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/main/gifs/traj_waypoints.gif" height="250">
</p>
