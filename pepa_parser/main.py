from pepa_parser import *
from CSPAst import tree_walker

if __name__=="__main__":
   with open("lan4.pepa","r") as f:
         try:
             model = PEPAparse(f.read())
             print("============= >> SEQ Procs TREE << ===============")
             for key in model.processes.keys():
                 tree_walker(model.processes[key])
             print("============= >> System EQ TREE << ===============")
             tree_walker(model.systemeq)
         except ParseException as e:
            print("LLALLAAA")
            error(e)
