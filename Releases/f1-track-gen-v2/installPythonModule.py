import sys
import subprocess
import os
import platform
import bpy

def isWindows():
    return os.name == 'nt'

def isMacOS():
    return os.name == 'posix' and platform.system() == 'Darwin'

def isLinux():
    return os.name == 'posix' and platform.system() == 'Linux'


def python_exec():
    if isWindows():
        return os.path.join(sys.prefix, 'bin', 'python.exe')

    elif isMacOS():
        try:
            # 2.92 and older
            path = bpy.app.binary_path_python

        except AttributeError:
            # For 2.93 and later
            path = sys.executable

        return os.path.abspath(path)

    elif isLinux():
        return os.path.join(sys.prefix, 'sys.prefix/bin', 'python')

    else:
        print("OS not supported", os.name, "-", platform.system)
        
        
def installModule(packageName):
    python_exe = python_exec()

    if not python_exe:
        print("Python executable not found.")
        return
     
    # Check if the module can be imported
    result = subprocess.call([python_exe, "-c", f"import {packageName}"])

    if result != 0:
        print(f"Module '{packageName}' not found. Attempting to install...")

        # Upgrade pip
        subprocess.call([python_exe, "-m", "pip", "ensurepip"])
        subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])

        # Install required package
        subprocess.call([python_exe, "-m", "pip", "install", packageName])
        
    else:
        print(f"Module '{packageName}' is already installed.")
