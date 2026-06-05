import numpy as np 
from .. import decorate

'''
Calculate the polynomial coefficients for every control point.

polynomial_coefficients_of_1d_bezier(3)
=>
array([[ 1, -3,  3, -1],
       [ 0,  3, -6,  3],
       [ 0,  0,  3, -3],
       [ 0,  0,  0,  1]], dtype=int32)

Given M+1 control points, we can then "squash" everything together
along the axis of degree of t to make an efficient calculator that takes a 
variable range of u 
'''
@decorate.cache_unary_function_result
def bezier_polynomial_coefficients(M, cache = {}):
    B = cache.get(M,None)
    if not B is None: return B    
    B = np.zeros( (M+1,M+1), dtype=np.int32)
    B[:,-1] = 1
    for i in range(M,0,-1):
        B[i-1] = -B[i]
        B[i-1,:-1] += B[i,1:]
    B = B * np.abs(B[0]).reshape((M+1,1))
    cache[M] = B
    return B

