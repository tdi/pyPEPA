from PEPAAst import *
import logging
from ComponentSSGraph import *
import sys
from pprint import pprint

class PEPATreeWalker():
    """ Various AST Tree methods to generate state spaces
    """
    def __init__(self):
        self._visitstack= []
        self.dotstack  = ""
        self.graph = ComponnetSSGraph()
        self.log = logging.getLogger(__name__)
        self._after_1_visit = None
        self.seq_components = {}

    def derive_dot(self, node):
        self.dotstack = "digraph " + node.process + " {\n"
        node = self._visit_tree1(node)
        self._visitstack = []
        self._visit_fordot(node)
        self.dotstack += "\n}"
        return self.dotstack

    def _visit_fordot(self,node):
        if node.data == "=":
            self._visitstack.append(node.process)
        elif node.data == ".":
            self.dotstack += "\"" + self._visitstack[-1] + "\" ->" + "\"" + node.resolved + "\" [label=" + node.action +"]\n"
            self._visitstack.append(node.resolved)
        elif node.data == "+":
            pass
        if node.left is not None:
            self._visit_fordot(node.left)
        if node.right is not None:
            self._visit_fordot(node.right)
        if node.data != "=":
            # if in = again, do not pop
            self._visitstack.pop()

    def derive_whole_ss(self):
        ss = self.graph.ss
        for first in self.graph.firstnodes:
            self._walk_comp_ss(first)

    def _walk_comp_ss(self, node):
        if self.graph.ss[node].name is not None:
            self.log.debug("State " + self.graph.ss[node].name)
        else:
            self.log.debug("State " + self.graph.ss[node].resolved)
        # for tran in self.graph.ss[node].transitions:
        #     self.log.debug("-> " + tran.to)
        #     self._walk_comp_ss(tran.to)

    def derive_processes_ss(self, node):
        """ Takes node returns state space of a single
            component
        """
        node = self._visit_tree1(node)
        self._after_1_visit = node
        self._visitstack = []
        # creating SS graph for all bedzie
        ### self.graph = ComponnetSSGraph()
        # assign name from the first node, which is DefNode with field name
        # to be changed
        self.graph.name = node.process
        self._visit_tree2(node)
        return self.graph

    def _name_subtree(self,node):
        """ Names the subtree
        """
        current = ""
        lcurrent,rcurrent = "",""

        if node.left is not None:
            lcurrent +=  self._name_subtree(node.left)
        if node.right is not None:
            rcurrent+=self._name_subtree(node.right)
        current = lcurrent + node.data + rcurrent
        return current


    def derive_systemeq(self, node):
        self._visit_systemeq(node)
        return self.seq_components

    def _visit_systemeq(self, node):
        if node.asttype == "coop":
            pass
        elif node.asttype == "procdef":
            self.seq_components[node.data] = ""
        if node.left is not None:
            self._visit_systemeq(node.left)
        if node.right is not None:
            self._visit_systemeq(node.right)



    def _visit_tree1(self,node):
        if node.data == "=":
            node.process = node.left.data
            node.resolved = self._name_subtree(node.right)
            node.left = None
        elif node.data == ".":
            node.action = node.left.action
            node.rate = node.left.rate
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
            self._visit_tree1(node.left)
        if node.right is not None:
            self._visit_tree1(node.right)
        return node

    def _visit_tree2(self,node):
        """ Second visiting of the tree, this tree is of elements +.=
            Additionally the function creates graph
        """
        if node.data == "=":
            # create new node, we are in the first node of AST
            compnode = ComponentState()
            compnode.name = node.process
            compnode.resolved = node.resolved
            # adding to ss dict
            self.graph.ss[node.process] = compnode
            self.graph.firstnodes.append( node.process )
            # first node for sure
            self.log.debug("(NS) " + node.process + " = " + node.resolved)
            self._visitstack.append(node.process)
        elif node.data == ".":
            trans = Transition(node.action, node.action, node.resolved)
            # add transition to the last state (in the graph)
            self.log.debug("Appending1 name " + self._visitstack[-1])
            self.graph.ss[self._visitstack[-1]].transitions.append( trans )
            self.log.debug("(TR) " + self._visitstack[-1] + " -(" + node.action +","+ node.rate +")-> " + node.resolved)
            # new state again, but if it exists...
            self.log.debug("(NS) " +  node.resolved)
            compnode = ComponentState()
            compnode.resolved = node.resolved
            if node.resolved not in self.graph.ss:
                self.log.debug("New state, not yet in there" + node.resolved)
                self.graph.ss[node.resolved] = compnode
            self._visitstack.append(node.resolved)
        elif node.data == "+":
            pass
        if node.left is not None:
            self._visit_tree2(node.left)
        if node.right is not None:
            self._visit_tree2(node.right)
        if node.data != "=":
            # if in = again, do not pop
            self._visitstack.pop()


