"""Transmission model based on a modified Wells-Riley model."""

import numpy as np

from parameters import *


class TransmissionSimulation:
    """Every pedestrian is an entry in the state and
    represented by a vector (x, y, p, i).
    i: 0 for susceptible 1 for infected 2 for source case
    p: probability of infection
    """
    def __init__(self, initial_state, inf_probs, delta_t=1, q=None, Q=None, p=None, c=None):
        self.delta_t = delta_t
        self.state = initial_state

        # the probability at which a passenger will get infected
        self.inf_probs = inf_probs
        
        # either specify all the parameters (q, Q and p) or c which is the combination of them
        self.c = c
        if not self.c and self.c != 0:
            self.c = p * q / Q

    def probability_of_infection(self, pd, t, prob):
        """Compute the probability of infection."""
        return 1 - np.exp(-((pd * self.c*t) - np.log(1-prob)))

    @staticmethod
    def pd_func(distance):
        """Compute the Pd (social distance index)."""
        x = np.where(distance > 0.05, distance, 0.05)
        pd = (ALPHA * np.log(x) + BETA) / 100
        np.clip(pd, 0, 1)
        return pd

    def step(self):
        """Do one step in the simulation and update the state in place."""
        source_cases_id = self.state[:, 3]==2.
        source_cases_xy = self.state[source_cases_id][:, :2]
        all_xy = self.state[:, :2]

        # shape of r: (number of passengers, number of index cases, 2)
        # r represents the x and y distance of each source case from other passengers in the environment
        r = np.expand_dims(all_xy, 1) - np.expand_dims(source_cases_xy, 0)
        distance_from_source_cases = np.linalg.norm(r, axis=-1)
        pd = self.pd_func(distance_from_source_cases)

        pd_sum = np.sum(pd, axis=-1)

        # update the probability based on the previous one
        prob_i = self.state[:, 2]
        prob_i_plus_1 = self.probability_of_infection(pd_sum, self.delta_t, prob_i)
        prob_i_plus_1[prob_i_plus_1 < 0] = 0

        # update state
        self.state[:, 2] = prob_i_plus_1
        self.state[:, 2][source_cases_id] = 0

        # calculate if anyone gets infected during the time step
        b = self.state[:, 2] > self.inf_probs
        self.state[:, 3] = np.where(np.logical_and(b, self.state[:, 3]==0.), 1., self.state[:, 3])

        return self
        