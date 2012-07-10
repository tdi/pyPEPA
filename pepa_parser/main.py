from pprint import *
import logging
from PEPAModel import PEPAModel

if __name__=="__main__":

    logging.basicConfig(level=logging.DEBUG)
    logging.info('zaczyna sie')
#    pm = PEPAModel("test_files/simple_prop.pepa")
    pm = PEPAModel("test_files/passive.pepa")
    proc = pm.seq_processes
    for v in proc.keys():
        print(v)


