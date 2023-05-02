#include <vector>
#include <iostream>

#include "io/readwrite.h"
#include "utils/utils.h"
#include "scenario/parameters.h"
#include "scenario/seat.h"
#include "scenario/spot.h"
#include "scenario/passenger.h"
#include "scenario/scenario.h"
#include "transmission/transmission.h"
#include "socialforcemodel/socialforcemodel.h"


using std::vector;
using std::cout;
using std::endl;


int main() {
    Scenario new_scenario;
    new_scenario.simulate();
    write_states(new_scenario.states);
}
