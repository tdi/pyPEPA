#!/usr/bin/env python

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
    fmt == "console" and print("Using ; delimiter")
    if fmt == "console" or fmt == "graph":
        for i, prob in enumerate(vect):
            print("{};{};{}".format(i+1, vect_names[i], vect[i]))
    elif fmt == "csv":
        with open(outfile, "w") as f:
            f.write("State number;State name;result\n")
            for i, prob in enumerate(vect):
                f.write("{};{};{}\n".format(i+1, vect_names[i], vect[i]))



