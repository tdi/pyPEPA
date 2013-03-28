#!/usr/bin/env python

def pretty_print_performance(actset):
    for perf in actset:
        print("{0:<40} {1:>10}".format(perf[0],perf[1]) )

def pretty_print_vector(vect, vect_names):
    print("Using ; delimiter")
    for i, prob in enumerate(vect):
        print("{};{};{}".format(i+1, vect_names[i], vect[i]))
