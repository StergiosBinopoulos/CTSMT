import numpy as np
import random

from parameters import *


class Passenger:
    """Class for passengers."""
    def __init__(self, x, y, dx, dy, env, phase=-1, inf=False, tau=TAU, speed=None):
        if speed == None:
            self.desired_speed = np.random.normal(SPEED, scale=SPEED_STD)
        else:
            self.desired_speed = speed

        self.seat_selection_prob = SEAT_SELECTION_PROB
        self.inf_at_prob = random.random()
        self.rand = random.random()

        self.x = x
        self.y = y
        self.dx = dx    
        self.dy = dy
        self.vx = self.desired_speed
        self.vy = 0
        self.prob = 0
        self.tau = tau
        self.inf = int(inf)*2
        self.phase = phase

        self.step = -1
        self.patience = abs(int(np.random.normal(PATIENCE, PATIENCE_STD)))
        
        self.initialized = False
        self.seat = None
        self.adj_occupied = []
        

        self.aisle_width = env.aisle_width
        self.xmax = env.dimensions[0]
        self.ymax = env.dimensions[1]
        self.y0 = self.ymax/2 - self.aisle_width/2
        self.y1 = self.ymax/2 + self.aisle_width/2
        self.min_standing_x = env.min_standing_x        

    def is_inside(self, x0, y0, x1, y1):
        """
        Returns true if the passenger is inside the rectangle 
        represented by the points x0, y0 and x1, y1 (bottom left and top right corners)
        """
        return x1 > self.x > x0 and y1 > self.y > y0

    def phase_update(self, standing_spots, seat_list, m_adj, doors):
        """Updates the passenger's phases based on it's position and performs 
        the required actions for each phase change (destination updates, seat or 
        standing spot selection and updating the availability status of seats).
        There are 9 phases in total:
            -1 for idle (used for the driver)
            0 for outside the vehicle and heading inside
            1, 2, 3 for movements towards a seat
            4 indicates seating
            5 indicates standing
            6, 7, 8 for exiting
            9 the passenger can be removed from the simulation
        """
        self.step += 1
        dx = self.dx
        dy = self.dy
        phase = self.phase
        change = False

        if self.phase == 6:
            change = True
            if self.y0 < self.y < self.y1 and self.x > self.min_standing_x + 0.2:
                nearest_door = self.nearest_door(doors)
                self.dx = nearest_door[0]
                self.phase = 7
            
        elif self.phase == 7:
            if self.y0 < self.y < self.y1:
                nearest_door = self.nearest_door(doors)
                self.dx = nearest_door[0]
            
            if self.is_inside(dx - 0.5, self.y0, dx + 0.5, self.y1):
                self.dy = - 0.5
            
            if self.is_inside(dx - 0.4, 0, dx + 0.5, 0.4):
                self.phase = 8

        elif self.phase == 8:
            if self.x < dx - 0.6 or self.x > dx + 0.6:
                self.phase = 7

            if self.y < 0:
                self.dy = - 10

            if self.y < -2:
                self.phase = 9

        elif self.phase == 5:
            if self.step % self.patience == 0:
                self.seat_selection(seat_list, standing_spots)

        self.to_phase_zero()

        if self.phase == 3:
            if self.is_inside(dx - 0.05, dy - 0.05, dx + 0.05, dy + 0.05):
                self.phase = 4

        elif self.phase == 2:
            #if stuck reset phase
            if not (self.y0 < self.y < self.y1):
                self.seat = None
                self.adj_occupied = []
                self.phase = 0
                return True

            if self.is_inside(dx - 0.6, dy - 2, dx + 0.6, dy + 2):
                self.dx = self.seat.x
                self.dy = self.seat.y
                self.seat.occupied = True
                self.phase = 3

        elif self.phase == 1:
            if self.y0 < self.y < self.y1:
                self.dx = self.seat.x + 0.3 * np.cos(self.seat.rotation * np.pi / 180)
                self.dy = self.ymax / 2
                self.phase = 2
            
        elif self.phase == 0:
            if not self.initialized:
                nearest_door = self.nearest_door(doors)
                self.dx = nearest_door[0]
                self.dy = self.ymax / 2
                self.initialized = True

            if self.is_inside(0, 0.1, self.xmax, self.ymax):
                self.initialized = False
                self.seat_selection(seat_list, standing_spots)

        # Check if anything used by the crowd simulation has changed
        if self.phase != phase or self.dx != dx or self.dy != dy:
            change = True
        
        return change

    def seat_selection(self, seat_list, standing_spots):
        """Chooses a seat or spot for the passenger.
        Passengers don't have knowledge of other passengers' choices.
        The probability of picking each option is depended on it's utility 
        (the utility functions can be found in 
        'seat.py' and 'spot.py').
        """
        if self.seat_selection_prob > self.rand:
            seat = self.selection(seat_list, self.x)
            if seat != -1:
                self.seat = seat
                self.adj_occupied = [s.occupied for s in self.seat.adjacent]
                self.phase = 1
                return

        if self.phase != 5:    
            spot = self.selection(standing_spots, self.x)
            self.dx = spot.x
            self.dy = spot.y
            self.phase = 5

    def selection(self, options, *args):
        """A simple selection function. 
        Returns an option or -1 if there are 
        no options with utility greater than 0
        """
        utilities = []
        pool = []
        for option in options:
            utility = option.utility(*args)
            if utility > 0:
                utilities.append(utility)
                pool.append(option)  
        
        utility_sum = sum(utilities)
        
        if utility_sum != 0:
            prob = np.asarray(utilities)/utility_sum
            c = np.random.choice(np.arange(0, len(utilities)), p=prob)
            return pool[c]
        
        return -1

    def nearest_door(self, doors):
        """Returns the nearest door to the passenger"""
        nearest = 0
        min_d = 10000000

        for i, d in enumerate(doors):
            dist = (d[0] - self.x)**2
            if dist < min_d:
                min_d = dist
                nearest = i
        return doors[nearest]

    def to_phase_zero(self):
        """Resets the passenger who to phase 0 to reselect a seat or standing area."""
        if self.seat == None or self.phase in (-1, 3, 4):
            return

        if self.seat.occupied:
            self.seat = None
            self.adj_occupied = []
            self.phase = 0
        
        elif self.adj_occupied != [s.occupied for s in self.seat.adjacent]:
            self.seat = None
            self.adj_occupied = []
            self.phase = 0

    def remove(self):
        """When used, the passenger will begin to exit the environment"""
        try:
            self.seat.occupied = False
            self.seat = None
        except:
            pass

        self.adj_occupied = []
        self.phase = 6
        self.dy = self.ymax/2

        if self.x < self.min_standing_x + 0.2:
            self.dx = self.min_standing_x + 0.2
        else:
            self.dx =self.x
        