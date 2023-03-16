"""Environment creation"""

import numpy as np

from scenario.seat import Seat
from scenario.spot import Spot

class Environment:
    """Class for environment creation."""
    def __init__(self):
        self.default_seat_dimensions = (0.4, 0.4)
        self.seat_distance = 0.247
        self.aisle_width = 0.5
        self.dimensions = None

        self.min_standing_x = 100
        self.seat_list = []
        self.standing_spots = []
        self.doors = []
        self.walls = []
        self.standing_boundaries = []
        self.obstacle_objects = []
        
        self.created = False

    def seat(self, x, y, rotation=0, size=None):
        """Creates and stores a seat."""
        if not size:
            size = self.default_seat_dimensions
        
        self.seat_list.append(Seat(x, y, self.dimensions[1], rotation=rotation, dimensions=size))

    def seat_row(self, x, y, number, rotation=0, size=None):
        """Stores a row of seats in the x axis leaving space between them equal to seat_distance."""
        for i in range(number):
            self.seat(x + i * (self.default_seat_dimensions[1] + self.seat_distance), y, rotation, size)

    def seat_column(self, x, y, number, rotation=0, size=None):
        """Stores a column of seats in the y axis leaving space between them equal to 0."""
        for i in range(number):
            self.seat(x, y + i * (self.default_seat_dimensions[1]), rotation, size)

    def set_dimensions(self, length, width):
        """Sets the environment's dimensions."""
        self.dimensions = (length, width)

    def door(self, x, width=1.25):
        """Appends a tuple of the x coordinate and the width of a door in a list.
        The y coordinate of all doors is considered equal to 0.
        """
        self.doors.append((x, width))

    def standing_spot(self, *args):
        """Appends a standing spot in a list."""
        for spot in args:
            self.standing_spots.append(Spot(spot[0], spot[1]))

    def obstacle_line(self, xy0, xy1, standing=False):
        """Stores an obstacle line.
        If the standing argument is equal to 0 it is treated it as a wall
        otherwise it is treated as a standing area boundary.
        """
        x0 = xy0[0]
        y0 = xy0[1]
        x1 = xy1[0]
        y1 = xy1[1]
        length = np.sqrt((y0 - y1) ** 2 + (x0 - x1) ** 2)

        if abs(x0 - x1) < .01:
            d = np.array([(x0, y) for y in np.linspace(y0, y1, int(abs(y1-y0)*13))])
        else:
            m = (y1 - y0)/(x1 - x0)  
            d = np.array([(x, m*(x - x0) + y0) for x in np.linspace(x0, x1, int(length*13))])
        if standing:
            self.min_standing_x = min(self.min_standing_x, x0)
            self.min_standing_x = min(self.min_standing_x, x1)
            self.standing_boundaries.append(d)
        else:
            self.walls.append(d)
            
    def obstacle_polyline(self, *args, standing=False):
        """Creates an obstacle polyline.
        If the standing argument is equal to 0 it is treated as a wall
        otherwise it is treated as a standing area boundary.
        """
        n_points = len(args)
        for i in range(n_points):
            if i < n_points-1:
                self.obstacle_line(args[i], args[i+1], standing)

    def obstacle_object(self, *args, hatch=None, linewidth=1, fc='gray', ec='k', closed=True):
        """Stores an obstacle object which can be displayed with matplotlib."""
        self.obstacle_polyline(*args)
        kwargs = {'hatch': hatch, 'linewidth': linewidth, 'fc': fc, 'ec': ec, 'closed': closed}
        self.obstacle_objects.append({'xy': [*args], 'kwargs': kwargs})

    def create_walls(self):
        """Adds walls based on the seats the doors and the boundary data of the environment."""
        if self.created:
            return self.walls
        
        for seat in self.seat_list:
            theta = seat.rotation*np.pi/180
            seat_x = seat.x
            seat_y = seat.y
            l1 = seat.dimensions[0]/2
            l2 = seat.dimensions[1]/2 - 0.1
            x0 = np.cos(theta)*(-l1) - np.sin(theta)*(-l2) + seat_x
            y0 = np.sin(theta)*(-l1) + np.cos(theta)*(-l2) + seat_y
            x1 = np.cos(theta)*(-l1) - np.sin(theta)*l2 + seat_x
            y1 = np.sin(theta)*(-l1) + np.cos(theta)*l2 + seat_y

            self.obstacle_line((x0, y0), (x1, y1))

        ndoors = len(self.doors)
        x2 = self.dimensions[0]
        y2 = self.dimensions[1]
        firstdoor = self.doors[0]

        self.obstacle_line((-1.5, 0), (firstdoor[0]-firstdoor[1]/2, 0))

        for i in range(ndoors):
            if i == ndoors -1:
                start = self.doors[i][0] + self.doors[i][1]/2
                end = x2 + 2
            else:
                start = self.doors[i][0] + self.doors[i][1]/2
                end = self.doors[i+1][0] - self.doors[i+1][1]/2

            self.obstacle_line((start, 0), (end, 0))

        self.obstacle_line((0, y2), (x2, y2))
        self.obstacle_line((0, 0), (0, y2))
        self.obstacle_line((x2, 0), (x2, y2))
        self.created = True

        return self.walls
