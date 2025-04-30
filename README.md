# Blender / PyBullet Trajectory Visualization

This repository provides tools for visualizing and rendering robot trajectories using PyBullet and Blender 4.3.2.

## Installation

### 1. Create a Python environment with Mamba

Install [Mamba](https://github.com/mamba-org/mamba) if you have not already. Then create and activate the environment:

```bash
mamba create -n blender python=3.10 -y
mamba activate blender

# Install dependencies
mamba install -c conda-forge pybullet pysimplegui urdfpy transforms3d opencv -y


```

### 2. Install Blender 4.3.2 on macOS

1. Download Blender 4.3.2 for your system:

   - [Apple Silicon (M1/M2/M3)](https://download.blender.org/release/Blender4.3/blender-4.3.2-macos-arm64.dmg)
   - [Intel Macs](https://download.blender.org/release/Blender4.3/blender-4.3.2-macos-x64.dmg)

2. Open the `.dmg` file and drag **Blender** into your `/Applications` folder.

3. Add an alias to your shell config so `blender` can be called from the terminal. Add the following line to your `~/.zshrc` (if using zsh) or `~/.bashrc` (if using bash):

   ```bash
   alias blender="/Applications/Blender.app/Contents/MacOS/Blender"
   ```

4. Reload your shell:

   ```bash
   source ~/.zshrc   # or source ~/.bashrc
   ```

5. Test that the alias works:

   ```bash
   blender --version
   ```

## Usage

### 1. Replay a Trajectory in PyBullet

Provide an input trajectory `traj.npy` of shape `N x 7` (7 joint angles) and play it back using a Panda URDF in PyBullet:

```bash
python pybullet_replay.py --joint_angles_file traj.npy
```

### 2. Render a Trajectory with Blender

Render images of the trajectory into a directory called `images`. This can be slow on CPU, so consider subsampling your trajectory to around 20–30 poses. (TODO: add support for CUDA rendering)

```bash
# Note: See line 272 in render.py to switch between visualization modes (URDF, spheres, axes)
blender -b -P render.py
```

You can modify `render.py` to change the camera pose, lighting, object colors, and rendering settings.

### Example Renderings

<p float="left">
 <img src="https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/main/images_traj/000.png" height="200">
 <img src="https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/main/images_traj/015.png" height="200">
 <img src="https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/main/images_traj/020.png" height="200">
</p>

### 3. Composite Frames into a Single Visualization

This combines multiple frames into a single composite visualization and saves it as `result.png`:

```bash
python overlay_traj.py
```

### Example Overlays

<p float="left">
 <img src="https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/main/result.png" height="250">
 <img src="https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/main/result_waypoints.png" height="250">
</p>

### 4. Generate GIFs

You can use [ezgif.com](https://ezgif.com/maker) to upload images or frames and create animated GIFs.

### Example GIFs

<p float="left">
 <img src="https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/main/gifs/traj.gif" height="250">
 <img src="https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/main/gifs/traj_poses.gif" height="250">
 <img src="https://github.com/priyasundaresan/blender_bullet_traj_vis/blob/main/gifs/traj_waypoints.gif" height="250">
</p>


