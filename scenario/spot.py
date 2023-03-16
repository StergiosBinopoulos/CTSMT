import numpy as np

class Spot:
    """Class for standing spots."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def utility(self, x):
        """Calculates the utility of the spot"""
        distance = abs(self.x - x)
        return np.e ** (-0.5 * (distance / 2) ** 2)

