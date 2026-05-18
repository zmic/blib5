import importlib
from blib5.remote import blender_connect

def test1():
    send = blender_connect()
    send(importlib.import_module, 'sys')

test1()

