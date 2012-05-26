from pepa_parser import *
from CSPAst import tree_walker

if __name__=="__main__":
   with open("test_files/comparison.pepa","r") as f:
         try:
             pepaparser = PEPAParser()
             model = pepaparser.PEPAparse(f.read())
             print("============= >> SEQ Procs TREE << ===============")
             for key in model.processes.keys():
                 tree_walker(model.processes[key])
             print("============= >> System EQ TREE << ===============")
             tree_walker(model.systemeq)
             print("============= >> Rates << ================")
             for key in model.rates.keys():
                 print(key+"="+model.rates[key])

         except ParseException as e:
            print("LLALLAAA")
            error(e)
