#!/usr/bin/env python

from pprint import pprint
import logging
from PEPAModel import PEPAModel

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

#    pm = PEPAModel("test_files/simple.pepa")
#    pm = PEPAModel("test_files/browser.pepa") # TEST ok
    # pm = PEPAModel("test_files/comparison.pepa") # TEST ok
    #pm = PEPAModel("test_files/REG_simple.pepa") # test OK
    pm = PEPAModel("test_files/REG-DB.pepa") # test OK
    # pm = PEPAModel("test_files/car_scenario.pepa") # test OK
#    pm = PEPAModel("test_files/lan4.pepa")
    # pm = PEPAModel("test_files/test1_coop.pepa") # Test ok
#    pm = PEPAModel("test_files/sri.pepa")
    #pm = PEPAModel("test_files/alternatingbit.pepa") # test ok
    # pm = PEPAModel("test_files/bankscenario.pepa") #
    pm.generate_dots()



