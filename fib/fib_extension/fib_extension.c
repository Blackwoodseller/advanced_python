#include <Python.h>

static PyObject *fibext(PyObject *self, PyObject *args)
{

    long long int prev=0, cur=1, next;
    int n;

    if (!PyArg_ParseTuple(args, "i", &n)) {
      return NULL;
    }

    // return first number
    if (n<2) return PyLong_FromLong(prev);

    for (int i=3;i<=n;i++)
    {
        next = prev + cur;
        prev = cur;
        cur = next;
    }

    return PyLong_FromLongLong(cur);
}


static PyMethodDef module_methods[] = {
   { "fibext", (PyCFunction)fibext, METH_VARARGS, NULL },
   { NULL, NULL, 0, NULL }
};


static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "fibonacciext",
    "Fibonacci numbers C extension module",
    -1,
    module_methods
};


PyMODINIT_FUNC PyInit_fibonacciext(void)
{
    return PyModule_Create(&moduledef);
}
