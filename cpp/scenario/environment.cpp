#include "environment.h"

#include <vector>

#include "parameters.h"
#include "seat.h"
#include "spot.h"
#include "passenger.h"
#include "../io/readwrite.h"


Environment::Environment(double env_width,
                         double env_length,
                         double env_aisle_width,
                         double env_min_standing_x,
                         vector<Seat> env_seats,
                         vector<Spot> env_spots,
                         vector<vector<double>> env_doors,
                         vector<vector<double>> env_walls,
                         vector<vector<double>> env_door_walls,
                         vector<vector<double>> env_standing_bounds) {
    width = env_width;
    length = env_length;
    aisle_width = env_aisle_width;
    min_standing_x = env_min_standing_x;
    seats = env_seats;
    spots = env_spots;
    doors = env_doors;
    walls = env_walls;
    door_walls = env_door_walls;
    standing_bounds = env_standing_bounds;

    for (auto &seat : seats)
        seat.adjacent_seats(seats);

    walls_doors_closed = walls;

    walls_doors_closed.insert(walls_doors_closed.end(),
        door_walls.begin(), door_walls.end() );
}
