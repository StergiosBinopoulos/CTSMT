import sys
import os
import subprocess

filepath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(filepath))

from utils import read_states, export_environment, export_parameters
from animation import AnimateSimulation
from busenvironments import citaro_g_3_door
from parameters import *

# extract the required c++ core input files in the correct directory
export_parameters(filepath + "/../cpp/files/parameters.txt")
export_environment(citaro_g_3_door, filepath + "/../cpp/files/conditions.txt")

# since the cpp core uses relative paths to read/write the simulation files
# we need to change the cwd to the cpp directory
subprocess.call(filepath + "/../cpp/core", cwd=filepath+'/../cpp')
states = read_states(filepath + "/../cpp/files/states.txt")

animate = AnimateSimulation(citaro_g_3_door, states,  delta_t=DELTA_T)
animate.animation()


