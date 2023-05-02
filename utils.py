import numpy as np
from examples.busenvironments import *
import parameters

def read_states(filename):
    file = open(filename)

    states = []
    state = []
    first = True
    for line in file:
        if first:
            first = False
            continue

        if line[0] == "#":
            states.append(np.asarray(state))
            state = []
            continue

        line = line.strip()
        row = line.split(",")
        row = [float(x) for x in row]
        state.append(row)

    file.close()
    states.append(np.asarray(state))

    return states


def export_environment(env, filename):
    file = open(filename, "w")
    lines = []

    lines.append(f"dimensions:{env.dimensions[1]},{env.dimensions[0]},{env.aisle_width},{env.min_standing_x}\n")
    
    for seat in env.seat_list:
        lines.append(f"seat:{seat.x},{seat.y},{seat.rotation}\n")
    
    for spot in env.standing_spots:
        lines.append(f"spot:{spot.x},{spot.y}\n")

    for door in env.doors:
        lines.append(f"door:{door[0]},{door[1]}\n")

    for door in env.doors:
        lines.append(f"door:{door[0]},{door[1]}\n")

    for wall in env.walls:
        for row in wall:
            lines.append(f"wall:{row[0]},{row[1]}\n")     

    for door_wall in env.door_walls:
        for row in door_wall:
            lines.append(f"door_wall:{row[0]},{row[1]}\n")

    for bound in env.standing_boundaries:
        for row in bound:
            lines.append(f"standing_boundary:{row[0]},{row[1]}\n")

    file.writelines(lines)
    file.close()


def export_parameters(filename):
    file = open(filename, "w")
    params = {key: value for key, value in parameters.__dict__.items() if not (key.startswith('__') or key.startswith('_'))}

    lines = []
    for key, val in params.items():
        lines.append(f"{key}:{val}\n")

    file.writelines(lines)
    file.close()