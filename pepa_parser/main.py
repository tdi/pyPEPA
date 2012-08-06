#!/usr/bin/env python

from pprint import pprint
import logging
from pepa_model import PEPAModel
import argparse


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="pyPEPA tool, author Dariusz Dwornikowski")
    parser.add_argument("file", help="path to the model file")
    parser.add_argument("-gd", "--generate_dots", help="generate a graphviz dot file for every sequentail component.WARNING: this can be very memory consuming when the state space is big", action="store_true")
    args = parser.parse_args()

    pm = PEPAModel(args.file)


    if args.generate_dots:
        pm.generate_dots()



