#!/usr/bin/env python
from collections import namedtuple
import sys

_vartup = namedtuple("VarTup", "vartype, varval, modtype, modval")

# rate:nazwa:mode:costam
def decode_variables(variables):
    varlist = []
    for var in variables:
        split = var.split(":")
        if split[0] != "rate" or split[2] not in ["list", "range"]:
            print("Invalid arguments")
            sys.exit(1)
        varlist.append(_vartup(split[0], split[1], split[2], split[3]))
    return varlist

def pretty_print_performance(actset, fmt="console", outfile="throughoutput.csv"):
    if fmt == "console" or fmt == "graph":
        for perf in actset:
            print("{0:<40} {1:>10}".format(perf[0],perf[1]) )
    elif fmt == "csv":
        with open(outfile, "w") as f:
            f.write("Rate name;Rate throughput\n")
            for perf in actset:
                f.write("{};{}\n".format(perf[0],perf[1]))


def pretty_print_vector(vect, vect_names, fmt="console", outfile="steady.csv"):
    if fmt == "console" or fmt == "graph":
        for i, prob in enumerate(vect):
            print("{};{};{}".format(i+1, vect_names[i], vect[i]))
    elif fmt == "csv":
        with open(outfile, "w") as f:
            f.write("State number;State name;result\n")
            for i, prob in enumerate(vect):
                f.write("{};{};{}\n".format(i+1, vect_names[i], vect[i]))



