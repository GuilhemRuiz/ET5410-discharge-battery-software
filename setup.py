#####################################################
# This is the program which convert the .py to .exe #
#####################################################

from cx_Freeze import setup, Executable
import sys
import os

#the following lines have to be change depending on your python implementation
includes = []
include_files = [r"C:\Users\guilh\AppData\Local\Programs\Python\Python310\DLLs\tcl86t.dll",
                 r"C:\Users\guilh\AppData\Local\Programs\Python\Python310\DLLs\tk86t.dll",
                 "checkVert.png",
                 "croixRouge.png",
                 "logo.png",
                 "icone.ico"
                ]
os.environ['TCL_LIBRARY'] = r'C:\Users\guilh\AppData\Local\Programs\Python\Python310\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\guilh\AppData\Local\Programs\Python\Python310\tcl\tk8.6'
base = 'Win32GUI' if sys.platform == 'win32' else None

setup(
    name="Software by Guilhem RUIZ www.linkedin.com/in/guilhem-ruiz",
    version="1.0",
    description="Software for battery discharge for ET54",
    author = "Guilhem Ruiz",
    options={"build_exe": {"includes" : includes, "include_files": include_files}},
    executables=[Executable("ET54Software.py", base=base, icon = "icone.ico")],
)