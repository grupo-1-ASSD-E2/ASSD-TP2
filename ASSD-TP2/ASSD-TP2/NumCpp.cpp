#include "NumCpp.h"

vector<double> NumCpp::sin(vector<double>& t, double frec, double phase)
{
    vector<double> res;

    for (double tn : t)
    {
        res.push_back(std::sin(2 * PI * frec * tn + phase));
    }
    return res;
}

vector<double> NumCpp::cos(vector<double>& t, double frec, double phase)
{
    return NumCpp::sin(t, frec, phase + PI / 2);
}
