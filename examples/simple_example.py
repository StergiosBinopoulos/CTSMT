import sys
import os

filepath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(filepath))

from scenario import Scenario
from animation import AnimateSimulation
from parameters import *

from busenvironments import citaro_g_3_door


# verbose set to False so the simulation won't print the events
dsim = Scenario(citaro_g_3_door, verbose=False)


dsim.driver(17  , 2.1, inf=False)
dsim.spawn_passengers(60, 1, doors_prob=[0.4, 0.4, 0.2])
dsim.initialize_models()


duration = 1200
for step in range(duration):
    dsim.step()
    if step == 300:
        dsim.spawn_passengers(12, 3, doors_prob=[0, 0, 1])
    
    if step == 800:
        dsim.remove_passengers(35)
    
    if step == 850:
        dsim.open_doors()


states = dsim.states_t
animate = AnimateSimulation(citaro_g_3_door, states,  delta_t=DELTA_T)
animate.animation()


