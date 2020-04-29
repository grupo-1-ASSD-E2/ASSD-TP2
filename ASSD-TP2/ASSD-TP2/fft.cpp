#include "fft.h"
#include <cmath>

#ifndef PI
#define PI (3.141592653589793238463)
#endif // !PI

void FFTCalculator::FFT(vector<double>& x, vector<complex<double>>& Xk, size_t N)
{
	// Calculating Wn.
	calculateWn(N);
	// Calculating FFT
	repeatFFT(x, Xk, N);
}

void FFTCalculator::repeatFFT(vector<double>& x, vector<complex<double>>& Xk, size_t N)
{
	unsigned int offsetInXn = 0;
	unsigned int currentWn = 0;

	// Computing FFT for first group.
	for (size_t i = 0; i < N / 2; i++)
	{
		complex<double> auxXk = x[offsetInXn + i];
		Xk[offsetInXn + i] = x[offsetInXn + i] + Wn[currentWn + i] * x[offsetInXn + N / 2 + i];
		Xk[offsetInXn + N / 2 + i] = auxXk - Wn[currentWn + i] * x[offsetInXn + N / 2 + i];
	}
	recursiveFFT(Xk, N, N, 0, 0);
}

void FFTCalculator::recursiveFFT(vector<complex<double>>& Xk, size_t N, size_t totalN, int groupNumber, int level)
{
	unsigned int offsetInXn = N * groupNumber;
	unsigned int currentWn = shift(bitReverse(static_cast<size_t>(log2(totalN)), groupNumber), level, totalN);

	// currentWn will be a number between 0 and titalN-1, but Wn only has N/2 elements, so...
	if (currentWn >= N / 2)
	{
		currentWn -= N / 2;
	}

	// Computing FFT for this group.
	for (size_t i = 0; i < N/2; i++)
	{
		complex<double> auxXk = Xk[offsetInXn + i];
		Xk[offsetInXn + i] = Xk[offsetInXn + i] + Wn[currentWn + i] * Xk[offsetInXn + N / 2 + i];
		Xk[offsetInXn + N / 2 + i] = auxXk - Wn[currentWn + i] * Xk[offsetInXn + N / 2 + i];
	}

	// Recursive case
	if (N != 2)
	{
		recursiveFFT(Xk, N / 2, totalN, 2 * groupNumber, level + 1);
		recursiveFFT(Xk, N / 2, totalN, 2 * groupNumber + 1, level + 1);
	}
}

unsigned int FFTCalculator::bitReverse(size_t numberOfBits, unsigned int num)
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

unsigned int FFTCalculator::shift(unsigned int num, size_t level, size_t totalN)
{
	unsigned int size = static_cast<unsigned int>(log2(totalN));
	unsigned int ret = num << (level - size);

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

void FFTCalculator::calculateWn(size_t N)
{
	for (size_t k = 0; k < N / 2; k++)
	{
		complex<double> newWn = exp(complex<double>(0.0, 1.0) * complex<double>(2.0 * k * PI / N));
		Wn.push_back(newWn);
	}
}
