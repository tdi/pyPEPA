from pepa_parser import *
from CSPAst import tree_walker
from pprint import *

laststate = ""
first = True
logging = True
visitstack = []

def log(self,string, msg="",prepend="log"):
    if logging:  print(prepend,msg,string)

def name_subtree(node):
    current = ""
    lcurrent,rcurrent = "",""

    if node.left is not None:
        lcurrent+=name_subtree(node.left)
    if node.right is not None:
        rcurrent+=name_subtree(node.right)
#    if node.asttype == "activity":
#        print(node.activity)
#        data = "("+ node.activity + "," + node.rate + ")"
#        current = lcurrent + data + rcurrent
#    else:
    current = lcurrent + node.data + rcurrent
    return current

def visit_tree1(node):
    if node.data == "=":
        node.process = node.left.data
        node.resolved = name_subtree(node.right)
        #node.resolved = name_subtree(node.right)
        node.left = None
    elif node.data == ".":
        node.action = node.left.data
        node.resolved = name_subtree(node.right)
        node.left = None
        if node.right.asttype == "procdef":
            # nie ma sensu bo to koniec drzewa
            node.right = None
    elif node.data == "+":
        node.resolved = name_subtree(node)
        node.lhs = name_subtree(node.left)
        node.rhs = name_subtree(node.right)
    elif node.asttype == "procdef":
        pass
    elif node.asttype == "activity":
        pass
    if node.left is not None:
        visit_tree1(node.left)
    if node.right is not None:
        visit_tree1(node.right)
    return node

def visit_tree2(node):
    global visitstack
    if node.data == "=":
        print("append(NS) " + node.process + "resolved " + node.resolved)
        visitstack.append(node.data)
    elif node.data == ".":
        print("przejscie z " + visitstack[-1] +" do " + node.resolved)
    elif node.data == "+":
        visitstack.append(node.data)
    if node.left is not None:
        visit_tree2(node.left)
    if node.right is not None:
        visit_tree2(node.right)

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
             curstate = ""
             laststate = comp.lhs
             print("Visit1")
             node = visit_tree1(comp)
             print("Visit2")
             visit_tree2(node)
             pprint(visitstack)
             print()
         except ParseException as e:
            print("LLALLAAA")
            error(e)
