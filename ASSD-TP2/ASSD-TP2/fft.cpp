#include "fft.h"
#include <cmath>

#define PI (3.141592653589793238463)

void FFTCalculator::FFT(complex<double>* in, complex<double>* out, size_t n)
{
	// Calculating Wn.
	calculateWn(n);
	// Calculating FFT
	recursiveFFT(out, Wn, n, n, 0, 0);
}

void FFTCalculator::repeatFFT(complex<double>* in, complex<double>* out, size_t n)
{
	recursiveFFT(out, Wn, n, n, 0, 0);
}

void FFTCalculator::recursiveFFT(complex<double>* Xk, vector<complex<double>>& Wn, size_t N, size_t totalN, int groupNumber, int level)
{
	unsigned int offsetInXn = N * groupNumber;
	unsigned int currentWn = bitReverse(sqrt(totalN), groupNumber);

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
		recursiveFFT(Xk, Wn, N / 2, totalN, 2 * groupNumber, level + 1);
		recursiveFFT(Xk, Wn, N / 2, totalN, 2 * groupNumber + 1, level + 1);
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

void FFTCalculator::calculateWn(size_t n)
{
	for (size_t i = 0; i < n / 2; i++)
	{
		complex<double> newWn = exp(complex<double>(0.0, 1.0) * 2.0 * complex<double>(i) * PI / complex<double>(n));
	}
}
