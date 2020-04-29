#pragma once
#include <cmath>
#include <vector>

#ifndef PI
#define PI (3.141592653589793238463)
#endif // !PI

using namespace std;

class NumCpp
	// Implements numpy like functions for C++
{
public:
	template<typename T>
    static vector<double> linspace(T start_in, T end_in, int num_in);
    template<typename T>
    static vector<T> abs(vector<T> in);

	static vector<double> sin(vector<double>& t, double frec, double phase = 0);
	static vector<double> cos(vector<double>& t, double frec, double phase = 0);

private:
};

template<typename T>
inline vector<double> NumCpp::linspace(T start_in, T end_in, int num_in)
{
    vector<double> linspaced;

    double start = static_cast<double>(start_in);
    double end = static_cast<double>(end_in);
    double num = static_cast<double>(num_in);

    if (num == 0) { return linspaced; }
    if (num == 1)
    {
        linspaced.push_back(start);
        return linspaced;
    }

    double delta = (end - start) / (num - 1);

    for (int i = 0; i < num - 1; ++i)
    {
        linspaced.push_back(start + delta * i);
    }
    linspaced.push_back(end); // I want to ensure that start and end are exactly the same as the input
    return linspaced;
}

template<typename T>
inline vector<T> NumCpp::abs(vector<T> in)
{
    vector<T> ret(in.size());
    for (T item : in)
    {
        ret.push_back(std::abs(item));
    }
    return ret;
}
