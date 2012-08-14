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
from experiments.experiment import rate_experiment, range_maker
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
    sol_args = parser.add_argument_group("Solution", "Solution related commands")
    exp_args = parser.add_argument_group("Experimentations", "Experimentations")
    sol_args.add_argument("-s", "--solver", action="store", dest="solver",type=str,  choices=['direct', 'sparse'], help="choose solver type DEFAULT: sparse", default="sparse")
    output_args = parser.add_argument_group("Output", "Output based options")
    parser.add_argument("file", help="path to the model file")
    output_args.add_argument("-gd", "--generate_dots", help="generate a graphviz dot file for every sequential component.WARNING: this can be very memory consuming when the state space is big", action="store_true", dest="gendots")
    output_args.add_argument("-st", "--steady", help="print steady state probability vector", action="store_true")
    output_args.add_argument("-th", "--performance", help="print throughoutput of actions", action="store_true", dest="top")
    output_args.add_argument("-ut", "--utilization", help="print utilization of action", action="store_true", dest="util")
    output_args.add_argument("-f", "--format", dest="format", type=str, choices=["console", "csv", "maple"], help="format for -st -th -ut")

    exp_args.add_argument("-varrate", help="varying rate with \n range r:1.0,10,0.1 or list l:1,2,3,4,5,6,7,8,9", dest="varrate", action="store", metavar="ratename,range")
    exp_args.add_argument("-", help="varying rate agains throughoutput of action", dest="varrate", action="store", metavar="ratename,actionname")


    args = parser.parse_args()

    pm = PEPAModel(args)
    pm.derive()

    # ran = range_maker(1,100,1)
    # result = rate_experiment("rateReset", ran, "badOffer", pm)
    # from pylab import plot, ylabel, xlabel, show, savefig
    # plot(result[0], result[1], linewidth=1.0)
    # xlabel("rateReset")
    # ylabel("badOffer throughoutput")
    # savefig("fig1.png")
    # #show()

    if args.steady or args.top or args.util:
        pm.steady_state()
        print("Statespace of {} has {} states \n".format( args.file ,len(pm.get_steady_state_vector() )))


    if args.steady:
        print("Steady state vector")
        _pretty_print_vector(pm.get_steady_state_vector())
    if args.top:
        print("Throuhoutput (successful action completion in one time unit)\n")
        _pretty_print_performance(pm.get_throughoutput())
    if args.util:
        print("NOT IMPLEMENTED YET")


