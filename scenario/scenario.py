"""Scenario creation"""

import numpy as np
import random

from transmissionmodel.transmission import TransmissionSimulation
import socialforcemodel as sfm
from scenario.passenger import Passenger
from parameters import *

class Scenario:
    """Class for setting simulation scenarios."""
    def __init__(self, env, verbose=True):
        self.env = env
        self.verbose = verbose
        self.standing_spots = np.asarray(env.standing_spots)
        self.standing_boundaries = env.standing_boundaries
        self.dimensions = env.dimensions
        self.doors = env.doors
        self.seat_list = env.seat_list

        self.walls = env.create_walls()
        self.door_wall = [np.array([(x, 0) for x in np.linspace(0, self.dimensions[0], 300)])]

        self.passenger_list = []

        self.states_t = []
        self.frame = 0
        self.door_counter = 0
        self.door_timeout = 0
        self.passengers_outside = 0
        self.passengers_exiting = 0
        self.passengers_exiting_last = 0
        self.passengers_outside_last = 0

        self.last_positions = None
        self.stabilized = False

        self.force_simulator = None 
        self.state_f = None
        self.speeds = None

        self.trans_simulator = None
        self.state_t = None
        self.inf_probs = None

        self.phases = None
        self.delta_t = DELTA_T
        self.open = False
        self.opened_doors = False

        
    def passenger(self, x, y, dx=0, dy=0, phase=0, inf=False):
        """Appends the coordinates of a passenger in their respected lists."""
        # dx, dy can't be = x, y (math error)
        if (dx == x) and (dy == y):
            dx = x - 0.01
            dy = y - 0.01
        self.passenger_list.append(Passenger(x, y, dx, dy, self.env, phase, inf))

    def driver(self, x, y, inf=False):
        """Stores a driver and sets the 'driver_id' equal to its.
        If a passenger with the same coordinates already exists it just sets the 'driver_id' equal to its.
        """
        self.passenger(x, y, x - 0.01, y, phase=-1, inf=inf)

    def _door_selection(self, doors_prob, n_in):
        """Probabilistically distributes passengers to the available doors."""
        door_choices = [0] * len(self.doors)
        for i in range(n_in):
            c = np.random.choice(np.arange(0, len(self.doors)), p=doors_prob)
            door_choices[c] += 1
        return door_choices

    def spawn_passengers(self, n_in, n_source, doors_prob):
        """Generates passengers' position."""
        # generated x, y in a 2x2 area located below the center of the door
        door_choices = self._door_selection(doors_prob, n_in)
        source_id = random.sample(range(n_in), n_source)
        self.open = True
        id_ = 0
        for i in range(len(door_choices)):
            door_x = self.doors[i][0]
            for j in range(door_choices[i]):
                x = (random.random()-0.5) * 2 + door_x
                y = random.random() * -2
                dy = self.dimensions[1]/2
                inf = id_ in source_id
                self.passenger(x, y, door_x, dy, phase=0, inf=inf)
                id_ += 1            

    def remove_passenger(self, i):
        """Remove the nth passenger"""
        self.passenger_list[i].remove()

    def remove_passengers(self, n):
        """N passengers will exit the environment"""
        passengers = [p for p in self.passenger_list if p.phase != -1 or p.phase > 6]
        n_passengers = len(passengers)
        ids = random.sample(range(n_passengers), n)
        for i in ids:
            passengers[i].remove()
    
    def initialize_models(self):
        """Initializes the social force model, the transmission model and the passenger logic."""
        # create the state arrays
        self.update_states()

        # block the doors until they are opened
        self.walls_doors_closed = sfm.PedSpacePotential(self.walls + self.door_wall, u0=U0_E, r=R_E)
        self.walls_doors_open = sfm.PedSpacePotential(self.walls, u0=U0_E, r=R_E)
        standing_boundaries = sfm.PedSpacePotential(self.standing_boundaries, u0=U0_SB, r=R_SB)
        passenger_force = sfm.PedPedPotential(self.delta_t, v0=V0, sigma=PEDPED_SIGMA)

        for seat in self.seat_list:
            seat.adjacent_seats(self.seat_list)

        self.inf_probs = np.expand_dims(np.array([p.inf_at_prob for p in self.passenger_list]), 0)

        self.force_simulator = sfm.Simulator(self.state_f, ped_space=self.walls_doors_closed, ped_ped=passenger_force, ped_walkspace=standing_boundaries, tau=0.3, delta_t=self.delta_t)
        self.force_simulator.update_state(self.state_f, self.speeds, self.phases)
        self.trans_simulator = TransmissionSimulation(self.state_t, self.inf_probs, delta_t=self.delta_t, c=TF)

    def open_doors(self):
        """Schedules the doors to be opened"""
        self.open = True
        self.stabilized = False
        self.door_counter = 0
        self.door_timeout = 0

    def update_doors(self):
        """Updates the state of the doors (opens or closes as needed)"""
        # Open doors if doors are scheduled to be opened
        if self.open:
            self.door_counter += 1
            if self.door_counter >= int(DOOR_OPEN_DELAY/self.delta_t):
                self.force_simulator.update_ped_space(self.walls_doors_open)
                self.opened_doors = True
                self.open = False
                self.door_counter = 0
                self.info_text(1)

        # If already open close
        if self.opened_doors:
            if self.passengers_outside != self.passengers_outside_last:
                self.door_timeout = 0
            elif self.passengers_exiting != self.passengers_exiting_last:
                self.door_timeout = 0
            else:
                self.door_timeout += 1

            self.door_counter += 1
            if self.door_timeout >= int(DOOR_TIMEOUT/self.delta_t) and self.door_counter >= int(MIN_DOOR_TIME/self.delta_t):
                self.opened_doors = False
                self.info_text(1)
                self.force_simulator.update_ped_space(self.walls_doors_closed)
                self.door_timeout = 0
                self.door_counter = 0

                for passenger in self.passenger_list:
                    if passenger.phase == 0:
                        self.passenger_list.remove(passenger)

    def update_states(self):
        """Updates the np arrays required for the simulation models"""
        self.state_t = np.array([[p.x, p.y, p.prob, p.inf] for p in self.passenger_list])
        self.state_f = np.array([[p.x, p.y, p.vx, p.vy, p.dx, p.dy, p.tau] for p in self.passenger_list])
        self.speeds = np.array([p.desired_speed for p in self.passenger_list])
        self.inf_probs = np.expand_dims(np.array([p.inf_at_prob for p in self.passenger_list]), 0)
        self.phases = np.expand_dims(np.array([p.phase for p in self.passenger_list]), axis=-1)

    def update_from_states(self, state_t, state_f):
        """Update the passenger objects from the np arrays used by the models"""
        for i in range(state_f.shape[0]):
            p = self.passenger_list[i]
            p.x = state_f[i, 0]
            p.y = state_f[i, 1]
            p.vx = state_f[i, 2]
            p.vy = state_f[i, 3]
            p.dx = state_f[i, 4]
            p.dy = state_f[i, 5]

        for i in range(state_t.shape[0]):
            p = self.passenger_list[i]
            p.prob = state_t[i, 2]
            p.inf = state_t[i, 3]

    def update_phases(self):
        """Triggers the phase/destination update for passengers"""
        changes = False
        self.passengers_outside_last = self.passengers_outside
        self.passengers_exiting_last = self.passengers_exiting
        self.passengers_outside = 0
        self.passenger_exiting = 0
        for passenger in self.passenger_list:
            change = passenger.phase_update(self.standing_spots, self.seat_list, 0.1, self.doors)
            changes = changes or change

            if passenger.phase == 9:
                self.passenger_list.remove(passenger)
                changes = True

            if passenger.phase >= 6:
                self.passenger_exiting += 1

            elif passenger.phase == 0:
                self.passengers_outside += 1
        return changes

    def info_text(self, key, n=0):
        """Prints useful information about the events occurring"""
        if self.verbose:
            # key 0 -> passengers added/removed
            if key == 0:
                if n == 0:
                    return
                elif n < 0:
                    print(abs(n), "passenger(s) removed from the simulation at frame:", 
                        self.frame, "|", (len(self.passenger_list)), "remaining |")
                else:
                    print(n, "passenger(s) added to the simulation at frame:", 
                        self.frame, "|", (len(self.passenger_list)), "total |")

            # key 1 -> doors update
            elif key == 1:
                if self.opened_doors:
                    print("Doors opened at frame:", self.frame)
                else:
                    print("Doors closed at frame:", self.frame)

    def step(self):
        """Do one step in the simulation and update the model states."""
        # If the doors haven't been opened yet open them if at least 1.5 sec in the simulation
        self.update_doors()
        
        changes = self.update_phases()
        diff = (len(self.passenger_list) - self.state_f.shape[0])
        if changes or diff != 0:
            self.info_text(0, diff)
            self.update_states()
            self.trans_simulator.inf_probs = self.inf_probs
            self.trans_simulator.state = self.state_t
            self.force_simulator.update_state(self.state_f, self.speeds, self.phases)
            self.stabilized = False

        self.state_t = self.trans_simulator.step().state
        self.states_t.append(self.state_t.copy())

        # do the simulation steps only simulate movements if passengers aren't stabilized
        if not self.stabilized:
            self.state_f = self.force_simulator.step().state
            self.stabilized = self.stability(10)

        self.trans_simulator.state[:, 0:2] = self.force_simulator.state[:, 0:2]

        self.update_from_states(self.state_t, self.state_f)
        self.frame += 1

    def stability(self, n):
        """Checks every n_secs seconds if the crowd movements have been stabilized"""
        if self.delta_t*self.frame % n == 0 and self.frame > 0:
            try:
                if (abs(self.state_f[:, 0:2] - self.last_positions) < 0.1).all():
                    return True
            except:
                self.last_positions = self.state_f[:, 0:2].copy()
                return False
            
            self.last_positions = self.state_f[:, 0:2].copy() 
        return False
