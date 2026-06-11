from functools import wraps
import inspect
import bpy
from .data import delete_object_and_data_if_orphaned

_missing = object()
def cache_unary_function_result(f):
    def f_wrapper(x, CACHE={}):
        r = CACHE.get(x, _missing)
        if r is _missing:
            r = f(x)
            CACHE[x] = r
        return r
    return f_wrapper


def blender_object(select_set=True, active_set=True, delete_object_with_same_name=False, create=False):
    def decorator(func):
        sig = inspect.signature(func) 
        has_kwargs = False
        param_names = set()
        for param in sig.parameters.values():
            if param.kind == inspect.Parameter.VAR_KEYWORD:
                has_kwargs = True
            elif param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                param_names.add(param.name)
        @wraps(func)
        def wrapper(*args, **kwargs) -> bpy.types.Object : 
            #print("wrapper", args, kwargs)
            scene = kwargs.pop('scene', bpy.context.scene if create else None)
            if isinstance(scene, str):
                    c = bpy.data.scenes(str)
            c = kwargs.pop('collection', scene.collection if create else None)
            #c = kwargs.pop('collection', None)
            m = kwargs.pop('material', None)
            g = kwargs.pop('geo', None)
            s = kwargs.pop('select_set', select_set)
            a = kwargs.pop('active_set', active_set)           
            d = kwargs.pop('delete_object_with_same_name', delete_object_with_same_name)
            if d:
                if (name := kwargs.get('name', None)) and (o := bpy.data.objects.get(name)):
                    delete_object_and_data_if_orphaned(o)
            data_attrs = []
            if not has_kwargs:
                for k in list(kwargs.keys()):
                    if not k in param_names:
                        data_attrs.append( (k, kwargs.pop(k)) )
            bound_args = sig.bind(*args, **kwargs) 
            o = func(*bound_args.args, **bound_args.kwargs)
            for k, v in data_attrs:
                setattr(o.data, k, v)
            if c:
                if isinstance(c, str):
                    c = bpy.data.collections[c]
                if not isinstance(c, bpy.types.Collection):
                    raise TypeError("collection should be of type bpy.types.Collection")
                c.objects.link(o)
            if m:
                if isinstance(m, str):
                    m = bpy.data.materials[m]
                if not isinstance(m, bpy.types.Material):
                    raise TypeError("material should be of type bpy.types.Material")
                o.data.materials.append(m)
            if g:   # geo node group
                node_group = bpy.data.node_groups[g]
                modifier = o.modifiers.new(name=g, type='NODES')
                modifier.node_group = node_group
            if s:
                if isinstance(s, bpy.types.ViewLayer):
                    o.select_set(True, view_layer=s)
                else:
                    o.select_set(True)
            if a:
                if isinstance(a, bpy.types.ViewLayer):
                    a.objects.active = o
                else:
                    bpy.context.view_layer.objects.active = o
            return o
        return wrapper
    return decorator
   

def blender_object_create(select_set=True, active_set=True, delete_object_with_same_name=True):
    return blender_object(select_set=select_set, active_set=active_set, delete_object_with_same_name=delete_object_with_same_name, create=True)

             

