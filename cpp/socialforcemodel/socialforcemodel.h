#ifndef SOCIALFORCEMODEL_SOCIALFORCEMODEL_H_
#define SOCIALFORCEMODEL_SOCIALFORCEMODEL_H_

#include <vector>

#include "../scenario/passenger.h"


using std::vector;


class SocialForceModel {
    private:
        double dt;

        double norm(vector<double> vec);

        double in_sight(vector<double> e, vector<double> f);

        double g_a(double umax, double wa);

        vector<double> find_nearest_wall(const Passenger &passenger,
                const vector<vector<double>> &candidates);

        vector<double> F0_a(vector<double> e, vector<double> u, double u0,
                double tau);
        
        vector<double> e_a(Passenger passenger);

        vector<double> f_ab(Passenger passenger_a, Passenger passenger_b,
                double V_ab0, double sigma);

        double value_r_ab(Passenger passenger_a, Passenger passenger_b,
                double V_ab0, double sigma, double delta_x=0, double delta_y=0);

        vector<double> f_aB(Passenger passenger, vector<double> obstacle,
                double U_aB0, double R);
        
        double value_r_aB(Passenger passenger, vector<double> obstacle,
                double U_aB0, double R, double delta_x=0, double delta_y=0);

    public:
        SocialForceModel();

        void step(Passenger &passenger, vector<Passenger> &passengers,
                const vector<vector<double>> &walls,
                const vector<vector<double>> &standing_bounds);
};


#endif  // SOCIALFORCEMODEL_SOCIALFORCEMODEL_H_
