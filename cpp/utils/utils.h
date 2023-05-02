#ifndef UTILS_UTILS_H_
#define UTILS_UTILS_H_

#include <random>
#include <vector>

int rand_int();

double rand_double();

double normal_dist_rand(double mean, double std);

std::vector<int> rand_sample(int min_value, int max_value, int sample_size);

#endif  // UTILS_UTILS_H_
