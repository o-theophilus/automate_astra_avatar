from sys import path
import os

# import bpy
# script_path = bpy.path.abspath("//") #blender file path
script_path = os.path.dirname(os.path.realpath(__file__))  # python file path
path.append(script_path)

from ops import reset, get_clothes, fix_cloth_pose, bind_items, set_pose
from mdt import transfer_shape_keys, transfer_vertex_groups
from iop import import_costume, get_character, save_files
from dof import delete_occluded_faces

input_path = os.path.abspath(os.path.join(script_path, '..', "input"))
files = os.listdir(input_path)
files = [f for f in files if os.path.splitext(f)[1].lower() == ".fbx"]
files = [os.path.join(input_path, f) for f in files]


for file in files:
    gender = os.path.splitext(file)[0]
    gender = gender.split("#")

    if len(gender) < 2:
        continue
    gender = gender[1].lower()
    if not gender or gender not in ["m", "f"]:
        continue

    reset()
    import_costume(file)
    get_character(f"{gender}.", script_path)
    clothes = get_clothes()
    transfer_vertex_groups(clothes)
    fix_cloth_pose(clothes)
    bind_items(clothes)
    transfer_shape_keys(clothes)
    delete_occluded_faces()
    set_pose()
    save_files(file, script_path)
