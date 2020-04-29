#include "pch.h"
#include "CppUnitTest.h"
#include "fft.h"
#include "NumCpp.h"

#include <cmath>

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace TestProject
{
	TEST_CLASS(TestProject)
	{
	public:
		
		TEST_METHOD(FFTTest1)
		{
			vector<double> t = NumCpp::linspace(0.0, 256.0, 256);
			vector<double> signal = NumCpp::sin(t, 1 / 256);

			FFTCalculator fftCalc;
			vector<complex<double>> fft(256, 0.0);
			fftCalc.FFT(signal, fft, 256);
			vector<complex<double>> modFFT = NumCpp::abs(fft);

			vector<complex<double>> modFFTInOrder = NumCpp::rearangeInBitReverse(modFFT);
			int hola;
		}
	};
}
