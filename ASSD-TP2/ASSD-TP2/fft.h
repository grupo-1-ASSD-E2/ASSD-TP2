#pragma once
#include <complex>
#include <vector>

using namespace std;

class FFTCalculator
{
public:
	// Calculate FFT from scratch (includes calculations of Wn factors)
	void FFT(complex<double>* in, complex<double>* out, size_t n);
	// Uses the same Wn already saved in this object and thus speeds up the process (for real time signal processing, for instance)
	void repeatFFT(complex<double>* in, complex<double>* out, size_t n);

private:
	void recursiveFFT(complex<double>* Xk, vector<complex<double>>& Wn, size_t N, size_t totalN, int groupNumber, int level);
	unsigned int bitReverse(size_t numberOfBits, unsigned int num);
	void calculateWn(size_t n);

	vector<complex<double>> Wn;
};