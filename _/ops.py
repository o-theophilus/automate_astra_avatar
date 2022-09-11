import bpy
import bmesh
import os


def reset():
    bpy.ops.wm.read_homefile(use_empty=True)


def get_clothes():
    reserved = ["body", "eye", "teeth", "tongue"]
    clothes = []
    for cloth in bpy.data.objects:
        if cloth.type == "MESH" and cloth.name not in reserved:
            clothes.append(cloth.name)

    return clothes


def fix_cloth_pose(clothes, body_name="body"):
    body = bpy.data.objects[body_name]

    for cloth_name in clothes:
        cloth = bpy.data.objects[cloth_name]
        bpy.context.view_layer.objects.active = cloth
        bpy.ops.object.modifier_add(type='SURFACE_DEFORM')
        cloth.modifiers["SurfaceDeform"].target = body
        bpy.ops.object.surfacedeform_bind(modifier="SurfaceDeform")

    armature = bpy.data.objects["Armature"]
    armature.data.pose_position = 'REST'

    for cloth_name in clothes:
        cloth = bpy.data.objects[cloth_name]
        bpy.context.view_layer.objects.active = cloth
        bpy.ops.object.modifier_apply(modifier="SurfaceDeform")


def bind_items(clothes):
    amt = bpy.data.objects["Armature"]
    # body_name = "body"
    # body = bpy.data.objects[body_name]

    for cloth_name in clothes:
        cloth = bpy.data.objects[cloth_name]
        if cloth.name.startswith("head"):
            cloth.select_set(True)
            bpy.context.view_layer.objects.active = cloth
            bpy.ops.object.mode_set(mode='EDIT')

            bm = bmesh.from_edit_mesh(cloth.data)
            bm.verts.ensure_lookup_table()
            verts = [y.index for y in bm.verts]

            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')

            cloth.vertex_groups.new(name="head")
            cloth.vertex_groups['head'].add(verts, 1.0, 'REPLACE')

            cloth.select_set(True)
            amt.select_set(True)
            bpy.context.view_layer.objects.active = amt
            bpy.ops.object.parent_set(type='ARMATURE_NAME')

        else:
            # cloth.select_set(True)
            # body.select_set(True)
            # bpy.context.view_layer.objects.active = cloth
            # bpy.ops.object.data_transfer(
            #     use_reverse_transfer=True,
            #     data_type='VGROUP_WEIGHTS',
            #     vert_mapping='POLYINTERP_NEAREST',
            #     layers_select_src='NAME',
            #     layers_select_dst='ALL'
            # )

            bpy.ops.object.select_all(action='DESELECT')

            cloth.select_set(True)
            amt.select_set(True)
            bpy.context.view_layer.objects.active = amt
            bpy.ops.object.parent_set(type='ARMATURE_NAME')
            cloth.modifiers["Armature"].use_deform_preserve_volume = True

    bpy.ops.object.select_all(action='DESELECT')


def set_pose():
    bpy.data.objects["Armature"].data.pose_position = 'POSE'
