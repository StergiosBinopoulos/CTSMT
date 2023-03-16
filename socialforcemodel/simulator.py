"""Synthetic pedestrian behavior according to the Social Force model.
See Helbing and Molnár 1998.
"""

import numpy as np
from socialforcemodel.potentials import PedPedPotential
from socialforcemodel.fieldofview import FieldOfView
import socialforcemodel.stateutils as stateutils

from parameters import *


class Simulator(object):
    """Simulate social force model.
    Main interface is the state. Every pedestrian is an entry in the state and
    represented by a vector (x, y, v_x, v_y, d_x, d_y, [tau]).
    tau is optional in this vector.
    ped_space is an instance of PedSpacePotential.
    ped_ped is an instance of PedPedPotential.
    delta_t in seconds.
    tau in seconds: either float or numpy array of shape[n_ped].
    """
    def __init__(self, initial_state, ped_space=None, ped_ped=None, ped_walkspace=None,
                 field_of_view=None, delta_t=0.05, tau=0.5):
        self.state = initial_state
        self.initial_speeds = stateutils.speeds(initial_state)
        self.max_speeds = MAX_SPEED_MULTIPLIER * self.initial_speeds

        self.delta_t = delta_t

        if self.state.shape[1] < 7:
            if not hasattr(tau, 'shape'):
                tau = tau * np.ones(self.state.shape[0])
            self.state = np.concatenate((self.state, np.expand_dims(tau, -1)), axis=-1)

        # potentials
        self.V = ped_ped or PedPedPotential(self.delta_t)
        self.U = ped_space
        self.U2 = ped_walkspace

        # field of views
        self.w = field_of_view or FieldOfView()

    def f_ab(self):
        """Compute f_ab."""
        return -1.0 * self.V.grad_r_ab(self.state)

    def f_aB(self, space):
        """Compute f_aB."""
        if self.U is None:
            return np.zeros((self.state.shape[0], 0, 2))
        return -1.0 * space.grad_r_aB(self.state)

    def capped_velocity(self, desired_velocity):
        """Scale down a desired velocity to its capped speed."""
        desired_speeds = np.linalg.norm(desired_velocity, axis=-1)
        factor = np.minimum(1.0, self.max_speeds / desired_speeds)
        factor[desired_speeds == 0] = 0.0
        return desired_velocity * np.expand_dims(factor, -1)

    def step(self):
        """Do one step in the simulation and update the state in place."""
        # accelerate to the desired velocity
        e = stateutils.desired_directions(self.state)
        vel = self.state[:, 2:4]
        tau = self.state[:, 6:7]
        F0 = 1.0 / tau * (np.expand_dims(self.initial_speeds, -1) * e - vel)

        # repulsive terms between pedestrians
        f_ab = self.f_ab()
        w = np.expand_dims(self.w(e, -f_ab), -1)
        F_ab = w * f_ab

        # repulsive terms between pedestrians and boundaries
        F_aB1 = self.f_aB(self.U)
        F_aB2 = self.f_aB(self.U2)

        # social force
        F = (F0*(1 - self.standing*(1-AFM_STAND))*(1 + self.entering*AFM_ENT)*(1 + self.exiting*AFM_EXIT)
             + np.sum(F_ab, axis=1) * ~self.seated
             + np.sum(F_aB1, axis=1) * ~self.seated
             + np.sum(F_aB2, axis=1) * self.walkspace )
        
        # desired velocity
        w = self.state[:, 2:4] + self.delta_t * F
        # velocity
        v = self.capped_velocity(w)

        # update state
        self.state[:, 0:2] += v * self.delta_t
        self.state[:, 2:4] = v

        return self

    def update_ped_space(self, space):
        """Updates the obstacles/walls."""
        self.U = space
    
    def update_state(self, state, speeds, phases):
        """Updates the destinations of pedestrians."""
        self.state = state

        self.walkspace = np.logical_or(phases == 1, phases == 2)
        self.walkspace = np.logical_or(self.walkspace, phases == 5)
        self.walkspace = np.logical_or(self.walkspace, phases == 7)

        self.seated = np.logical_or(phases == 3, phases == 4)
        self.seated = np.logical_or(self.seated, phases == 6)

        self.entering = phases == 0
        self.exiting = np.logical_or(phases == 8, phases == 7)


        self.standing = phases == 5

        self.initial_speeds = speeds
        self.max_speeds = MAX_SPEED_MULTIPLIER * self.initial_speeds
