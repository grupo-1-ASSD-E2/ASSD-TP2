#pragma once
#include <complex>
#include <vector>

using namespace std;

class FFTCalculator
{
public:
	// Calculate FFT from scratch (includes calculations of Wn factors)
	void FFT(vector<double>& x, vector<complex<double>>& Xk, size_t N);
	// Uses the same Wn already saved in this object and thus speeds up the process (for real time signal processing, for instance)
	void repeatFFT(vector<double>& x, vector<complex<double>>& Xk, size_t N);

private:
	void recursiveFFT(vector<complex<double>>& Xk, size_t N, size_t totalN, int groupNumber, int level);
	unsigned int bitReverse(size_t numberOfBits, unsigned int num);
	unsigned int shift(unsigned int num, size_t level, size_t totalN);
	void calculateWn(size_t n);

	vector<complex<double>> Wn;

};