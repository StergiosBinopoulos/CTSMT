#ifndef SCENARIO_SCENARIO_H_
#define SCENARIO_SCENARIO_H_

#include <vector>

#include "seat.h"
#include "spot.h"
#include "passenger.h"
#include "environment.h"
#include "action.h"
#include "../socialforcemodel/socialforcemodel.h"
#include "../transmission/transmission.h"


using std::vector;


class Scenario {
    private:
        SocialForceModel sfm;
        Transmission tsm;
        Environment* environment;
        vector<Passenger> passengers;
        vector<Action> actions;
        
        int duration;
        int frame = 0;

        bool open = false;
        bool stabilized = false;

        vector<int> door_selection(vector<double> doors_prob, int n_in);

    public:
        vector<vector<vector<double>>> states;

        Scenario();

        ~Scenario();

        void add_passenger(double x, double y, double dx=0, double dy=0, 
            int phase=0, bool inf=false);

        void spawn_passengers(int n_in, int n_source, 
            vector<double> doors_prob);

        void remove_passenger(int i);

        void remove_passengers(int n);

        void open_doors();

        void update_doors();

        void step();

        bool stability();

        void execute_actions();
        
        void simulate();
};


#endif  // SCENARIO_SCENARIO_H_
