#ifndef SCENARIO_ENVIRONMENT_H_
#define SCENARIO_ENVIRONMENT_H_

#include <vector>

#include "parameters.h"
#include "seat.h"
#include "spot.h"


class Environment {
    public:
        double width;
        double length;
        double aisle_width;
        double min_standing_x;
        bool opened_doors = false;
        int door_counter;
        int door_timeout;
        vector<Seat> seats;
        vector<Spot> spots;
        vector<vector<double>> doors;
        vector<vector<double>> walls;
        vector<vector<double>> door_walls;
        vector<vector<double>> walls_doors_closed;
        vector<vector<double>> standing_bounds;

        Environment(double env_width,
            double env_length,
            double env_aisle_width,
            double env_min_standing_x,
            vector<Seat> env_seats,
            vector<Spot> env_spots,
            vector<vector<double>> env_doors,
            vector<vector<double>> env_walls,
            vector<vector<double>> env_door_walls,
            vector<vector<double>> env_standing_bounds);   
};


#endif  // SCENARIO_ENVIRONMENT_H_
