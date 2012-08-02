#!/usr/bin/env python

from pprint import pprint
import logging
from PEPAModel import PEPAModel

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

#    pm = PEPAModel("test_files/simple.pepa")
#    pm = PEPAModel("test_files/browser.pepa")
     #pm = PEPAModel("test_files/REG_simple.pepa"
    pm = PEPAModel("test_files/car_scenario.pepa")
#    pm = PEPAModel("test_files/lan4.pepa")
#    pm = PEPAModel("test_files/test1_coop.pepa")
#    pm = PEPAModel("test_files/sri.pepa")
    pm.generate_dots()

    # print("Seq processes")
    # for proc in pm.seq_processes.keys():
    #     print(proc + " Number in SEQ"+str (pm.seq_processes[proc] ))
    # for c in pm.components.keys():
    #     print(pm.components[c].name)
    #     print("Shared")
    #     pprint(pm.components[c].shared)
    #     print("Activities")
    #     pprint(pm.components[c].activities)


