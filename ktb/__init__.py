'''
kinect toolbox: A more intuitive interface for the kinectv2.
==================================================

Copyright (c) 2020 by Nikolas Lamb.
'''

from .kinect import Kinect
from .constants import *

# Environment setup for cross-platform compatibility
import os
import sys
import warnings

# Check for required environment variable
libfreenect2_prefix = os.getenv('LIBFREENECT2_INSTALL_PREFIX')
if libfreenect2_prefix is None:
    warnings.warn(
        "LIBFREENECT2_INSTALL_PREFIX environment variable not set. "
        "Set it to your libfreenect2 installation path.", 
        ImportWarning
    )
else:
    # Windows-specific DLL loading support
    if sys.platform == "win32":
        dll_path = os.path.join(libfreenect2_prefix, "bin")
        if os.path.exists(dll_path):
            # For Python 3.8+, use os.add_dll_directory
            if hasattr(os, 'add_dll_directory'):
                os.add_dll_directory(dll_path)
            # Also add to PATH as fallback
            os.environ["PATH"] = dll_path + os.pathsep + os.environ.get("PATH", "")
    
    # Linux/macOS library path setup
    elif sys.platform in ["linux", "darwin"]:
        lib_path = os.path.join(libfreenect2_prefix, "lib")
        if os.path.exists(lib_path):
            env_var = "DYLD_LIBRARY_PATH" if sys.platform == "darwin" else "LD_LIBRARY_PATH"
            current_path = os.environ.get(env_var, "")
            if lib_path not in current_path:
                warnings.warn(
                    f"Add {lib_path} to your {env_var} environment variable", 
                    ImportWarning
                )