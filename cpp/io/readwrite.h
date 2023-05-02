#ifndef IO_READER_H_
#define IO_READER_H_

#include <map>
#include <string>
#include <vector>

#include "../scenario/seat.h"
#include "../scenario/spot.h"
#include "../scenario/passenger.h"
#include "../scenario/action.h"


std::map<string, double> read_parameters();


void read_conditions(double &width,
                     double &length,
                     double &aisle_width,
                     double &min_standing_x,
                     vector<Seat> &seats,
                     vector<Spot> &spots,
                     vector<vector<double>> &doors,
                     vector<vector<double>> &walls,
                     vector<vector<double>> &door_walls,
                     vector<vector<double>> &standing_bounds);

void write_states(vector<vector<vector<double>>> states);

void read_actions(int &duration, vector<Action> &actions);


#endif  // IO_READER_H_
