#!/usr/bin/python

import numpy
import scipy
from pepa_ss_parse import pepa_ss_parser

def ctmc(Q):
    b = numpy.zeros(len(Q), dtype=numpy.float64)
    b[0] = 1
    # normalization
    Q[:,0] = 1
    return numpy.linalg.solve(Q.transpose(),b)

if __name__ == "__main__":

    x = ctmc(pepa_ss_parser("test_examples/model3.generator"))
    for el in numpy.nditer(x):
        if el < 0:
            print("Error, probabilities are negative, the universe exploded just now")
            break
        else:
            print(x)
