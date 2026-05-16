import bpy 

def ensure_scene_collections(names, scene=None):
    if scene is None:
        scene = bpy.context.scene
    S = set()
    for n in names:
        b = ''
        S.update([b:=b+'/'+x for x in n.split('/')])
    def walk_collections(stem, C):
        for c in C.children[:]:
            c_stem = stem + '/' + c.name
            if c_stem in S:
                S.remove(c_stem)
                walk_collections(c_stem, c)
            else:
                C.children.unlink(c)
    walk_collections('', scene.collection)
    for p in sorted(list(S)):
        L = p.split('/')
        if len(L) == 2:
            parent_collection = scene.collection
        else:
            parent_collection = bpy.data.collections[L[-2]]
        c = bpy.data.collections.get(L[-1])
        if not c:
            c = bpy.data.collections.new(L[-1])
        parent_collection.children.link(c)

        
