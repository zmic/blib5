import bpy
from blib5.module import reload_module_tree
from blib5.remote import start_server, stop_server
from . import __main__

bl_info = {
    "name": "blib5", 
    "category": "User",
    "author": "ik",
    "blender": (5,1,1),
    "support": "COMMUNITY",  
}

class operator_main(bpy.types.Operator):
    bl_idname = "user.blib5"
    bl_label = "blib5"
    bl_options = {'REGISTER'}
    def execute(self, context): 
        print("========================== BLIB5 ==========================") 
        reload_module_tree(__main__)   
        __main__.main(context)  
        return {'FINISHED'}

def register():
    start_server("blib5")
    bpy.utils.register_class(operator_main)

def unregister():
    stop_server()
    bpy.utils.unregister_class(operator_main)
  