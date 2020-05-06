# => Description: This definition performs quadratic interpolation for estimating the true position of
#                 an inter-sample maximum when nearby samples are known.
# => Parameters: 
#           - f: Input vector
#           - x: Index for that vector 
# => Precondition: Assumes that f is a dicrete time fourier transform vetor of real input and x is a
#                  less accurate, naive version of the inter-sample maximum
# => Postcondition: Returns the coordinates of the vertex of a parabola that goes through point x and
#                   its two neighbors.

def parabolic(f, x):
    xv = 1/2. * (f[x-1] - f[x+1]) / (f[x-1] - 2 * f[x] + f[x+1]) + x
    yv = f[x] - 1/4. * (f[x-1] - f[x+1]) * (xv - x)
    return (xv, yv)