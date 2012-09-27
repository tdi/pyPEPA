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
from experiments.experiment import rate_experiment, range_maker, rate_experiment_two
from experiments.graphing import plot_2d, plot_3d
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
    output_args.add_argument("-tr", "--transient", help="print throughoutput of actions", action="store", dest="trantime", type=int)
    output_args.add_argument("-ut", "--utilization", help="print utilization of action", action="store_true", dest="util")
    output_args.add_argument("-f", "--format", dest="format", type=str, choices=["graph", "console", "csv"], help="format for -st -th -ut", default="console")

    exp_args.add_argument("-vr", "--varrate", help="varyin rate name", dest="varrate", action="store", metavar="ratename")
    exp_args.add_argument("--range", help="\"START,STOP,STEP\" e.g. \"1.0,10,0.1\"", dest="range", action="store", metavar="range")
    exp_args.add_argument("--list", help="List of values e.g. \"1,2,3,5.0,4\"", dest="list_range", action="store", metavar="list")
    exp_args.add_argument("--actionth", help="throughoutput of action on the Y axis", dest="actionth", action="store", metavar="action name")
    exp_args.add_argument("--actionth2", help="throughoutput of the second action on the Z axis, if this is given 3d graph is created", dest="actionth2", action="store", metavar="action name")

    args = parser.parse_args()

    # mutual exclusion
    if args.list_range and args.range:
        print("Cannot use range and list")
        exit(1)


    if args.varrate:
        ratename = args.varrate
        if args.actionth is None:
            print("Action name not given")
            exit(1)
        if args.range:
            rran = args.range.split(",")
            if len(rran) != 3:
                print("Range should be START, STOP, STEP")
                exit(1)
            start, stop, step = rran[0], rran[1], rran[2]
            ran = range_maker(float(start), float(stop), float(step))
            pm = PEPAModel(args)
            pm.derive()
            if args.actionth2 is None:
                result = rate_experiment(ratename, ran, args.actionth, pm)
                if args.format == "graph":
                    plot_2d(result[0], result[1], lw=2, action="show", xlab=ratename, ylab=args.actionth)
                elif args.format == "csv":
                    with open("varrate-thr-{}-{}.csv".format(ratename, args.actionth), "w") as exp_f:
                        exp_f.write("{}, {}\n".format(ratename, args.actionth))
                        x = result[0]
                        y = result[1]
                        for i in list(range(0, len(x))):
                            exp_f.write("{}, {}\n".format(x[i], y[i]))

            else:
                result = rate_experiment_two(ratename, ran, args.actionth, args.actionth2, pm)
                print(result)
                if args.format == "graph":
                    plot_3d(result[0], result[1], result[2], lw=2, action="show", xlab=ratename, ylab=args.actionth, zlab=args.actionth2)
        exit(0)


    if args.steady or args.top or args.util:
        pm = PEPAModel(args)
        pm.derive()
        pm.steady_state()
        print("Statespace of {} has {} states \n".format( args.file ,len(pm.get_steady_state_vector() )))
    if args.trantime:
        pm = PEPAModel(args)
        pm.derive()
        pm.transient(10)
        print("transient")

    if args.steady:
        print("Steady state vector")
        _pretty_print_vector(pm.get_steady_state_vector())
    if args.top:
        print("Throuhoutput (successful action completion in one time unit)\n")
        _pretty_print_performance(pm.get_throughoutput())
    if args.util:
        print("NOT IMPLEMENTED YET")


