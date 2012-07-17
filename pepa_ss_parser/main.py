from ctmc import ctmc
from pepa_ss_parse import pepa_ss_parser
import numpy

if __name__ == "__main__":
    x = ctmc(pepa_ss_parser("test_examples/modelen.generator"))
    #x = ctmc(pepa_ss_parser("test_examples/webserver.generator"))
    #x = ctmc(pepa_ss_parser("test_examples/model3.generator"))
    err = 0
    for el in numpy.nditer(x):
        if el < 0:
            print("Error, probabilities are negative, the universe exploded just now")
            err = 1
            break
    if err == 0:
        print(x)   




