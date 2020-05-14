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

unsigned int NumCpp::bitReverse(size_t numberOfBits, unsigned int num)
{
	unsigned int reversed = 0;
	for (size_t i = 0; i < numberOfBits; i++)
	{
		if (num & (1 << i))
		{
			reversed |= 1 << ((numberOfBits - 1) - i);
		}
	}
	return reversed;
}

unsigned int NumCpp::shift(unsigned int num, size_t level, size_t totalN)
{
	unsigned int size = static_cast<unsigned int>(log2(totalN));
	unsigned int ret = num << (size - level - 1);

	// Building mask for first log2(totalN) bits.
	unsigned int mask = 0;
	for (size_t i = 0; i < size; i++)
	{
		mask |= 1 << i;
	}

	// Applying mask.
	ret &= mask;

	return ret;
}