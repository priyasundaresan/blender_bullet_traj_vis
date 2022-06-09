import argparse
import os
import numpy as np
import pybullet
import pybullet_data
import pybullet_utils.bullet_client as bclient
from utils.bullet_manipulator import BulletManipulator
from utils.camera_utils import MultiCamera
from utils.pybullet_recorder import PyBulletRecorder
from spatialmath import SE3
import matplotlib.pyplot as plt
#import roboticstoolbox as rtb

#def create_test_traj():
#    robot = rtb.models.DH.Panda()
#    robot.qz = np.load('initial_joint_pos.npy')
#    T = SE3(0.8, 0.2, 0.1) * SE3.OA([0, 1, 0], [0, 0, -1]) # random pose
#    sol = robot.ikine_LM(T) 
#    q_pickup = sol.q
#    qt = rtb.jtraj(robot.qz, q_pickup, 25)
#    np.save('traj.npy', qt.q)
#    return qt.q

def get_args(parent=None):
    parser = argparse.ArgumentParser(description='Main', add_help=False)
    parser.add_argument('--joint_angles_file', type=str, help='Path to file with N x 7 joint angle trajectory.')
    args = parser.parse_args()
    return args


def main(args):
    #traj_data = create_test_traj()
    traj_data = np.load(os.path.expanduser(args.joint_angles_file))
    print('Loaded traj_data', traj_data.shape)
    assert(traj_data.shape[-1] == 7)  # 7DoF joint poses
    #
    # Init Pybullet sim.
    #
    sim = bclient.BulletClient(connection_mode=pybullet.GUI)
    pybullet.configureDebugVisualizer(pybullet.COV_ENABLE_GUI, False)
    pybullet.configureDebugVisualizer(
        pybullet.COV_ENABLE_RGB_BUFFER_PREVIEW, True)
    pybullet.configureDebugVisualizer(
        pybullet.COV_ENABLE_DEPTH_BUFFER_PREVIEW, True)
    pybullet.configureDebugVisualizer(
        pybullet.COV_ENABLE_SEGMENTATION_MARK_PREVIEW, True)
    cam_args = {
        'cameraDistance': 2.0, 'cameraYaw': 0, 'cameraPitch': -30,
        'cameraTargetPosition': np.array([0, 0, 0])
    }
    sim.resetDebugVisualizerCamera(**cam_args)
    sim.setGravity(0, 0, -9.8)
    sim.setTimeStep(1.0/500.0)

    # Load the robot URDF.
    #
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    robot_path = os.path.join(curr_dir, 'data', 'franka_panda', 'panda.urdf')
    print('Loading robot from', robot_path)
    robot = BulletManipulator(
        sim, robot_path, control_mode='velocity',
        ee_joint_name='gripper_base_joint',
        ee_link_name='end_effector_link',
        base_pos=[0,0,0],
        base_quat=pybullet.getQuaternionFromEuler([0, 0, 0]),
        global_scaling=1.0,
        use_fixed_base=True,
        debug=True)

    sim.setAdditionalSearchPath(pybullet_data.getDataPath())
    floor_id = sim.loadURDF('plane.urdf')
    pybullet.configureDebugVisualizer(pybullet.COV_ENABLE_RENDERING, 1)
    view_matrix, proj_matrix = MultiCamera.get_cam_vals(
        cam_rolls=[0], cam_yaws=[cam_args['cameraYaw']],
        cam_pitches=[cam_args['cameraPitch']],
        cam_dist=cam_args['cameraDistance'],
        cam_target=cam_args['cameraTargetPosition'],
        proj_matrix=None,  # get_cam_vals will compute proj_matrix
        fov=90, aspect_ratio=1.0)[0][:2]
    #
    recorder = PyBulletRecorder()
    #
    recorder.register_object(robot.info.robot_id, robot_path)
    print(traj_data.shape[0])

    for step in range(traj_data.shape[0]):
        qpos = traj_data[step]
        robot.reset_to_qpos(qpos)
        sim.stepSimulation()
        MultiCamera.render(
            sim, cam_rolls=[0], cam_yaws=[cam_args['cameraYaw']],
            cam_pitches=[cam_args['cameraPitch']],
            cam_dist=cam_args['cameraDistance'],
            cam_target=cam_args['cameraTargetPosition'],
            proj_matrix=proj_matrix, fov=90, width=300,
            return_seg=True, debug=True)
        recorder.add_keyframe()

    fnm = os.path.expanduser('recorder.pkl')
    recorder.save(fnm)
    print('PyBullet Recorder saved', fnm)

if __name__ == '__main__':
    main(get_args())
