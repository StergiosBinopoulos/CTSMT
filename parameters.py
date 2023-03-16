"""General"""
# The simulation step
DELTA_T = 0.1


"""Environment"""
# The door will close DOOR_TIMEOUT seconds after the last 
# person who entered or left the environment 
DOOR_TIMEOUT = 6
# The minimum time the door will remain open
MIN_DOOR_TIME = 10
# The time required to open the door after it is signaled to open
DOOR_OPEN_DELAY = 1.5


"""Passenger"""
# The probability to select a seat instead of a standing spot
SEAT_SELECTION_PROB = 0.75
# The average speed of each passenger (m/s)
SPEED = 0.65
# The standard deviation of passengers' speeds
SPEED_STD = 0.12

# Affects how often standing passengers will notice that a seat has been freed 
# Average passenger patience in seconds
PATIENCE = 50 
# The standard deviation of passengers' patience
PATIENCE_STD = 5


"""Crowd Simulation (See Helbing and Molnár 1998 (Social Force Model))"""
# Max speed = MAX_SPEED_MULTIPLIER * SPEED
MAX_SPEED_MULTIPLIER = 1.3
# Angle of Sight (degrees)
TWOPHI = 200
# Out of View factor
C = 0.5
# Relaxation Time
TAU = 0.5

# == Ped-Ped Potential ==

V0 = 1.3
PEDPED_SIGMA = 0.25

# == Environment Obstacles Potential ==

U0_E = 10
R_E = 0.05

# == Standing Boundaries Potential ==

U0_SB = 2
R_SB = 0.05

# == Additional Factors (Not Included in the original model) ==

# Used to help passengers enter/exit without getting stuck 
# Acceleration Force Multiplier for passengers entering the environment
AFM_ENT = 1.3
# Acceleration Force Multiplier for passengers exiting the environment
AFM_EXIT = 1.6
# Acceleration Force Multiplier for passengers standing
AFM_STAND = 0.4


"""Transmission Simulation"""
# Social Distance Index (Pd) 
# Logarithmic Regression Factors 
# (ALPHA * ln(x) + BETA)/100 where x is distance in meters
ALPHA = -22.8
BETA = 51.16

# Transmission factor (quantum/s)
TF = 1.61 * 10**-4


"""Seat Utility"""
# The utility of seats with passengers on the adjacent seats is multiplied by MADJ
MADJ = 0.5
# The utility of window seats is multiplied by MW 
MW = 3
# Larger SIGMA_SEAT results in larger utility scores for seats further away   
SIGMA_SEAT = 1
# Max selection distance (m)
MAX_DIST = 5


"""Standing Spot Utility"""
# A larger SIGMA_SPOT results in larger utility scores for further away spots  
SIGMA_SPOT = 2


