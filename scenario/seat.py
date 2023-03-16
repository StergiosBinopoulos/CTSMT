import numpy as np

from parameters import *

class Seat:
    """Class for seats."""
    def __init__(self, x, y, ymax, rotation=0, dimensions=(0.4, 0.4)):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.dimensions = dimensions
        self.occupied = False
        self.upper_seat = None
        self.lower_seat = None
        self.right_seat = None
        self.left_seat = None
        self.adjacent = []
        self.window = self.y < 0.6 or ymax - self.y < 0.6

    def adjacent_seats(self, seat_list):
        """Finds adjacent seats from a list of seats"""
        for seat in seat_list:
            if self == seat:
                continue

            dy = seat.y - self.y
            dx = seat.x - self.x

            if abs(dx) < 0.3:
                if 0 < dy < 0.6:
                    self.upper_seat = seat
                elif 0 > dy > -0.6:
                    self.lower_seat = seat

            if abs(dy) < 0.3:
                if 0 < dx < 0.6:
                    self.right_seat = seat
                elif 0 > dx > -0.6:
                    self.left_seat = seat

        if self.rotation in (0, 180):
            if self.upper_seat:
                self.adjacent.append(self.upper_seat)
            if self.lower_seat:
                self.adjacent.append(self.lower_seat)

        if self.rotation in (90, 270):
            if self.right_seat:
                self.adjacent.append(self.right_seat)
            if self.left_seat:
                self.adjacent.append(self.left_seat)

    def utility(self, x):
        """Calculates the utility of a seat"""
        if self.occupied:
            return 0

        distance = abs(self.x - x)
        if distance > 5:
            return 0

        adj_par = 1
        for seat in self.adjacent:
            if seat.occupied:
                adj_par = MADJ

        window_par = (MW if self.window else 1)
        base_util = np.e ** (-0.5 * (distance / 1.5) ** 2)
        util = window_par * adj_par * base_util
        return util
