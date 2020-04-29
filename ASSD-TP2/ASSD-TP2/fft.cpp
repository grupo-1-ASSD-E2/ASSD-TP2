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
		complex<double> auxXk = Wn[currentWn] * x[offsetInXn + N / 2 + i];
		Xk[offsetInXn + N / 2 + i] = x[offsetInXn + i] - auxXk;
		Xk[offsetInXn + i] = x[offsetInXn + i] + auxXk;
	}
	if (N != 2)
	{
		recursiveFFT(Xk, N / 2, N, 0, 1);
		recursiveFFT(Xk, N / 2, N, 1, 1);
	}
}

void FFTCalculator::recursiveFFT(vector<complex<double>>& Xk, size_t N, size_t totalN, int groupNumber, int level)
{
	unsigned int offsetInXn = N * groupNumber;
	unsigned int currentWn = NumCpp::shift(NumCpp::bitReverse(static_cast<size_t>(log2(totalN)), offsetInXn), level, totalN);

	// Computing FFT for this group.
	for (size_t i = 0; i < N/2; i++)
	{
		complex<double> auxXk = Wn[currentWn] * Xk[offsetInXn + N / 2 + i];
		Xk[offsetInXn + N / 2 + i] = Xk[offsetInXn + i] - auxXk;
		Xk[offsetInXn + i] = Xk[offsetInXn + i] + auxXk;
	}

	// Recursive case
	if (N != 2)
	{
		recursiveFFT(Xk, N / 2, totalN, 2 * groupNumber, level + 1);
		recursiveFFT(Xk, N / 2, totalN, 2 * groupNumber + 1, level + 1);
	}
}

void FFTCalculator::calculateWn(size_t N)
{
	for (size_t k = 0; k < N / 2; k++)
	{
		complex<double> newWn = exp(complex<double>(0.0, 1.0) * complex<double>(2.0 * k * PI / N));
		Wn.push_back(newWn);
	}
}