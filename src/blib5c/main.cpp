#include <Python.h>
#include <numpy/arrayobject.h>

static PyMethodDef module_methods[] = 
{

    {nullptr, nullptr, 0, nullptr}        /* Sentinel */
};

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "blib5c",   /* name of module */
    "Functionality for the blib5 module written in C++", /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    module_methods
};

PyMODINIT_FUNC
PyInit_blib5c(void)
{
    PyObject *m = PyModule_Create(&spammodule);
    if (m)
    {
        ;
    }
    return m;
}

