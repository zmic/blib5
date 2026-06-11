from contextlib import contextmanager
import numpy as np
import bpy
import bmesh
from . import decorate


@contextmanager
def new_mesh(object_name, mesh_name=None):
    bm = bmesh.new()
    mesh = bpy.data.meshes.new(mesh_name or object_name) 
    obj = bpy.data.objects.new(object_name, mesh)     
    try:
        yield bm, obj 
    finally:
        bm.to_mesh(mesh)  
        bm.free() 

@decorate.blender_object_create()
def mesh_only_edges(VERTICES, INDICES, object_name, mesh_name=None):
    with new_mesh(object_name, mesh_name) as (bm, obj):
        V, E = bm.verts, bm.edges
        for p in VERTICES:
            V.new(p)               
        V.ensure_lookup_table()
        for e in INDICES:
            E.new((V[e[0]], V[e[1]]))    
    #######################################################      
    return obj

def create_mesh_polyline(V, closed, **kwargs):
    v = V.shape[0]
    I = np.empty((v,2),dtype=np.int32)
    I[:,0] = np.arange(v)
    I[:,1] = I[:,0] + 1
    if closed:
        I[v-1,1] = 0     
    else:
        I = I[:-1]    
    return mesh_only_edges(V, I, **kwargs)

