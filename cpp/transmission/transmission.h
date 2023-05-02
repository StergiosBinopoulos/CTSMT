#ifndef TRANSMISSION_TRANSMISSION_H_
#define TRANSMISSION_TRANSMISSION_H_

#include <vector>

#include "../scenario/passenger.h"


using std::vector;


class Transmission {
    private:
        double dt;
        double tf;

        double probability_of_infection(double pd, double t, double P);

        double pd_func(double distance);

    public:
        Transmission();

        void step(Passenger &passenger, vector<Passenger> &passengers);
};


#endif  // TRANSMISSION_TRANSMISSION_H_
