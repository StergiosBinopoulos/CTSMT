#include "seat.h"

#include <cmath>

#include "parameters.h"


Seat::Seat(double seat_x, double seat_y, double y_max, double rotation) {
    x = seat_x;
    y = seat_y;
    r = rotation;
    occupied = false;
    window = (y < 0.6 || y_max - y < 0.6);

    upper_seat = nullptr;
    lower_seat = nullptr;
    right_seat = nullptr;
    left_seat = nullptr;
}

void Seat::adjacent_seats(vector<Seat> &seats) {
    adjacent.clear();
    for (auto &seat : seats) {
        if (seat.y == y && seat.x == x)
            continue;

        double dy = seat.y - y;
        double dx = seat.x - x;

        if (std::abs(dx) < 0.3) {
            if ((0 < dy) && (dy < 0.6))
                upper_seat = &seat;

            else if ((0 > dy) && (dy > -0.6))
                lower_seat = &seat;
        }

        if (std::abs(dy) < 0.3) {
            if ((0 < dx) && (dx < 0.6))
                right_seat = &seat;

            else if ((0 > dx) && (dx > -0.6))
                left_seat = &seat;
        }
    }

    if (std::abs(r) < 0.1 || std::abs(r-180) < 0.1) {
        if (upper_seat != nullptr)
            adjacent.push_back(upper_seat);
        if (lower_seat != nullptr)
            adjacent.push_back(lower_seat);
    }

    if (std::abs(r-90) < 0.1 || std::abs(r-270) < 0.1) {
        if (right_seat != nullptr)
            adjacent.push_back(right_seat);
        if (left_seat != nullptr)
            adjacent.push_back(left_seat);
    }
}

double Seat::utility(double px) {
    if (occupied)
        return 0;

    double distance = std::abs(x - px);
    if (distance > 5)
        return 0;

    double adj_par = 1;
    for (auto seat : adjacent) {
        if (seat->occupied)
            adj_par = MADJ;
    }

    double window_par = window? MW: 1;
    double base_util = exp(-0.5 * pow(distance / 1.5, 2));
    double util = window_par * adj_par * base_util;

    return util;
}
