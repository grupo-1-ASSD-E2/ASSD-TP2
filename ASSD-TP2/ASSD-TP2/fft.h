#pragma once
#include <complex>
#include <vector>

using namespace std;

class FFTCalculator
{
public:
	void FFT(complex<double>* in, complex<double>* out, size_t n);

private:
	void recursiveFFT(complex<double>* Xk, vector<complex<double>>& Wn, size_t N, size_t totalN, int groupNumber, int level);
	unsigned int bitReverse(size_t numberOfBits, unsigned int num);
};