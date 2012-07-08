from PEPAParser import PEPAParser
from PEPATreeWalker import PEPATreeWalker

from pprint import *
import logging



if __name__=="__main__":

    logging.basicConfig(level=logging.DEBUG)
    logging.info('zaczyna sie')
    with open("test_files/simple_prop.pepa","r") as f:
         try:
             pepaparser = PEPAParser(False)
             model = pepaparser.PEPAparse(f.read())
#             print("============= >> SEQ Procs TREE << ===============")
#             for key in model.processes.keys():
#                 tree_walker(model.processes[key])
#             print("============= >> System EQ TREE << ===============")
#             tree_walker(model.systemeq)
#             print("============= >> Rates << ================")
#             for key in model.rates.keys():
#                 print(key+"="+model.rates[key])
             pprint(model.processes)
             comp = next( iter ( model.processes.values()))
             tw = PEPATreeWalker()
             graph = tw.deriveStateSpace(comp)
             pprint(graph.name)

#             tw.deriveDot(comp)
#             print(tw.dotstack)

         except ParseException as e:
            print("LLALLAAA")

