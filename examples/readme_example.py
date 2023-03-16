import sys
import os

filepath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(filepath))

from scenario import Scenario, Environment
from animation import AnimateSimulation
from parameters import *


bus = Environment()
bus.set_dimensions(5.5, 2.5) # 5.5m length, 2.5m width

bus.seat(1.4, 0.8, rotation=0, size=(0.4, 0.4))

bus.seat_row(1.4, 0.4, 3)

bus.seat_column(0.7, 0.65, 4)

# Each tuple represents the coordinates of a standing spot 
bus.standing_spot((2, 1.8), (4.5, 0.8))

# door positioned 3.5 meters from the start of the vehicle
bus.door(3.5, width=1.25)

# driver enclosure
bus.obstacle_object((3.5, 2.5), 
                    (3.5, 2), 
                    (4, 1.5), 
                    (5.5, 1.5), 
                    linewidth=2, 
                    closed=False, 
                    fc='none')

# standing area
bus.obstacle_polyline((0.9, 0.9), 
                      (0.9, 2.4), 
                      (3.4, 2.4), 
                      (3.4, 2), 
                      (3.9, 1.4), 
                      (5.4, 1.4), 
                      (5.4, 0.1), 
                      (2.88, 0.1), 
                      (2.88, 0.9), 
                      (0.9, 0.9), 
                      standing=True)



dsim = Scenario(bus)

dsim.driver(4.5, 2.1, inf=True)
dsim.spawn_passengers(10, 1, doors_prob=[1])
dsim.initialize_models()

# doors open automatically only when spawning 
# passengers not when removing
# it's best to open doors/spawn passengers approx. 5 seconds 
# after removing passengers to avoid exiting 
# passengers from getting stuck

# duration in steps (200s with the default 0.1s step)
duration = 2000
for step in range(duration):
    dsim.step()
    if step == 500:
        dsim.remove_passengers(7)

    if step == 550:
        dsim.open_doors()
    
    if step == 1400:
        dsim.remove_passengers(3)

    if step == 1450:
        dsim.spawn_passengers(12, 3, doors_prob=[1])


states = dsim.states_t
animate = AnimateSimulation(bus, 
                            states, 
                            delta_t=DELTA_T,
                            standing_bounds=True, 
                            standing_spots=True, 
                            collision_lines=False)
animate.animation()


