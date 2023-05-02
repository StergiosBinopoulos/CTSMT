#include "transmission.h"

#include <cmath>
#include <algorithm>

#include "../scenario/parameters.h"
#include "../scenario/passenger.h"


using std::vector;
using std::min;
using std::max;


Transmission::Transmission() {
    dt = DELTA_T;
    tf = TF;
}

double Transmission::probability_of_infection(double pd, double t, double P) {
    return 1 - exp(-((pd * tf*t) - log(1-P)));
}

double Transmission::pd_func(double distance) {
    double x = distance > 0.05? distance: 0.05;
    double pd = (ALPHA * log(x) + BETA) / 100;
    return min(max(pd, 0.), 1.);
}

void Transmission::step(Passenger &passenger, vector<Passenger> &passengers) {
    if (std::abs(passenger.inf - 2) < 0.1)
        return;

    double pd_sum = 0;

    for (auto other_passenger : passengers) {
        if (std::abs(other_passenger.inf - 2) > 0.1)
            continue;

        double distance = sqrt(pow(passenger.x - other_passenger.x, 2) +
            pow(passenger.y - other_passenger.y, 2));

        double pd = pd_func(distance);
        pd_sum += pd;
    }

    double prob_i = passenger.prob;
    double prob_i_plus_1 = probability_of_infection(pd_sum, dt, prob_i);
    prob_i_plus_1 = prob_i_plus_1 < 0? 0: prob_i_plus_1;
    passenger.prob = prob_i_plus_1;

    if (passenger.prob > passenger.inf_at_prob)
        passenger.inf = 1;
}
