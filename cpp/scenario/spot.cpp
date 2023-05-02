#include "spot.h"

#include <cmath>


Spot::Spot(double spot_x, double spot_y) {
    x = spot_x;
    y = spot_y;
}

double Spot::utility(double px) {
    double distance = std::abs(x - px);
    return exp(-0.5*pow(distance/2, 2));
}
