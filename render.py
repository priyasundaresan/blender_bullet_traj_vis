import bpy
import numpy as np
import pickle
import os
from os.path import splitext, join, basename
import sys
import sys
from bpy.props import (
    StringProperty,
    CollectionProperty
)

def clear_scene():
    # Clear existing objects in scene
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)
    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)
    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def set_viewport_shading(mode):
    # Make materials visible in viewport
    areas = bpy.context.workspace.screens[0].areas
    for area in areas:
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = mode

def colorize(obj, color=(1,1,1,1)):
    # Add (R,G,B,A) color to obj; TODO: priya fix to allow alpha transparency
    if '%sColor' % obj.name in bpy.data.materials:
        mat = bpy.data.materials['%sColor'%obj.name]
    else:
        mat = bpy.data.materials.new(name="%sColor"%obj.name)
        mat.use_nodes = False
    mat.diffuse_color = color
    mat.specular_intensity = np.random.uniform(0, 0.1)
    mat.roughness = np.random.uniform(0.5, 1)
    if not obj.data.materials:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat
    set_viewport_shading('MATERIAL')

def add_camera():
    # Add a camera to the scene
    bpy.ops.object.camera_add(location=(1.94, -0.77, 0.9), rotation=(np.radians(68), 0.0, np.radians(61)))
    bpy.context.scene.camera = bpy.context.object
    return bpy.context.object
    
def add_light():
    # Add area light
    bpy.ops.object.light_add(type='AREA', align='WORLD', location=(0, -1, 0.37328), scale=(1, 1, 1), rotation=(np.radians(90), 0, 0))
    bpy.context.object.data.energy = 5

def set_render_settings(render_size, engine='CYCLES', generate_masks=True):
    # Configure renderer
    scene = bpy.context.scene

    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.3
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)

    scene.view_layers['View Layer'].cycles.use_denoising = True
    scene.render.film_transparent = True
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.resolution_percentage = 100
    scene.render.engine = engine
    render_width, render_height = render_size
    scene.render.resolution_x = render_width
    scene.render.resolution_y = render_height
    scene.use_nodes = True
    scene.render.image_settings.file_format='PNG' # Transparent background
    #scene.render.image_settings.file_format='JPEG' # Non-transparent background
    scene.view_settings.exposure = 1.6
    scene.cycles.samples = 150 # Quality of render; in general higher is slower!!!
    scene.view_settings.view_transform = 'Raw'
    scene.render.tile_x = 16 # Use 256 if on GPU
    scene.render.tile_y = 16 # Use 256 if on GPU

def render(frame, output_dir):
    scene = bpy.context.scene
    scene.render.filepath = '%s/%03d.png'%(output_dir, frame)
    #scene.render.filepath = '%s/%03d.jpg'%(output_dir, frame)
    bpy.ops.render.render(write_still=True)

def make_traj_vis_obj(vis_object='axes'):
    r,g,b = (255, 169, 27)
    if vis_object == 'axes':
        bpy.ops.import_mesh.stl(filepath='data/blender_assets/xyz_axis.stl', filter_glob="*.stl")
        scale = (0.001,0.001,0.001)
    else:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1)
        scale = (0.01,0.01,0.01)
    obj = bpy.context.object
    obj.scale = scale
    colorize(obj, (r/255,g/255,b/255,1))
    return obj

