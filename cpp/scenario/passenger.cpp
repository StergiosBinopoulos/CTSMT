#include "passenger.h"

#include <vector>
#include <random>

#include "parameters.h"
#include "seat.h"
#include "../utils/utils.h"


using std::vector;


int Passenger::newuid = 0;


Passenger::Passenger(double passenger_x,
                     double passenger_y,
                     double passenger_dx,
                     double passenger_dy,
                     int initial_phase,
                     bool initial_infection,
                     double passenger_tau,
                     double speed) {
    desired_speed = (speed <= 0) ? normal_dist_rand(SPEED, SPEED_STD) : speed;

    seat_selection_prob = SEAT_SELECTION_PROB;
    rand = rand_double();

    inf_at_prob = rand_double();
    
    uid = newuid++;

    x = passenger_x;
    y = passenger_y;
    dx = passenger_dx;
    dy = passenger_dy;
    vx = 0;
    vy = 0;

    new_x = x;
    new_y = y;
    new_vx = vx;
    new_vy = vy;

    prob = 0;
    tau = passenger_tau;
    inf = (int)(initial_infection*2);
    phase = initial_phase;
    seat = nullptr;

    step = 1;

    patience = abs((int)normal_dist_rand(PATIENCE, PATIENCE_STD));

    initialized = false;
    stabilized = false;
}

bool Passenger::is_inside(double x0, double y0, double x1, double y1) {
    return (x1 > x) && (x > x0) && (y1 > y) && (y > y0);
}

void Passenger::phase_update(Environment *environment) {
    double aisle_width = environment->aisle_width;
    double xmax = environment->length;
    double ymax = environment->width;
    double Y0 = ymax/2 - aisle_width/2;
    double Y1 = ymax/2 + aisle_width/2;
    double min_standing_x = environment->min_standing_x;
    vector<vector<double>> doors = environment->doors;

    // update movements
    x = new_x;
    y = new_y;
    vx = new_vx;
    vy = new_vy;
    
    step += 1;
    if (phase == -1) {
        stabilized = true;
        return;
    }

    if (phase == 6) {
        if ((Y0 < y) && (y < Y1) && x > min_standing_x + 0.2) {
            vector<double> nearest = nearest_door(doors);
            dx = nearest[0];
            phase = 7;
        }
    
    } else if (phase == 7) {
        if ((Y0 < y) && (y < Y1)) {
            vector<double> nearest = nearest_door(doors);
            dx = nearest[0];
        }

        if (is_inside(dx - 0.5, Y0, dx + 0.5, Y1))
            dy = - 0.5;
        
        if (is_inside(dx - 0.4, 0, dx + 0.5, 0.4))
            phase = 8;
    
    } else if (phase == 8) {
        if (x < dx - 0.6 || x > dx + 0.6)
            phase = 7;

        if (y < 0) {
            environment->door_timeout = 0;
            dy = - 10;
        }

        if (y < -2)
            phase = 9;
    
    } else if (phase == 5) {
        if (step % patience == 0)
            seat_selection(environment);
    }

    to_phase_zero();

    if (phase == 3) {
        if (is_inside(dx - 0.05, dy - 0.05, dx + 0.05, dy + 0.05))
            phase = 4;
    
    } else if (phase == 2) {
        // if stuck reset phase
        if (!((Y0 < y) && (y < Y1))) {
            seat = nullptr;
            adj_occupied.clear();
            phase = 0;
            bool_vals_update();
            return;
        }

        if (is_inside(dx - 0.6, dy - 2, dx + 0.6, dy + 2)) {
            dx = seat->x;
            dy = seat->y;
            seat->occupied = true;
            phase = 3;
        }
    
    } else if (phase == 1) {
        if ((Y0 < y) && (y < Y1)) {
            dx = seat->x + 0.3 * cos(seat->r * M_PI / 180);
            dy = ymax / 2;
            phase = 2;
        }

    } else if (phase == 0) {
        if (!initialized) {
            vector<double> nearest = nearest_door(doors);
            dx = nearest[0];
            dy = ymax / 2;
            initialized = true;
        }

        if (is_inside(0, 0.1, xmax, ymax)) {
            initialized = false;
            seat_selection(environment);
            environment->door_timeout = 0;
        }
    }

    bool_vals_update();
}

