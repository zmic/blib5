import inspect
import builtins

def introspect_caller():
    current_frame = inspect.currentframe()
    caller_frame = current_frame.f_back.f_back
    caller_module = inspect.getmodule(caller_frame)
    caller_function_name = caller_frame.f_code.co_name
    caller_module_name = caller_module.__name__ if caller_module else None
    return caller_module_name, caller_function_name

def cprint(*args, **kwargs):
    caller_module_name, caller_function_name = introspect_caller()
    header = f'[{caller_module_name+'.'+caller_function_name: <40}] '
    print(header, *args, **kwargs)

builtins.cprint = cprint

