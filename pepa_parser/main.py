#!/usr/bin/env python

from pprint import pprint
import logging
from PEPAModel import PEPAModel

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    logging.info('zaczyna sie')
#    pm = PEPAModel("test_files/simple_prop.pepa")
    pm = PEPAModel("test_files/comparison.pepa")
    # pm.generate_dots()
    # print("Seq processes")
    # for proc in pm.seq_processes.keys():
    #     print(proc + " Number in SEQ"+str (pm.seq_processes[proc] ))
    # for c in pm.components.keys():
    #     print(pm.components[c].name)
    #     print("Shared")
    #     pprint(pm.components[c].shared)
    #     print("Activities")
    #     pprint(pm.components[c].activities)


