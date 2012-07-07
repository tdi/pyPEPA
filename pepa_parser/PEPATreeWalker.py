from PEPAAst import *

class PEPATreeWalker():
    """ Various AST Tree methods to generate state spaces
    """
    def __init__(self):
        self._visitstack= []
        self.logging = False

    def log(self,string, msg="",prepend="log"):
        if self.logging:  print(prepend,msg,string)

    def deriveStateSpace(self, node):
        """ Takes node returns state space of a singl
            component
        """
        node = self.visit_tree1(node)
        self._visitstack = []
        self.visit_tree2(node)

    def _name_subtree(self,node):
        """ Names the subtree
        """
        current = ""
        lcurrent,rcurrent = "",""

        if node.left is not None:
            lcurrent+=self._name_subtree(node.left)
        if node.right is not None:
            rcurrent+=self._name_subtree(node.right)
        current = lcurrent + node.data + rcurrent
        return current

    def visit_tree1(self,node):
        if node.data == "=":
            node.process = node.left.data
            node.resolved = self._name_subtree(node.right)
            node.left = None
        elif node.data == ".":
            node.action = node.left.data
            node.resolved = self._name_subtree(node.right)
            node.left = None
            if node.right.asttype == "procdef":
                #  the end of the tree
                node.right = None
        elif node.data == "+":
            node.resolved = self._name_subtree(node)
            node.lhs = self._name_subtree(node.left)
            node.rhs = self._name_subtree(node.right)
        elif node.asttype == "procdef":
            pass
        elif node.asttype == "activity":
            pass
        if node.left is not None:
            self.visit_tree1(node.left)
        if node.right is not None:
            self.visit_tree1(node.right)
        return node

    def visit_tree2(self,node):
#        global visitstack
#        global graph
        if node.data == "=":
            graph = ProcessGraph(node.process)
            print("append(NS) " + node.process + " =" + node.resolved)
            self._visitstack.append(node.resolved)
        elif node.data == ".":
            print("trans from " + self._visitstack[-1] + " do " + node.resolved)
            print("append(NS) "  + node.resolved)
            self._visitstack.append(node.resolved)
        elif node.data == "+":
    #        print("JESTEM W "+node.resolved)
            pass
        if node.left is not None:
            self.visit_tree2(node.left)
        if node.right is not None:
            self.visit_tree2(node.right)
        if node.data != "=":
            self._visitstack.pop()




