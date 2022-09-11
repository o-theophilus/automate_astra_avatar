import bpy
import bmesh


def vertex_group_to_face(obj, group_name):
    mesh = obj.data

    verts = []
    for v in mesh.vertices:
        for g in v.groups:
            if g.group == obj.vertex_groups[group_name].index:
                verts.append(v)

    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    for v in verts:
        v.select = True

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="FACE")
    bpy.ops.object.mode_set(mode='OBJECT')

    faces = []
    for f in mesh.polygons:
        if f.select == True:
            faces.append(f.index)

    return faces


def delete_occluded_faces(obj_name="body"):

    body = bpy.data.objects[obj_name]

    radius = -1
    for i in body.dimensions:
        if i > radius:
            radius = i

    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=2,
        radius=radius
    )
    pov = bpy.context.view_layer.objects.active
    pov.name = "pov"

    bpy.ops.object.select_all(action='DESELECT')
    body.select_set(True)
    pov.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.align(bb_quality=True, align_mode='OPT_2',
                         relative_to='OPT_4', align_axis={'X', 'Y', 'Z'})

    depsgraph = bpy.context.view_layer.depsgraph
    distance = radius * 2

    def get_hidden():
        seen = []
        for v1 in pov.data.vertices:

            v1_n = v1.normal
            v1 = pov.matrix_world @ v1.co

            for v2 in body.data.vertices:
                v2 = body.matrix_world @ v2.co

                origin = v1 - v1_n * 0.000001
                direction = v2 - v1
                direction.normalize()

                is_hit, hit_loc, hit_nor, hit_face_ind, hit_obj, matrix = bpy.context.scene.ray_cast(
                    depsgraph,
                    origin,
                    direction,
                    distance=distance
                )

                if hit_obj == body and hit_face_ind not in seen:
                    seen.append(hit_face_ind)

        hidden = [i.index for i in body.data.vertices if i.index not in seen]
        return hidden

    to_hide = get_hidden()
    # body.vertex_groups.new(name="occ")
    # body.vertex_groups['occ'].add(to_hide, 1.0, 'REPLACE')

    # ***************************************************
    # show = vertex_group_to_face(body, "show")
    # to_hide = [f for f in to_hide if f not in show]
    # hide = vertex_group_to_face(body, "hide")
    # hide = [f for f in hide if f not in to_hide]
    # to_hide = [*to_hide, *hide]
    # to_hide = vertex_group_to_face(body, "show")
    # ***************************************************

    me = body.data
    bm = bmesh.new()
    bm.from_mesh(me)

    faces = [f for f in bm.faces if f.index in to_hide]
    bmesh.ops.delete(bm, geom=faces, context="FACES")
    bm.to_mesh(me)
    # me.update()

    bpy.ops.object.select_all(action='DESELECT')
    pov.select_set(True)
    bpy.ops.object.delete()
