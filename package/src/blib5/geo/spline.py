import numpy as np 
from .. import decorate

def calculator(R):
    MP1 = R.shape[-1]
    if R.ndim == 2:
        def calculator(U):
            npoints = U.shape[0]
            '''
            construct PU with every row i = [1 u[i] u[i]² u[i]³ ... ]
            U = np.linspace(0,1,5)
            PU = 
                [1.       0.       0.       0.      ]
                [1.       0.25     0.0625   0.015625]
                [1.       0.5      0.25     0.125   ]
                [1.       0.75     0.5625   0.421875]
                [1.       1.       1.       1.      ]]
            '''        
            PU = np.empty((npoints, MP1))
            PU[:] = U[:, np.newaxis]
            PU[:,0] = 1
            PU = np.cumprod(PU, axis=1)
            return PU @ R
    elif R.ndim == 3:
        def calculator(IDX, U):
            npoints = U.shape[0]      
            PU = np.empty((npoints, MP1))
            PU[:] = U[:, np.newaxis]
            PU[:,0] = 1
            PU = np.cumprod(PU, axis=1)
            return (PU[:,:,np.newaxis]*R[IDX]).sum(axis=1) 
        calculator.nsegments = R.shape[0]  
    calculator.R = R
    return calculator


#############################################################################################
'''
Calculate the polynomial coefficients for every control point.

polynomial_coefficients_of_1d_bezier(3)
=>
array([[ 1, -3,  3, -1],
       [ 0,  3, -6,  3],
       [ 0,  0,  3, -3],
       [ 0,  0,  0,  1]], dtype=int32)

'''
@decorate.cache_unary_function_result
def bezier_polynomial_coefficients(M):
    B = np.zeros( (M+1,M+1), dtype=np.int32)
    B[:,-1] = 1
    for i in range(M,0,-1):
        B[i-1] = -B[i]
        B[i-1,:-1] += B[i,1:]
    B = B * np.abs(B[0]).reshape((M+1,1))
    return B


'''
Construct a point calculator for a fixed set of M+1 control points and variable U.
The shape of control points is (N, M+1, dimension of points) for N segments.
'''
def calculator_1d_bezier(CONTROL_POINTS):
    ''' shape of control points is (M+1, dimension of points)'''
    M = CONTROL_POINTS.shape[-2] - 1  # degree of the polynomial
    B = bezier_polynomial_coefficients(M).transpose()
    # we squash all terms of the same degree together to make an efficient calculator that takes a variable array of t values.
    R = B @ CONTROL_POINTS
    return calculator(R)
