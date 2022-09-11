import bpy
import os


def import_costume(path):
    if os.path.splitext(path)[1].lower() == ".fbx":
        bpy.ops.import_scene.fbx(filepath=path)
    if os.path.splitext(path)[1].lower() == ".obj":
        bpy.ops.import_scene.obj(filepath=path)


def get_character(gender, script_path):
    script_path = os.path.join(script_path, "base")
    bpy.ops.object.select_all(action='DESELECT')

    with bpy.data.libraries.load(script_path, link=False) as (data_from, data_to):
        data_to.objects = [
            name for name in data_from.objects if name.startswith(gender)]
    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj)
            obj.name = obj.name.split(gender)[1]


def save_files(filename, script_path):
    output_path = os.path.abspath(os.path.join(script_path, '..', "output"))
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    filename = os.path.split(filename)[1]
    fbx = os.path.join(output_path, filename)
    blend = os.path.join(output_path, f"{filename.split('.')[0]}.blend")

    try:
        bpy.ops.file.autopack_toggle()
        bpy.ops.wm.save_as_mainfile(filepath=blend)
    except:
        bpy.ops.file.autopack_toggle()
        bpy.ops.wm.save_as_mainfile(filepath=blend)
        # pass
    bpy.ops.export_scene.fbx(
        filepath=fbx,
        path_mode='COPY',
        embed_textures=True
    )
    # bpy.ops.wm.save_as_mainfile(filepath=blend)
