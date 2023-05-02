#include "parameters.h"

#include <string>
#include <map>

#include "../io/readwrite.h"


std::map<std::string, double> parameters = read_parameters();


extern const double DELTA_T = parameters["DELTA_T"];
extern const double DOOR_TIMEOUT = parameters["DOOR_TIMEOUT"];
extern const double MIN_DOOR_TIME = parameters["MIN_DOOR_TIME"];
extern const double DOOR_OPEN_DELAY = parameters["DOOR_OPEN_DELAY"];
extern const double SEAT_SELECTION_PROB = parameters["SEAT_SELECTION_PROB"];
extern const double SPEED = parameters["SPEED"];
extern const double SPEED_STD = parameters["SPEED_STD"];

extern const double PATIENCE = parameters["PATIENCE"];
extern const double PATIENCE_STD = parameters["PATIENCE_STD"];

extern const double MAX_SPEED_MULTIPLIER = parameters["MAX_SPEED_MULTIPLIER"];
extern const double TWOPHI = parameters["TWOPHI"];
extern const double C = parameters["C"];
extern const double TAU = parameters["TAU"];

extern const double V0 = parameters["V0"];
extern const double PEDPED_SIGMA = parameters["PEDPED_SIGMA"];

extern const double U0_E = parameters["U0_E"];
extern const double R_E = parameters["R_E"];

extern const double U0_SB = parameters["U0_SB"];
extern const double R_SB = parameters["R_SB"];

extern const double AFM_ENT = parameters["AFM_ENT"];
extern const double AFM_EXIT = parameters["AFM_EXIT"];
extern const double AFM_STAND = parameters["AFM_STAND"];

extern const double ALPHA = parameters["ALPHA"];
extern const double BETA = parameters["BETA"];

extern const double TF = parameters["TF"];

extern const double MADJ = parameters["MADJ"];
extern const double MW = parameters["MW"];
extern const double SIGMA_SEAT = parameters["SIGMA_SEAT"];
extern const double MAX_DIST = parameters["MAX_DIST"];

extern const double SIGMA_SPOT = parameters["SIGMA_SPOT"];
