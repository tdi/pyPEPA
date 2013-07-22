#!/usr/bin/env python
__author__= "Dariusz Dwornikowski"
__email__ = "dariusz.dwornikowski@cs.put.poznan.pl"

""" Main file for pyPEPA """

from pprint import pprint
from pypepa import PEPAModel
from pypepa.utils import pretty_print_vector, pretty_print_performance,\
                           pretty_print_utilisations
from pypepa.experiments.experiment import rate_experiment, range_maker,\
                                            rate_experiment_two
from pypepa.experiments.graphing import plot_2d, plot_3d
from pypepa.logger import init_log
from pypepa import __version__
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="pypepa v{},"
                                     " author {}, {}".format(__version__,
                                     __author__, __email__))
    gen_args = parser.add_argument_group("General", "General arguments")
    gen_args.add_argument("--log", action="store", dest="loglevel", 
                          choices=["DEBUG", "INFO", "ERROR", "NONE"], 
                          help="logging level",
                          default="ERROR", type=str)
    sol_args = parser.add_argument_group("Solution",
                                         "Solution related commands")
    exp_args = parser.add_argument_group("Experimentations",
                                         "Experimentations")

    sol_args.add_argument("-s", "--solver", action="store",
                          dest="solver",type=str,
                          choices=['direct', 'sparse'],
                          help="choose solver type DEFAULT: sparse",
                          default="sparse")
    sol_args.add_argument("-da", "--derive-algorithm", action="store",
                          type=str, choices=["BU", "TD"],
                          help="Choose the algorithm to use for deriving the statespace",
                          default="BU")
    output_args = parser.add_argument_group("Output", "Output based options")
    parser.add_argument("file", help="path to the model file")
    output_args.add_argument("-gd", "--generate_dots",
                             help="generate a graphviz dot file for every"
                                  "sequential component in a GENDOTS folder and"
                                  "for the whole state space",
                             action="store", dest="gendots", type=str)
    output_args.add_argument("-st", "--steady",
                             help="print steady state probability vector",
                             action="store_true")
    output_args.add_argument("-ut", "--utilisations",
                             help="print steady state utilisations",
                             action="store_true")
    output_args.add_argument("-th", "--performance",
                             help="print throughoutput of actions",
                             action="store_true", dest="top")
    output_args.add_argument("-tr", "--transient",
                             help="print throughoutput of actions",
                             action="store", dest="trantime", type=int)
    output_args.add_argument("-f", "--format", dest="format", type=str,
                             choices=["graph", "console", "csv"],
                             help="format for -st -th -varrate", default="console")
    output_args.add_argument("-o", "--output", dest="output", type=str,
                               action="store",
                              help="output file valid when format cvs")
    exp_args.add_argument("-var", "--variable",
                          help="one or more variables in format"
                               "rate:RATENAME:r:START,STOP,STEP"
                               "or rate:RATENAME:l:val1,val2,val3",
                          action="append", dest="variables")
    exp_args.add_argument("-val", "--value", action="store", dest="yvar") 
    # exp_args.add_argument("--actionth",
    #                       help="throughoutput of action on the Y axis",
    #                       dest="actionth", action="store",
    #                       metavar="action name")

    args = parser.parse_args()

    logger = init_log(log_level=args.loglevel)
    pargs = {"file": args.file, "solver" : args.solver,
             "derive_algorithm": args.derive_algorithm}

    if args.gendots:
        try:
            pm = PEPAModel(**pargs)
        except Exception as e:
            print("Exception occured:", e)
            sys.exit(1)
        import os
        if os.path.isdir(args.gendots):
            pass
        else:
            os.makedirs(args.gendots)
        pm.generate_dots(args.gendots)
        sys.exit(0)

    if args.variables and args.yvar:
        variables = decode_variables(args.variables)
        if len(variables) == 1:
            pm = PEPAModel(**pargs)
            pm.derive()
            result = experiment(variables, args.yvar, pm)
            if args.format == "graph":
                plot_2d(result[0], result[1], lw=2, action="show",
                        xlab=args.yvar, ylab=variables[0].varval)
            elif args.format == "csv":
                with open("{}.csv".format(args.output), "w") as f:
                    for i in range(0, len(result[0])):
                            f.write("{}, {}\n".format(result[0][i], result[1][i]))
        elif len(variables) == 2:
            pm = PEPAModel(**pargs)
            pm.derive()
            result = experiment(variables, args.yvar, pm)
            plot_3d(result[0], result[1], result[2], action="show",
                    xlab=args.yvar, ylab=variables[0].varval)
        else:
            print("Wrong number of -var, either one or two")
            sys.exit(1)
    try:
        pm = PEPAModel(**pargs)
    except Exception as e:
        print("Exception occured: ", e)
        sys.exit(1)



    if args.steady or args.top or args.utilisations:
        pm.steady_state()
        print("Statespace of {} has {} states \n".format(args.file,
              len(pm.get_steady_state_vector() )))
    if args.trantime:
        tr = pm.transient(0, int(args.trantime))
        print("Transient analysis from time %d to %d" % (0, args.trantime))
        args.output = "{}-transient.csv".format(pm.name)
        pretty_print_vector(tr,
                             pm.get_state_names(),
                             fmt=args.format,
                             outfile=args.output
                             )
    if args.steady:
        print("Steady state vector")
        args.output = "{}-steady.csv".format(pm.name)
        pretty_print_vector(pm.get_steady_state_vector(),
                             pm.get_state_names(),
                             fmt=args.format,
                             outfile=args.output
                             )
    if args.utilisations:
        print ("Steady State utilisations")
        args.output = "{}-utilisations.csv".format(pm.name)
        pretty_print_utilisations(pm.get_utilisations(),
                                  fmt=args.format,
                                  outfile=args.output
                                 )
    if args.top:
        print("Throuhoutput (successful action completion in a time unit)")
        print("Output:{}".format(args.format))
        args.output = "{}-throughput.csv".format(pm.name)
        pretty_print_performance(pm.get_throughoutput(), fmt=args.format,
                                                         outfile=args.output)


if __name__ == "__main__":
    main()
