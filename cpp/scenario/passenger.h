#ifndef SCENARIO_PASSENGER_H_
#define SCENARIO_PASSENGER_H_

#include <vector>

#include "parameters.h"
#include "seat.h"
#include "spot.h"
#include "environment.h"


using std::vector;


class Passenger {
    private:
        static int newuid;
        int uid;

        double seat_selection_prob;
        double rand;

        vector<double> nearest_door(vector<vector<double>> doors);

        void bool_vals_update();

    public:
        double desired_speed;
        double x;
        double y;
        double dx;
        double dy;
        double vx;
        double vy;

        bool entering;
        bool exiting;
        bool standing;
        bool walkspace;
        bool seated;
        bool stabilized;
        double past_x;
        double past_y;
        
        double prob;
        double inf_at_prob;

        double tau;

        double new_x;
        double new_y;
        double new_vx;
        double new_vy;
        
        int inf;
        int phase;
        int step;
        int patience;
        
        bool initialized;
        
        Seat* seat;
        vector<bool> adj_occupied;

        Passenger(double passenger_x,
            double passenger_y,
            double passenger_dx,
            double passenger_dy,
            int initial_phase=-1,
            bool initial_infection=false,
            double passenger_tau=TAU,
            double speed=0);

        bool is_inside(double x0, double y0, double x1, double y1);

        void phase_update(Environment *environment);

        void seat_selection(Environment *environment);

        void to_phase_zero();

        void remove(Environment *environment);

        int get_uid();
};


#endif  // SCENARIO_PASSENGER_H_
