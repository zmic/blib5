import bpy


blender_type_to_collection = {
    bpy.types.Mesh : 'meshes',
    bpy.types.Curve : 'curves',
    bpy.types.Camera : 'cameras',
    bpy.types.Light : 'lights',
    bpy.types.GeometryNodeTree : 'node_groups',
    bpy.types.Material : 'materials',  # materials are not in objects
}

def delete_object_and_data_if_orphaned(o):
    data = o.data
    bpy.data.objects.remove(o)
    if data.users == 0:
        C = blender_type_to_collection.get(type(data), None)
        if C:
            getattr(bpy.data,C).remove(data)    

