from sys import platform
import ctypes
import importlib.resources as pkg_resources


def _load_lib():
    if platform == "linux" or platform == "linux2":
        path = (pkg_resources.files('interop') / 'Interop.Native.so').__str__()
        lib = ctypes.CDLL(path)
    elif platform == "win32":
        path = (pkg_resources.files('interop') / 'Interop.Native.dll').__str__()
        lib = ctypes.WinDLL(path)
    elif platform == "darwin":
        path = (pkg_resources.files('interop') / 'Interop.Native.dylib').__str__()
        lib = ctypes.CDLL(path)
    return lib
