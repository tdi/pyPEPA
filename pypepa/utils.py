#!/usr/bin/env python
from collections import namedtuple
import sys

_vartup = namedtuple("VarTup", "vartype, varval, modtype, modval")

def decode_variables(variables):
    varlist = []
    for var in variables:
        split = var.split(":")
        if split[0] != "rate" or split[2] not in ["list", "range"]:
            print("Invalid arguments")
            sys.exit(1)
        varlist.append(_vartup(split[0], split[1], split[2], split[3]))
    return varlist

class Bunch:
    """The bunch recipe, this allows you to create simple objects with
       named attributes, eg. "Bunch(x=1, y=2)" or you could do:
       point = Bunch()
       point.x = 1
       point.y = 2
    """
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class OutputFile(object):
   """A simple output file class to allow us to use the 'with' syntax for all
      pretty print methods below, even when outputting to the console.
      We wouldn't even need this were it not for the fact that __exit__ calls
      close on the file value by default, hence we would otherwise call close on
      sys.stdout. Even this would be fine if users only ever did one kind of
      analysis, but since a user might do "pypepa myfile.pepa -st -ut -th" we
      require this simple class to avoid closing the stdout after the pretty
      printing of the first results.
   """
   def __init__(self, fmt, outfile):
       self.fmt = fmt
       self.outfile = outfile

   def __enter__(self):
       self.file = open(self.outfile, "w") if self.fmt == "csv" else sys.stdout
       return self.file

   def __exit__(self, arg1, arg2, arg3):
       if self.fmt == "csv":
           self.file.close()

def pretty_print_performance(actset, fmt="console", outfile="throughoutput.csv"):
    with OutputFile(fmt, outfile) as f:
      f.write("# Rate name; Rate throughput\n")
      for perf in actset:
          f.write("{0:<40} {1:>10}\n".format(perf[0],perf[1]) )

def pretty_print_vector(vect, vect_names, fmt="console", outfile="steady.csv"):
    with OutputFile(fmt, outfile) as f:
      f.write("# State number; State name; Result\n")
      for i, prob in enumerate(vect):
        f.write("{};{};{}\n".format(i+1, vect_names[i], vect[i]))

def pretty_print_utilisations(utilisations, fmt="console", outfile="utilisations.csv"):
    with OutputFile(fmt, outfile) as f:
        for (i, component_utils) in enumerate(utilisations):
           f.write("# States for component:{}\n".format(i))
           for state_name, utilisation in component_utils.items():
               f.write("    {};{}\n".format(state_name, utilisation))

