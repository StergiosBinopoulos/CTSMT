#ifndef SCENARIO_SPOT_H_
#define SCENARIO_SPOT_H_

class Spot {
    public:
        double x;
        double y;

        Spot(double spot_x, double spot_y);

        double utility(double px);
};

#endif  // SCENARIO_SPOT_H_

