#include "utils.h"

#include <random>
#include <vector>


int rand_int() {
    std::mt19937 gen(std::random_device {}());
    std::uniform_int_distribution<int> distrib(0, RAND_MAX);
    return distrib(gen);
}

double rand_double() {
    std::mt19937 gen(std::random_device {}());
    std::uniform_real_distribution<double> distrib(0, 1);
    return distrib(gen);
}

double normal_dist_rand(double mean, double std) {
    std::mt19937 gen(std::random_device {}());
    std::normal_distribution<double> ndr(mean, std);
    return ndr(gen);
}

std::vector<int> rand_sample(int min_value, int max_value, int sample_size) {
    std::vector<int> options;
    for (int i = min_value; i <= max_value; i++)
        options.push_back(i);

    std::vector<int> sample;
    for (int i = 0; i != sample_size; i++) {
        int selection = rand_int()%options.size();
        sample.push_back(options[selection]);
        options.erase(options.begin() + selection);
    }

    return sample;
}
