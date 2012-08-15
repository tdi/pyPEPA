#!/usr/bin/python

import numpy
import scipy
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from scipy.linalg import expm

def ctmc(Q):
    b = numpy.zeros(len(Q), dtype=numpy.float64)
    b[0] = 1
    # normalization
    Q[:,0] = 1
    return numpy.linalg.solve(Q.transpose(),b)

def ctmc_sparse(Q, size):
    b = numpy.zeros(size, dtype=numpy.float64)
    b[0] = 1
    # normalization
    Q[:,0] = 1
    Q =Q.tocsr()
    return spsolve(Q.transpose(),b)

def ctmc_transient(Q, size, tstart, tstop):
    Qnew = expm(Q*tstop)
    return Qnew



def vector_mult(v1, v2):
    return float(numpy.vdot(numpy.array(v1), numpy.array(v2)))

def create_lil_matrix(res):
    size = len(res)
    QD = numpy.zeros( (size, size), dtype=numpy.float64)
    Q = lil_matrix(QD)
    del QD
    rowsum = 0.0
    for key in sorted(res, key=lambda k: res[k][1]):
        for tos in res[key][0]:
            from_state = int( res[key][1] )
            to_state = int( res[tos[1]][1] )
            rate = float(tos[0])
            Q[ from_state-1 , to_state-1 ] = rate
            rowsum += rate
        Q[ res[key][1]-1 , res[key][1]-1] = -rowsum
        rowsum = 0.0
    return Q


def create_matrix(res):
    # create matrix lnum x lnum
    size = len(res)
    Q = numpy.zeros( (size, size), dtype=numpy.float64)
    rowsum = 0.0
    for key in sorted(res, key=lambda k: res[k][1]):
        for tos in res[key][0]:
            from_state = int( res[key][1] )
            to_state = int( res[tos[1]][1] )
            rate = float(tos[0])
            Q[ from_state-1 , to_state-1 ] = rate
            rowsum += rate
        Q[ res[key][1]-1 , res[key][1]-1] = -rowsum
        rowsum = 0.0
    return Q



if __name__ == "__main__":

    x = ctmc(pepa_ss_parser("test_examples/model3.generator"))
    for el in numpy.nditer(x):
        if el < 0:
            print("Error, probabilities are negative, the universe exploded just now")
            break
        else:
            print(x)
