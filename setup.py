import sys
from cx_Freeze import setup, Executable

setup(
    name = "Table Football",
    version = "1.0",
    description = "Assignment 2, 02/10/2016",
    executables = [Executable("main.py", base = "Win32GUI")])