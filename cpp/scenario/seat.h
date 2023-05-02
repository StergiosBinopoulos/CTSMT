#ifndef SCENARIO_SEAT_H_
#define SCENARIO_SEAT_H_

#include <vector>


using std::vector;


class Seat {
    public:
        double x;
        double y;
        double r;
        bool window;
        bool occupied;

        Seat* upper_seat;
        Seat* lower_seat;
        Seat* right_seat;
        Seat* left_seat;
        vector<Seat*> adjacent;

        Seat(double seat_x, double seat_y, double y_max, double rotation=0);

        void adjacent_seats(vector<Seat> &seats);
        
        double utility(double px);
};


#endif  // SCENARIO_SEAT_H_
