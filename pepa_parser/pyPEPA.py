#!/usr/bin/env python
""" Main file od pyPEPA """

__author__ = "Dariusz Dwornikowski"
__copyright__ = "Dariusz Dwornikowski, Poznan University of Technology"
__licence__ = "GNU General Public License version 3"
__email__ = "dariusz.dwornikowski@cs.put.poznan.pl"
__version__ = "201208"


from pprint import pprint
import logging
from pepa_model import PEPAModel
import argparse


def _pretty_print_performance(actset):
    for perf in actset:
        print("{0:<40} {1:>10}".format(perf[0],perf[1]) )

def _pretty_print_vector(vect):
    i = 1
    for prob in vect:
        print("State {}: {}".format(i, vect[i-1]))
        i = i + 1

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="pyPEPA, author {}, {}".format(__author__, __email__))
    parser.add_argument("file", help="path to the model file")
    parser.add_argument("-gd", "--generate_dots", help="generate a graphviz dot file for every sequentail component.WARNING: this can be very memory consuming when the state space is big", action="store_true", dest="gendots")
    parser.add_argument("-s", "--steady", help="print steady state probability vector", action="store_true")
    parser.add_argument("-t", "--performance", help="print throughoutput of action", action="store_true", dest="top")
    args = parser.parse_args()

    pm = PEPAModel(args)
    pm.derive()
    pm.recalculate()

    if args.steady or args.top:
        pm.steady_state()


    if args.steady:
        print("Statespace of {} has {} states \n".format( args.file ,len(pm.get_steady_state_vector() )))
        print("Steady state vector")
        _pretty_print_vector(pm.get_steady_state_vector())
    if args.top:
        print("Statespace of {} has {} states \n".format( args.file ,len(pm.get_steady_state_vector() )))
        print("Throuhoutput (successful action completion in one time unit)\n")
        _pretty_print_performance(pm.get_throughoutput())


