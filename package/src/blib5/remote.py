import socket
import sys
import _thread
import traceback
import importlib   # so remote client can call importlib
import types

import dill
import bpy

import blib5
from .cprint import cprint
from .module import reload_module_tree


##########################################################################
#
#   server side = Blender
#
#   The register() function of the user addon should call start_server()
#        
#
HOST = '127.0.0.1'    # The remote host
PORT = 18131
client_count = 0            

def start_server_():
    start_server__()
    cprint("Closed listening port")

def send_packet(s, data):
    s.sendall(len(data).to_bytes(8, byteorder='big', signed=False))
    s.sendall(data)

def receive_bytes(s, nbytes):
    data = b''
    while nbytes:
        data_ = s.recv(nbytes)
        if not data_: 
            return b''
        nbytes -= len(data_)
        data += data_
    return data

def receive_packet(s):
    data = receive_bytes(s, 8)
    if data:
        packet_length = int.from_bytes(data, byteorder='big', signed=False)
        data = receive_bytes(s, packet_length)
    return data

##########################################################################
def add_path__(path):
    sys.path.append(path)
    cprint(sys.path)

def import_module__(module):
    cprint(f"importing {module}")
    m = importlib.import_module(module)
    base_module = sys.modules[m.__name__.split('.')[0]]
    globals()[base_module.__name__] = base_module

def execute_function(function, args, kwargs):
    cprint(f"execute_command: {function}({len(args)} arguments)")  
    function = eval(function)
    return function(*args, **kwargs)

def wrap_con(connection, command, args, kwargs):
    def run_in_main_thread():
        try:
            rv = execute_function(command, args, kwargs)
        except Exception as error:            
            traceback_string = traceback.format_exc()
            rv = None
            for L in traceback_string.split('\n'):
                cprint(L)
        else:
            traceback_string = None
        rv = dill.dumps((traceback_string, rv))
        #cprint(f"Send {len(rv)} bytes")
        send_packet(connection, rv)
        #cprint(f"Done send {len(rv)} bytes response")
    return run_in_main_thread
    

def start_server__():
    global client_count 
    cprint("Listening on {}:{}".format(HOST, PORT))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        while 1:
            conn, addr = s.accept()
            cprint('Connected by', addr)
            while 1:
                data = receive_packet(conn)
                if not data:
                    break
                try:
                    command, args, kwargs = dill.loads(data)
                except EOFError:
                    continue
                if command == 'UNREGISTER':
                    client_count -= 1
                    if client_count == 0:
                        return
                else:
                    reload_module_tree(blib5) 
                    run_in_main_thread = wrap_con(conn, command, args, kwargs)
                    bpy.app.timers.register(run_in_main_thread)
            del conn
            cprint('Disconnected by', addr)


def start_server(addon_name):
    global client_count    
    client_count += 1    
    cprint(f"start_server() called by {addon_name}, {client_count=}")
    if client_count == 1:
        _thread.start_new_thread(start_server_, ())

def stop_server():
    pass

# 
# client side = your script
#
class connection:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
    def command(self, command, *args, **kwargs):
        if not isinstance(command, str):
            command = f'{command.__module__}.{command.__qualname__}'        
        b = dill.dumps((command, args, kwargs))
        send_packet(self.s, b)
        data = receive_packet(self.s)
        error, rv = dill.loads(data)
        if error:
            print("Remote error:")
            for L in error.split('\n'):
                print("+  ", L)
            raise RuntimeError("remote error")
        return rv 
    def import_lib(self, module):
        if isinstance(module, types.ModuleType):
            module = module.__name__
        self.command('import_module__', module)


'''
if __name__ == '__main__':
    send_message("blib3.mesh.test1", 0, w=1)
'''

    
