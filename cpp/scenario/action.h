#ifndef SCENARIO_ACTION_H_
#define SCENARIO_ACTION_H_

#include <vector>
#include <string>

using std::vector;
using std::string;


class Action {
    public:
        int frame;
        string name;
        vector<double> num_args;
        vector<vector<double>> list_args;

        Action(int action_frame,
               string action_name,
               vector<double> num_arguments,
               vector<vector<double>> list_arguments);
};


#endif  // SCENARIO_ACTION_H_