def keyframe_traj(context, files, directory, mode='urdf'):
    assert(mode == 'urdf' or mode == 'waypoints' or mode == 'waypoints-axes')
    if mode == 'waypoints':
        traj_vis_obj = make_traj_vis_obj(vis_object='sphere')
    elif mode == 'waypoints-axes':
        traj_vis_obj = make_traj_vis_obj(vis_object='axes')
        
    for file in files:
        filepath = join(directory, file)
        print(f'Processing {filepath}')
        with open(filepath, 'rb') as pickle_file:
            data = pickle.load(pickle_file)
            collection_name = splitext(basename(filepath))[0]
            collection = bpy.data.collections.new(collection_name)
            bpy.context.scene.collection.children.link(collection)
            context.view_layer.active_layer_collection = \
                context.view_layer.layer_collection.children[-1]

            for obj_key in data:
                pybullet_obj = data[obj_key]

                # Load mesh of each link
                assert pybullet_obj['type'] == 'mesh'
                extension = pybullet_obj['mesh_path'].split(
                    ".")[-1].lower()
                # Handle different mesh formats
                if 'obj' in extension:
                    bpy.ops.import_scene.obj(
                        filepath=pybullet_obj['mesh_path'],
                        axis_forward='Y', axis_up='Z')
                elif 'dae' in extension:
                    bpy.ops.wm.collada_import(
                        filepath=pybullet_obj['mesh_path'])
                elif 'stl' in extension:
                    bpy.ops.import_mesh.stl(
                        filepath=pybullet_obj['mesh_path'])
                else:
                    print("Unsupported File Format:{}".format(extension))
                    pass

                # Delete lights and camera
                parts = 0
                final_objs = []
                for import_obj in context.selected_objects:
                    bpy.ops.object.select_all(action='DESELECT')
                    import_obj.select_set(True)
                    if 'Camera' in import_obj.name \
                            or 'Light' in import_obj.name\
                            or 'Lamp' in import_obj.name:
                        bpy.ops.object.delete(use_global=True)
                    else:
                        scale = pybullet_obj['mesh_scale']
                        if scale is not None:
                            import_obj.scale.x = scale[0]
                            import_obj.scale.y = scale[1]
                            import_obj.scale.z = scale[2]
                        final_objs.append(import_obj)
                        parts += 1
                bpy.ops.object.select_all(action='DESELECT')
                for obj in final_objs:
                    if obj.type == 'MESH':
                        obj.select_set(True)
                if len(context.selected_objects):
                    context.view_layer.objects.active =\
                        context.selected_objects[0]
                    # join them
                    bpy.ops.object.join()
                blender_obj = context.view_layer.objects.active
                blender_obj.name = obj_key

                # Keyframe motion of imported object
                for frame_count, frame_data in enumerate(
                        pybullet_obj['frames']):
                    percentage_done = frame_count / \
                        len(pybullet_obj['frames'])
                    print(f'\r[{percentage_done*100:.01f}% | {obj_key}]',
                          '#' * int(60*percentage_done), end='')
                    pos = frame_data['position']
                    orn = frame_data['orientation']

                    if (mode == 'waypoints' and frame_count == 0) or (mode == 'urdf'):
                        blender_obj.location.x = pos[0]
                        blender_obj.location.y = pos[1]
                        blender_obj.location.z = pos[2]
                        blender_obj.rotation_mode = 'QUATERNION'
                        blender_obj.rotation_quaternion.x = orn[0]
                        blender_obj.rotation_quaternion.y = orn[1]
                        blender_obj.rotation_quaternion.z = orn[2]
                        blender_obj.rotation_quaternion.w = orn[3]
                        blender_obj.keyframe_insert(data_path="location", frame=frame_count)
                        blender_obj.keyframe_insert(data_path="rotation_quaternion", frame=frame_count)
                    if (mode == 'waypoints' and 'hand' in blender_obj.name):
                        traj_vis_obj.location.x = pos[0]
                        traj_vis_obj.location.y = pos[1]
                        traj_vis_obj.location.z = pos[2]
                        traj_vis_obj.rotation_mode = 'QUATERNION'
                        traj_vis_obj.rotation_quaternion.x = orn[0]
                        traj_vis_obj.rotation_quaternion.y = orn[1]
                        traj_vis_obj.rotation_quaternion.z = orn[2]
                        traj_vis_obj.rotation_quaternion.w = orn[3]
                        traj_vis_obj.keyframe_insert(data_path="location", frame=frame_count)
                        traj_vis_obj.keyframe_insert(data_path="rotation_quaternion", frame=frame_count)
    return frame_count+1

def delete_objs(ob_names):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    for ob_name in ob_names:
        ob = bpy.data.objects[ob_name]
        ob.select_set(True)
    bpy.ops.object.delete()

def make_table():
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    obj = bpy.context.object
    obj.scale = (0.5,0.5,0.5)
    return obj

def make_cube():
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0.3, 0, 0.05))
    obj = bpy.context.object
    obj.scale = (0.1,0.1,0.1)
    return obj

def main():
    render_size = (480, 480) # Set size of render
    set_render_settings(render_size)

    clear_scene()
    camera = add_camera()
    #add_light() 

    # Add objects to the scene if you want
    table = make_table()
    colorize(table, (1,1,1,1))
    cube = make_cube()
    colorize(cube, (1,0,0,1))

    # Keyframe the trajectory, can comment these out for other modes

    #frame_count = keyframe_traj(bpy.context, files=['recorder.pkl'], directory=os.path.abspath(os.getcwd()), mode='waypoints-axes') # Show the traj by keyframing a coordinate axes obj
    #frame_count = keyframe_traj(bpy.context, files=['recorder.pkl'], directory=os.path.abspath(os.getcwd()), mode='waypoints') # Show the traj by a set of points (spheres)
    frame_count = keyframe_traj(bpy.context, files=['recorder.pkl'], directory=os.path.abspath(os.getcwd()), mode='urdf') # Show the traj by putting the robot URDF in each pose of the traj

    # Directory to save images
    output_dir = 'images'
    if not(os.path.exists(output_dir)):
        os.mkdir(output_dir)

    # Render!
    for i in range(frame_count):
        render(i, output_dir)
        bpy.context.scene.frame_set(i)

if __name__ == '__main__':
    main()
