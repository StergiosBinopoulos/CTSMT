#include "scenario.h"

#include <random>
#include <algorithm>
#include <iostream>

#include "action.h"
#include "../utils/utils.h"
#include "../io/readwrite.h"


using std::cout;
using std::endl;


Scenario::Scenario() {   
    double width;
    double length;
    double aisle_width;
    double min_standing_x;
    vector<Seat> seats;
    vector<Spot> spots;
    vector<vector<double>> doors;
    vector<vector<double>> walls;
    vector<vector<double>> door_walls;
    vector<vector<double>> standing_bounds;

    read_conditions(
        width,
        length,
        aisle_width,
        min_standing_x,
        seats,
        spots,
        doors,
        walls,
        door_walls,
        standing_bounds);

    environment = new Environment(
        width,
        length,
        aisle_width,
        min_standing_x,
        seats,
        spots,
        doors,
        walls,
        door_walls,
        standing_bounds);

    read_actions(duration, actions);
}

Scenario::~Scenario() {
    delete environment;
}

void Scenario::add_passenger(double x, double y, double dx, double dy, 
        int phase, bool inf) {
    //  dx, dy can't be = x, y (math error)
    if ((dx == x) && (dy == y)) {
        dx = x - 0.01;
        dy = y - 0.01;
    }
    passengers.push_back(Passenger(x, y, dx, dy, phase, inf));
}

vector<int> Scenario::door_selection(vector<double> doors_prob, int n_in) {
    // Probabilistically distributes passengers to the available doors.
    vector<int> count(doors_prob.size(), 0);

    for (int i = 0; i != n_in; i++) {
        double cursor = -1;
        double sum = 0;
        while (sum <= rand_double()) {
            cursor++;
            sum += doors_prob[cursor];
        }

        count[cursor]++;
    }

    return count;
}

void Scenario::spawn_passengers(int n_in, int n_source, 
        vector<double> doors_prob) {
    vector<int> choices = door_selection(doors_prob, n_in);
    vector<int> source_id = rand_sample(0, n_in-1, n_source);

    open = true;

    int id_ = 0;
    for (long unsigned int i = 0; i != choices.size(); i++) {
        double door_x = environment->doors[i][0];
        for (int j = 0; j != choices[i]; j++) {
            double x = 2*(rand_double()-0.5) + door_x;
            double y = -0.2 + rand_double() * -2;
            double dy = environment->width/2;
            double dx = door_x;
            
            bool inf = std::count(source_id.begin(), 
                source_id.end(), id_) == 1? true: false;

            passengers.push_back(Passenger(x, y, dx, dy, 0, inf));
            id_++;  
        }
    }
}

void Scenario::remove_passenger(int i) {
    passengers.erase(passengers.begin()+i);
}

void Scenario::remove_passengers(int n) {   
    vector<Passenger*> viable;
    for (auto &p : passengers) {
        if (!p.exiting)
            viable.push_back(&p);
    }

    if (n > viable.size()) {
        cout << "remove_passengers: Not enough passengers to remove" << endl;
        cout << "removing " << viable.size() << " passengers instead of ";
        cout << n << endl;
        n = viable.size();
    }

    vector<int> sample = rand_sample(0, viable.size()-1, n);

    for (int i : sample) {
        viable[i]->remove(environment);   
    }
}

void Scenario::open_doors() {
    open = true;

    for (auto &passenger : passengers)
        passenger.stabilized = false;

    environment->door_counter = 0;
    environment->door_timeout = 0;
}

void Scenario::execute_actions() {
    for (auto action : actions) {
        if (frame == action.frame) {
            if (action.name == "passenger") {
                passengers.push_back(Passenger(
                        action.num_args[0],
                        action.num_args[1],
                        action.num_args[2],
                        action.num_args[3],
                        (int)action.num_args[4],
                        (bool)action.num_args[5]));
            }

            if (action.name == "spawn") {
                spawn_passengers(
                    action.num_args[0],
                    action.num_args[1],
                    action.list_args[0]);
            }

            if (action.name == "remove") {
                remove_passengers(action.num_args[0]);
            }

            if (action.name == "open_doors") {
                open_doors();
            }
        }
    }
}

void Scenario::update_doors() {
    // Updates the state of the doors (opens or closes as needed)
    // Open the doors if the doors are scheduled to be opened
    if (open) {
        environment->door_counter++;
        if (environment->door_counter >= (int)(DOOR_OPEN_DELAY/DELTA_T)) {
            environment->opened_doors = true;
            environment->door_counter = 0;
            open = false;
        }
    }

    //  If already open, close
    if (environment->opened_doors) {
        // when passengers enter/exit the environment they value to 0
        environment->door_timeout++;

        environment->door_counter++;
        if (environment->door_timeout >= (int)(DOOR_TIMEOUT/DELTA_T) &&
                environment->door_counter >= (int)(MIN_DOOR_TIME/DELTA_T)) {
            environment->opened_doors = false;
            environment->door_timeout = 0;
            environment->door_counter = 0;

            for (long unsigned int i = 0; i != passengers.size(); i++) {
                double l = environment->length;
                double w = environment->width;
                if (!passengers[i].is_inside(0, 0, l, w))
                    passengers.erase(passengers.begin()+i);
            }
        }
    }
}

bool Scenario::stability() {
    bool all_stabilized = true;
    for (auto &passenger : passengers)
        all_stabilized = all_stabilized && passenger.stabilized;
    
    return all_stabilized;
}

void Scenario::step() {
    execute_actions();
    update_doors();

    vector<vector<double>> state_i;
    int i = 0;


    stabilized = stability();

    for (auto &passenger : passengers) {
        state_i.push_back({passenger.x, passenger.y, passenger.prob, 
            (double)passenger.inf});

        if (!stabilized && passenger.phase != -1) {
            if (environment->opened_doors)
                sfm.step(
                    passenger, 
                    passengers, 
                    environment->walls, 
                    environment->standing_bounds);
            else
                sfm.step(
                    passenger, 
                    passengers, 
                    environment->walls_doors_closed, 
                    environment->standing_bounds);
        }

        tsm.step(passenger, passengers);

        if (!stabilized)
            passenger.phase_update(environment);

        // delete passengers who have exited the vehicle
        if (passenger.phase == 9)
            passengers.erase(passengers.begin()+i);

        i++;
    }

    states.push_back(state_i);
    frame++;
}

void Scenario::simulate() {
    while (duration >= frame)
        step();
}