void Passenger::bool_vals_update() {
    if (step%100 == 0 && step > 0) {
        if (phase == 4)
            stabilized = true;
        
        if (std::abs(past_y-y) < 0.2 && std::abs(past_x-x) < 0.2 &&
            (std::abs(vx)+std::abs(vy)) < 0.3*desired_speed)
            stabilized = true;

        past_x = x;
        past_y = y;
    }

    entering = phase == 0;
    exiting = phase == 7 || phase == 8;
    standing = phase == 5;
    walkspace = phase == 1 || phase == 2 || phase == 7 || phase == 5;
    seated = phase == 3 || phase == 4 || phase == 6;
}

void Passenger::seat_selection(Environment *environment) {
    if (seat_selection_prob > rand) {
        vector<double> utilities;
        double utility;
        vector<Seat*> pool;

        for (auto &s : environment->seats) {
            utility = s.utility(x);
            if (utility > 0) {
                utilities.push_back(utility);
                pool.push_back(&s);
            }
        }

        double utility_sum = 0;
        for (auto &util : utilities)
            utility_sum += util;

        if (utility_sum > 0) {
            double sum = 0;
            int cursor = -1;

            while (sum <= rand_double()*utility_sum) {
                cursor++;
                sum += utilities[cursor];
            }

            seat = pool[cursor];

            vector<bool> new_adj_occupied;
            for (auto s : seat->adjacent)
                new_adj_occupied.push_back(s->occupied);

            adj_occupied = new_adj_occupied;
            phase = 1;
            return;
        }
    }

    if (phase != 5) {
        vector<double> utilities;
        vector<Spot> pool;
        double utility;

        for (auto s : environment->spots) {
            utility = s.utility(x);
            if (utility > 0) {
                utilities.push_back(utility);
                pool.push_back(s);
            }
        }

        double utility_sum = 0;
        for (auto& util : utilities)
            utility_sum += util;

        if (utility_sum > 0) {
            double sum = 0;
            double cursor = -1;

            while (sum <= rand_double()*utility_sum) {
                cursor++;
                sum += utilities[cursor];
            }

            dx = pool[cursor].x;
            dy = pool[cursor].y;
            phase = 5;
            return;
        }
    }
}

vector<double> Passenger::nearest_door(vector<vector<double>> doors) {
    int nearest = 0;
    int min_d = 10000000;

    for (int i = 0; i != doors.size(); i++) {
        double dist = pow((doors[i][0] - x), 2);
        if (dist < min_d) {
            min_d = dist;
            nearest = i;
        }
    }
    return doors[nearest];
}

void Passenger::to_phase_zero() {
    if (seat == nullptr || (phase == -1 || phase == 3 || phase == 4))
        return;

    if (seat->occupied) {
        seat = nullptr;
        adj_occupied.clear();
        phase = 0;
        return;
    }

    vector<bool> new_adj_occupied;
    for (auto s : seat->adjacent)
        new_adj_occupied.push_back(s->occupied);

    if (adj_occupied != new_adj_occupied) {
        seat = nullptr;
        adj_occupied.clear();
        phase = 0;
        return;
    }
}

void Passenger::remove(Environment *environment) {
    stabilized = false;

    if (seat != nullptr) {
        seat->occupied = false;
        seat = nullptr;
    }

    phase = 6;
    dy = environment->width/2;
    
    if (x < environment->min_standing_x + 0.2)
        dx = environment->min_standing_x + 0.2;
    else
        dx = x;
}

int Passenger::get_uid() {
    return uid;
}
