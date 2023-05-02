#include "socialforcemodel.h"

#include <cmath>
#include <vector>

#include "../scenario/parameters.h"
#include "../scenario/passenger.h"


using std::vector;


SocialForceModel::SocialForceModel() {
    dt = DELTA_T;
}

double SocialForceModel::norm(vector<double> vec) {
    double squared = 0;

    for (auto item : vec)
        squared += pow(item, 2);

    return sqrt(squared);
}

double SocialForceModel::in_sight(vector<double> e, vector<double> f) {
    double dot_product = e[0]*f[0] + e[1]*f[1];
    if (dot_product >= norm(f)*cos(TWOPHI*M_PI/360))
        return 1;

    return C;
}

double SocialForceModel::g_a(double umax, double wa) {
    if (wa <= umax)
        return 1;

    return umax/wa;
}

vector<double> SocialForceModel::find_nearest_wall(
        const Passenger &passenger,
        const vector<vector<double>> &candidates) {
    vector<double> nearest;
    double min = __DBL_MAX__;
    double current;
    for (auto &bound : candidates) {
        current = sqrt(pow(bound[0] - passenger.x, 2) +
            pow(bound[1] - passenger.y, 2));

        if (current < min) {
            nearest = bound;
            min = current;
        }
    }
    return nearest;
}

vector<double> SocialForceModel::F0_a(vector<double> e, vector<double> u,
                                      double u0, double tau) {
    vector<double> F = {0, 0};
    F[0] = 1/tau*(u0*e[0] - u[0]);
    F[1] = 1/tau*(u0*e[1] - u[1]);
    return F;
}

vector<double> SocialForceModel::e_a(Passenger passenger) {
    vector<double> E = {0, 0};
    double x = passenger.x;
    double y = passenger.y;
    double dx = passenger.dx;
    double dy = passenger.dy;

    vector<double> r_ak = {dx - x, dy - y};
    double length = norm(r_ak);
    E[0] = r_ak[0]/length;
    E[1] = r_ak[1]/length;

    return E;
}

vector<double> SocialForceModel::f_ab(Passenger passenger_a,
                                      Passenger passenger_b,
                                      double V_ab0,
                                      double sigma) {
    vector<double> F = {0, 0};
    double v =  value_r_ab(passenger_a, passenger_b, V_ab0, sigma);
    double v1 =  value_r_ab(passenger_a, passenger_b, V_ab0, sigma, 0.001, 0);
    double v2 =  value_r_ab(passenger_a, passenger_b, V_ab0, sigma, 0, 0.001);

    F[0] = -1 * (v1 - v) / 0.001;
    F[1] = -1 * (v2 - v) / 0.001;
    return F;
}

double SocialForceModel::value_r_ab(Passenger passenger_a,
                                    Passenger passenger_b,
                                    double V_ab0,
                                    double sigma,
                                    double delta_x,
                                    double delta_y) {
    double B;
    double x_a = passenger_a.x;
    double y_a = passenger_a.y;
    double x_b = passenger_b.x;
    double y_b = passenger_b.y;

    double ub = norm({passenger_b.vx, passenger_b.vy});

    vector<double> eb = e_a(passenger_b);
    vector<double> r_ab = {x_a - x_b + delta_x, y_a - y_b + delta_y};
    vector<double> vec2 = {0, 0};

    vec2[0] = r_ab[0] - ub*dt*eb[0];
    vec2[1] = r_ab[1] - ub*dt*eb[1];

    B = sqrt(pow(norm(r_ab) + norm(vec2), 2) - pow(dt*ub, 2))/2;

    double Vab = V_ab0*exp(-B/sigma);


    return Vab;
}

vector<double> SocialForceModel::f_aB(Passenger passenger,
                                      vector<double> obstacle,
                                      double U_aB0, 
                                      double R) {
    vector<double> F = {0, 0};
    double v =  value_r_aB(passenger, obstacle, U_aB0, R);
    double v1 =  value_r_aB(passenger, obstacle, U_aB0, R, 0.001, 0);
    double v2 =  value_r_aB(passenger, obstacle, U_aB0, R, 0, 0.001);

    F[0] = -1 * (v1 - v) / 0.001;
    F[1] = -1 * (v2 - v) / 0.001;

    return F;
}

double SocialForceModel::value_r_aB(Passenger passenger,
                                    vector<double> obstacle, 
                                    double U_aB0, 
                                    double R, 
                                    double delta_x, 
                                    double delta_y) {
    double x_a = passenger.x;
    double y_a = passenger.y;
    double x_B = obstacle[0];
    double y_B = obstacle[1];

    vector<double> r_aB = {x_a - x_B + delta_x, y_a - y_B + delta_y};

    double UaB = U_aB0*exp(-norm(r_aB)/R);

    return UaB;
}

void SocialForceModel::step(Passenger &passenger,
                            vector<Passenger> &passengers,
                            const vector<vector<double>> &walls,
                            const vector<vector<double>> &standing_bounds) {
    vector<double> e = e_a(passenger);
    vector<double> u = {passenger.vx, passenger.vy};
    double tau_a = passenger.tau;
    double u0 = passenger.desired_speed;

    // accelerate to the desired velocity
    double f0_factor = (1 - passenger.standing*(1-AFM_STAND))*
        (1 + passenger.entering*AFM_ENT)*(1 + passenger.exiting*AFM_EXIT);

    vector<double> F = F0_a(e, u, u0, tau_a);
    F[0] = F[0]*f0_factor;
    F[1] = F[1]*f0_factor;

    // repulsive terms between pedestrians
    if (!passenger.seated) {
        for (auto &other_passenger : passengers) {
            if (passenger.get_uid() == other_passenger.get_uid() ||
                other_passenger.seated || other_passenger.phase == -1)
                continue;

            vector<double> Fped_ab = f_ab(passenger, other_passenger, V0,
                PEDPED_SIGMA);

            double in_sight_factor = in_sight(e, Fped_ab);
            F[0] += in_sight_factor*Fped_ab[0];
            F[1] += in_sight_factor*Fped_ab[1];
        }
    }

    // standing_boundaries
    if (passenger.walkspace) {
        vector<double> sbound = find_nearest_wall(passenger, standing_bounds);
        vector<double> Fsb = f_aB(passenger, sbound, U0_SB, R_SB);
        F[0] += Fsb[0];
        F[1] += Fsb[1];
    }

    // obstacles
    if (!passenger.seated) {
        vector<double> bound = find_nearest_wall(passenger, walls);
        vector<double> Fb = f_aB(passenger, bound, U0_E, R_E);
        F[0] += Fb[0];
        F[1] += Fb[1];
    }

    // desired velocity
    vector<double> w = {0, 0};
    w[0] = passenger.vx + dt*F[0];
    w[1] = passenger.vy + dt*F[1];

    // capped velocity
    vector<double> v = {0, 0};
    double g = g_a(MAX_SPEED_MULTIPLIER*passenger.desired_speed, norm(w));

    v[0] = w[0]*g;
    v[1] = w[1]*g;

    // update state
    passenger.new_x += v[0]*dt;
    passenger.new_y += v[1]*dt;

    passenger.new_vx = v[0];
    passenger.new_vy = v[1];
}
