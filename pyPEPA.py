#!/usr/bin/env python
__author__= "Dariusz Dwornikowski"
__email__ = "dariusz.dwornikowski@cs.put.poznan.pl"
__version__ = "0.3"

""" Main file for pyPEPA """

from pprint import pprint
from libpepa import __version__ as libpepa_version
from libpepa import PEPAModel
from libpepa.utils import pretty_print_vector, pretty_print_performance
from libpepa.experiments.experiment import rate_experiment, range_maker,\
                                            rate_experiment_two
from libpepa.experiments.graphing import plot_2d, plot_3d
from libpepa.logger import init_log
import argparse
import sys


if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="pyPEPA v{}, libpepa v{},"
                                     " author {}, {}".format(__version__,
                                     libpepa_version,__author__, __email__))
    gen_args = parser.add_argument_group("General", "General arguments")
    gen_args.add_argument("--log", action="store", dest="loglevel", 
                          choices=["DEBUG", "INFO", "ERROR", "NONE"], 
                          help="logging level",
                          default="NONE", type=str)
    sol_args = parser.add_argument_group("Solution",
                                         "Solution related commands")
    exp_args = parser.add_argument_group("Experimentations",
                                         "Experimentations")

    sol_args.add_argument("-s", "--solver", action="store",
                          dest="solver",type=str,
                          choices=['direct', 'sparse'],
                          help="choose solver type DEFAULT: sparse",
                          default="sparse")
    output_args = parser.add_argument_group("Output", "Output based options")
    parser.add_argument("file", help="path to the model file")
    output_args.add_argument("-gd", "--generate_dots",
                             help="generate a Graphviz dot file for every"
                                  "sequential component in a GENDOTS folder.",
                             action="store", dest="gendots", type=str)
    output_args.add_argument("-st", "--steady",
                             help="print steady state probability vector",
                             action="store_true")
    output_args.add_argument("-th", "--performance",
                             help="print throughoutput of actions",
                             action="store_true", dest="top")
    output_args.add_argument("-tr", "--transient",
                             help="print throughoutput of actions",
                             action="store", dest="trantime", type=int)
    # output_args.add_argument("-ut", "--utilization",
                               # help="print utilization of action",
                               # action="store_true", dest="util")
    output_args.add_argument("-f", "--format", dest="format", type=str,
                             choices=["graph", "console", "csv"],
                             help="format for -st -th -varrate", default="console")
    output_args.add_argument("-o", "--output", dest="output", type=str,
                               action=store,
                              help="output file valid when format cvs")

    exp_args.add_argument("-vr", "--varrate",
                          help="varyin rate name", dest="varrate",
                          action="store", metavar="ratename")
    exp_args.add_argument("--range",
                          help="\"START,STOP,STEP\" e.g. \"1.0,10,0.1\"",
                          dest="range", action="store", metavar="range")
    exp_args.add_argument("--list", help="List of values e.g. \"1,2,3,5.0,4\"",
                          dest="list_range", action="store", metavar="list")
    exp_args.add_argument("--actionth",
                          help="throughoutput of action on the Y axis",
                          dest="actionth", action="store",
                          metavar="action name")
    exp_args.add_argument("--actionth2",
                          help="throughoutput of the second action on the Z"
                               "axis, if this is given 3d graph is created",
                          dest="actionth2", action="store",
                          metavar="action name")

    args = parser.parse_args()

    logger = init_log(log_level=args.loglevel)
    pargs = {"file": args.file, "solver" : args.solver}
    if args.gendots:
        pm = PEPAModel(**pargs)
        import os
        if os.path.isdir(args.gendots):
            pass
        else:
            os.makedirs(args.gendots)
        pm.derive()
        pm.generate_dots(args.gendots)
        sys.exit(0)

    # mutual exclusion
    if args.list_range and args.range:
        print("Cannot use range and list")
        sys.exit(1)
    if args.varrate:
        ratename = args.varrate
        if args.actionth is None:
            print("Action name not given")
            sys.exit(1)
        if args.range:
            rran = args.range.split(",")
            if len(rran) != 3:
                print("Range should be START, STOP, STEP")
                sys.exit(1)
            start, stop, step = rran[0], rran[1], rran[2]
            ran = range_maker(float(start), float(stop), float(step))
            pm = PEPAModel(**pargs)
            pm.derive()
            if args.actionth2 is None:
                result = rate_experiment(ratename, ran, args.actionth, pm)
                if args.format == "graph":
                    plot_2d(result[0], result[1], lw=2, action="show",
                            xlab=ratename, ylab=args.actionth)
                elif args.format == "csv":
                    with open("varrate-thr-{}-{}.csv"
                              .format(ratename, args.actionth), "w") as exp_f:
                        exp_f.write("{}, {}\n".format(ratename, args.actionth))
                        x,y  = result[0], result[1]
                        for i in range(0, len(x)):
                            exp_f.write("{}, {}\n".format(x[i], y[i]))
            else:
                result = rate_experiment_two(ratename, ran, args.actionth,
                                             args.actionth2, pm)
                if args.format == "graph":
                    plot_3d(result[0], result[1], result[2], lw=2,
                            action="show", xlab=ratename, ylab=args.actionth,
                            zlab=args.actionth2)
        sys.exit(0)
 
    pm = PEPAModel(**pargs)
    pm.derive()

    if args.steady or args.top:
        pm.steady_state()
        print("Statespace of {} has {} states \n".format(args.file,
              len(pm.get_steady_state_vector() )))
    if args.trantime:
        tr = pm.transient(0,int(args.trantime))
        print("Transient analysis from time %d to %d\n" % (0, args.trantime))
        pretty_print_vector(tr, pm.get_state_names())
    if args.steady:
        print("Steady state vector")
        pretty_print_vector(pm.get_steady_state_vector(),
                             pm.get_state_names(),
                             fmt=args.format,
                             )
    if args.top:
        print("Throuhoutput (successful action completion in one time unit)\n")
        pretty_print_performance(pm.get_throughoutput())


