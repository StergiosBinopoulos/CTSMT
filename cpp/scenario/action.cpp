#include "action.h"

#include <vector>
#include <string>


using std::vector;
using std::string;


Action::Action(int action_frame,
               string action_name,
               vector<double> num_arguments,
               vector<vector<double>> list_arguments) {
    frame = action_frame;
    name = action_name;
    num_args = num_arguments;
    list_args = list_arguments;
}
