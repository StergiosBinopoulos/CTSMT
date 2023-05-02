#include "readwrite.h"

#include <map>
#include <fstream>
#include <sstream>
#include <string>
#include <iostream>
#include <iomanip>
#include <functional>

#include "../scenario/seat.h"
#include "../scenario/spot.h"
#include "../scenario/passenger.h"
#include "../scenario/scenario.h"
#include "../scenario/action.h"


using std::string;
using std::vector;


void separate(string s, vector<double> &num_arguments,
        vector<vector<double>> &list_arguments) {
    num_arguments.clear();
    list_arguments.clear();
    bool in_list = false;
    vector<double> list;

    string val;

    for (std::size_t i = 0; i <= s.size(); i++) {
        if (s[i] == ',' || i == s.size()) {
            if (val.size() < 1)
                continue;
            
            if (in_list)
                list.push_back(stod(val));

            else
                num_arguments.push_back(stod(val));

            val = "";

        } else if (s[i] == '{') {
            in_list = true;

        } else if (s[i] == '}') {
            in_list = false;
            list.push_back(stod(val));

            list_arguments.push_back(list);

            val = "";
            list.clear();

        } else {
            val.push_back(s[i]);
        }
    }
}

std::map<string, double> read_parameters() {
    std::ifstream file("./files/parameters.txt");
    string line; 
    std::map<string, double> parameters;    
    while (std::getline(file, line)) {
        if (line[0] == '#')
            continue;

        std::size_t pos = line.find(':');
        string num;
        double value;
        string var = line.substr(0, pos);

        char const* digits = "-.0123456789";
        std::size_t const n = line.find_first_of(digits, pos);
        if (n != string::npos) {
            std::size_t const m = line.find_first_not_of(digits, n);
            num = line.substr(n, m != string::npos ? m-n : m);
        }   
        value = stod(num);
        parameters[var] = value;
    }
    return parameters;
}

void write_states(vector<vector<vector<double>>> states) {
    std::ofstream outfile;
    outfile.open("./files/states.txt");
    int frame = 0;

    for (auto state : states) {
        outfile << std::fixed;
        outfile << std::setprecision(3);
        outfile << '#' << frame << std::endl;
        frame++;
        for (auto entry : state) {
            for (long unsigned int i = 0; i != entry.size(); i++) {
                outfile << entry[i];
                if (i != entry.size()-1)
                    outfile << ",";
            }
            outfile << std::endl;
        }
    }
}

void read_actions(int &duration, vector<Action> &actions) {
    std::ifstream file("./files/actions.txt");
    string line;

    while (std::getline(file, line)) {
        if (line[0] == '#')
            continue;

        std::size_t pos1 = line.find('|');
        if (pos1 == string::npos)
            continue;
        string frame = line.substr(0, pos1);

        std::size_t pos2 = line.find(':');
        if (pos2 == string::npos)
            continue;

        string arg = line.substr(pos1 + 1, pos2 - pos1 - 1);

        std::size_t values_start = (pos2 != string::npos) ? pos2 + 1: pos2;
        string values = line.substr(values_start, string::npos - values_start);
        vector<double> num_args;
        vector<vector<double>> list_args;

        separate(values, num_args, list_args);
        if (arg == "duration") {
            duration = num_args[0];

        } else if (arg == "spawn" || arg == "remove"
                || arg == "open_doors" || arg == "passenger") {
            actions.push_back(Action(stoi(frame), arg, num_args, list_args));
        }
    }
}

void read_conditions(double &width,
                     double &length,
                     double &aisle_width,
                     double &min_standing_x,
                     vector<Seat> &seats,
                     vector<Spot> &spots,
                     vector<vector<double>> &doors,
                     vector<vector<double>> &walls,
                     vector<vector<double>> &door_walls,
                     vector<vector<double>> &standing_bounds) {
    std::ifstream file("./files/conditions.txt");
    string line;
    
    while (std::getline(file, line)) {
        if (line[0] == '#')
            continue;

        std::size_t pos = line.find(':');

        if (pos == string::npos)
            continue;

        string arg = line.substr(0, pos);

        std::size_t values_start = (pos != string::npos) ? pos + 1: pos;
        string values = line.substr(values_start, string::npos - values_start);
        vector<double> num_args;
        vector<vector<double>> list_args;

        separate(values, num_args, list_args);

        if (arg == "dimensions") {
            width = num_args[0];
            length = num_args[1];
            aisle_width = num_args[2];
            min_standing_x = num_args[3];

        } else if (arg == "standing_boundary") {
            standing_bounds.push_back({num_args[0], num_args[1]});

        } else if (arg == "seat") {
            seats.push_back(Seat(num_args[0], num_args[1], width, num_args[2]));

        } else if (arg == "spot") {
            spots.push_back(Spot(num_args[0], num_args[1]));

        } else if (arg == "door") {
            doors.push_back({num_args[0], num_args[1]});

        } else if (arg == "wall") {
            walls.push_back({num_args[0], num_args[1]});

        } else if (arg == "door_wall") {
            door_walls.push_back({num_args[0], num_args[1]});
        }
    }
}
