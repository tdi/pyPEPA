from pepa_parser import *
from pprint import *
from PEPATreeWalker import PEPATreeWalker
from colorama import Fore, Back, Style



if __name__=="__main__":
   with open("test_files/simple.pepa","r") as f:
         try:
             pepaparser = PEPAParser(True)
             model = pepaparser.PEPAparse(f.read())
#             print("============= >> SEQ Procs TREE << ===============")
#             for key in model.processes.keys():
#                 tree_walker(model.processes[key])
#             print("============= >> System EQ TREE << ===============")
#             tree_walker(model.systemeq)
#             print("============= >> Rates << ================")
#             for key in model.rates.keys():
#                 print(key+"="+model.rates[key])
             print("============= >> SS << =============")
             comp = next( iter ( model.processes.values()))
             tw = PEPATreeWalker()
#             node = tw.deriveStateSpace(comp)
             tw.deriveDot(comp)
             print(tw.dotstack)

         except ParseException as e:
            print("LLALLAAA")

