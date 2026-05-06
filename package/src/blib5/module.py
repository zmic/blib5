import sys
import os
import importlib    
from pathlib import Path
from collections import defaultdict
from .cprint import cprint

def dependencies(main_folder, parent_module, module, D):
    already_visited = module in D
    D[module].add(parent_module)
    for upstream_module in D[parent_module]:
        D[module].add(upstream_module)
    if not already_visited:
        for k, v in module.__dict__.items():
            if type(v) == type(module):
                file = getattr(v, '__file__', None)  # built-in modules don't have __file__
                if file:
                    #print(module.__name__, 'imports', file)
                    if Path(file).is_relative_to(main_folder):
                        #if v in D[module]:
                        #    raise RuntimeError('Circular dependency between {} and {}'.format(v.__name__, module.__name__))
                        if not v in D[module]:
                            dependencies(main_folder, module, v, D)

last_modified_dict = defaultdict(float)

def reload_module_tree(main_module):
    main_folder = Path(main_module.__file__).parent
    D = defaultdict(set)
    #dependencies(main_folder, sys.modules[__name__], main_module, D)
    dependencies(main_folder, None, main_module, D)
    D[main_module] = set()
    S_reload = set()
    while len(D) > 1:
        for module in D.keys():
            m_is_leaf = True
            for s in D.values():
                if module in s:
                    m_is_leaf = False
                    break
            if m_is_leaf:
                reload = module in S_reload
                path = module.__file__
                last_modified = os.path.getmtime(path)
                last_modified_stored = last_modified_dict[path]
                if last_modified > last_modified_stored:
                    reload = True
                    S_reload.update(D[module])
                    last_modified_dict[path] = last_modified                    
                if reload:
                    if module.__name__ not in ['blib5.module', 'blib5.network', 'blib5.timer']:
                        cprint(f"reload: module {module.__name__}")
                        importlib.reload(module)
                del D[module]
                break


if __name__ == '__main__':
    import blib5.network
    reload_module_tree(blib5)


