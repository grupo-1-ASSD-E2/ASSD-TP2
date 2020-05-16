
import numpy as np
import matplotlib.pyplot as plt
import control
import scipy
from sympy.core.numbers import pi, I, oo
from sympy import re, im
from scipy import signal


l = 199
z = np.linspace(0, 2*np.pi, 10000)
#r=0.999
num = 0.5 * z**(l+1) + 0.5 * z**l
den = z**(l+1) - 0.5 * 0.1 * (z + 1)

num_c = np.array([0.5, 0.5])
num_ceros = np.zeros(l) 
num_c = np.concatenate((num_c, num_ceros)) #coefs del num

den_c = np.array([1])
den_cc = np.array([- 0.5 * 0.999, - 0.5 * 0.999])
den_ceros = np.zeros(l-1)
den_c = np.concatenate((den_c, den_ceros, den_cc))


tf = control.TransferFunction(num_c,den_c)
control.pzmap(tf, Plot = True, title =  'Diagrama de polos y ceros')
#control.bode_plot(tf)
plt.grid(which = 'both')
plt.show()



import scipy
from scipy import signal



