from PEPAAst import *
import logging
from ComponentSSGraph import *

class PEPATreeWalker():
    """ Various AST Tree methods to generate state spaces
    """
    def __init__(self):
        self._visitstack= []
        self.dotstack  = ""
        self.graph = None
        self.log = logging.getLogger(__name__)

    def deriveDot(self, node):
        self.log.debug('Starting')
        self.dotstack = "digraph test {\n"
        node = self._visit_tree1(node)
        self._visitstack = []
        self._visit_tree2(node)
        self.dotstack += "\n}"

    def deriveStateSpace(self, node):
        """ Takes node returns state space of a singl
            component
        """
        node = self._visit_tree1(node)
        self._visitstack = []
        # creating SS graph fo the component
        self.graph = ComponnetSSGraph()
        # assign name from the first node, which is DefNode with field name
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

    def _visit_tree1(self,node):
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
            self._visit_tree1(node.left)
        if node.right is not None:
            self._visit_tree1(node.right)
        return node

    def _visit_tree2(self,node):
        if node.data == "=":
            # create new node, we are in the first node of AST
            compnode = ComponentState()
            compnode.name = node.process
            compnode.resolved = node.resolved
            # adding to ss dict
            self.graph.ss[node.process] = compnode
            self.graph.firstnode = node.process
            # first node for sure
            self.log.debug("append(NS) " + node.process + " =" + node.resolved)
            self._visitstack.append(compnode)
        elif node.data == ".":
            trans = Transition(node.action, node.action, node.resolved)
            # add transition to the last state (in the graph)
            if self._visitstack[-1].name is not None:
                self.graph.ss[self._visitstack[-1].name].transitions = trans
            else:
                self.graph.ss[self._visitstack[-1].resolved].transitions = trans
            self.log.debug("trans from " + self._visitstack[-1].resolved + " do " + node.resolved)
            self.log.debug("append(NS) "  + node.resolved)
            # new state again
            compnode = ComponentState()
            compnode.resolved = node.resolved
            self.graph.ss[node.resolved] = compnode
            self._visitstack.append(compnode)
        elif node.data == "+":
            pass
        if node.left is not None:
            self._visit_tree2(node.left)
        if node.right is not None:
            self._visit_tree2(node.right)
        if node.data != "=":
            # if in = again, do not pop
            self._visitstack.pop()


