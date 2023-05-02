# Crowd Transmission Simulation in Mass Transit
CTSMT is a collection of Python modules for 2D crowd simulation combined with viral transmission simulation in mass transit. The Social Force Model is used to simulate the passengers' movements and the transmission probabilities are calculated based on a modified Wells-Riley model. Passengers seat/spot selection is probabilistic based on a utility score for every option.

![Alt text](./docs/image.gif?raw=true "Basic Simulation")


## Usage
### 1. Import the required modules
```python
import sys
import os

filepath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(filepath))

from scenario import Scenario, Environment
from animation import AnimateSimulation
from parameters import *
```

### 2. Create an environment

Create a new mass transit environment using the Environment class (environment/environment.py):

```python
bus = Environment()
bus.boundaries(5.5, 2.5) # 5.5m length, 2.5m width
```

Add seats, standing spots, doors and obstacles to the environment:

```python
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
                    closed=False, fc='none')
```

A standing area should be defined where passengers can stand and walk freely. This area is defined using the 'obstacle_polyline' method and setting the optional argument 'standing' equal to True.

```python
# Points (x, y) indicating the polyline shape.
# The shape should be closed.
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
```


### 3. Create a scenario

Create a new scenario instance based on the environment defined previously. 
```python
dsim = Scenario(bus)
```

Create the initial conditions by adding a driver (optional), and spawning passengers outside of the environment.
```python
dsim.driver(4.5, 2.1, inf=True)

# doors_prob is a list of the probability of passengers spawning
# outside each door. The length of the list should be equal to the 
# number of doors in the environment and the sum of the list must add up 
# to one  

# This spawns 10 passengers of which 1 carries the disease
dsim.spawn_passengers(10, 1, doors_prob=[1])

dsim.initialize_models()
```

Start simulating step by step until the desired duration. Add various actions at specific steps (spawn_passengers, remove_passengers, open_doors).
```python
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
``` 


### 4. Animating the simulation
Animate using the AnimateSimulation class and the states stored in the scenario instance.

```python
states = dsim.states_t
animate = AnimateSimulation(bus, 
                            states, 
                            delta_t=DELTA_T)
animate.animation()
```

(Alternatively) Visualize the standing bounds, standing spots and collision lines, created by the obstacles, by setting the respected variables to True (useful for debugging).

```python
animate = AnimateSimulation(bus, 
                            states, 
                            delta_t=delta_t,
                            standing_bounds=True, 
                            standing_spots=True, 
                            collision_lines=True)
animate.animation()
```


See more in the "examples" directory.

## Parameter Tuning

Simulation parameters can be found inside the "parameters.py" module and tuned as needed to achieve the desired results. For example by setting the MADJ parameter to 0, a policy can be simulated in which passengers will not select a seat if the adjacent seat is occupied.

## Using the C++ Core
Using the C++ core produces faster results for passenger numbers <200. The C++ core configures the simulation based on three input files; "conditions.txt", "parameters.txt" and "actions.txt" located in the "cpp/files" directory and outputs the results to the "state.txt" file located in the same directory. The user defines actions that would take place in the simulation inside the "actions.txt" file, the other two input files can be exported directly from Python using the functions defined in the "utils.py" module.

See more in the "actions.txt" file. 

### 1.  Compiling
Inside the "cpp" directory (using gnu make and gcc)

```
make && make clean
```

### 2. Extracting the required files
Create a new python file and import the required modules and export the input files in the correct directory ("cpp/files").
```python
import sys
import os
import subprocess

filepath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(filepath))

from utils import read_states, export_environment, export_parameters
from animation import AnimateSimulation
from busenvironments import citaro_g_3_door
from parameters import *

export_parameters(filepath + "/../cpp/files/parameters.txt")
export_environment(citaro_g_3_door, filepath + "/../cpp/files/conditions.txt")
```

### 3. Calling the C++ core and reading the results
```python
executable_path = filepath + "/../cpp/core"
subprocess.call(executable_path, cwd=filepath+'/../cpp')
states = read_states(filepath + "/../cpp/files/states.txt")
```
(If you're using windows you should change the 'executable_path' accordingly (core.exe).)


### 4. Animating the simulation

```python
animate = AnimateSimulation(citaro_g_3_door, states,  delta_t=DELTA_T)
animate.animation()
```
See more in the "examples/cpp_core_example.py" file. 