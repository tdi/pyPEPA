#!/usr/bin/env python

import logging
import sys
from pprint import pprint
from ComponentSSGraph import *
from PEPAAst import *


class PEPATreeWalker():
    """ Various AST Tree methods to generate state spaces
    """
    def __init__(self):
        self._visitstack= []
        self.graph = ModelSSGraph()
        self.log = logging.getLogger(__name__)
        self._after_1_visit = None
        self.seq_components = {}
        self.shared_actions = {}
        self.global_start_state = []

    def derive_processes_ss(self, node):
        """ Takes node returns state space of a single
            component
        """
        node = self._visit_tree1(node)
        self._after_1_visit = node
        self._visitstack = []
        self.graph.name = node.process
        self.log.debug("Deriving " + node.process)
        self._visit_tree2(node)
        return self.graph

    def _name_subtree(self,node):
        """ Names the subtree
        """
        current = ""
        lcurrent,rcurrent = "",""

        if node.left is not None:
            if node.left.asttype in ("choice", "prefixx"):
                lcurrent += "("
                lcurrent +=  self._name_subtree(node.left)
                lcurrent += ")"
            else:
                lcurrent +=  self._name_subtree(node.left)
        if node.right is not None:
            if node.right.asttype in ("choice", "prefixx"):
                rcurrent += "("
                rcurrent += self._name_subtree(node.right)
                rcurrent += ")"
            else:
                rcurrent += self._name_subtree(node.right)
        current = lcurrent + node.data + rcurrent
        return current


    def derive_systemeq(self, node):
        """ API function for generating state space of a process (node)"""
        self._visit_systemeq(node)
        self.graph.shared_actions = self.shared_actions
        return (self.seq_components, self.global_start_state)

    def _visit_systemeq(self, node):
#        print("NIO"+node.data)
        if node.asttype == "coop" and node.cooptype is not "par":
            for action in node.actionset:
                if action != "<>":
                    self.shared_actions[action]=""
        elif node.asttype == "procdef":
            if node.data in self.seq_components:
                self.global_start_state.append(node.data)
                self.seq_components[node.data] += 1
            else:
                self.global_start_state.append(node.data)
                self.seq_components[node.data] = 1
        if node.left is not None:
            self._visit_systemeq(node.left)
        if node.right is not None:
            self._visit_systemeq(node.right)



    def _visit_tree1(self,node):
        """
        Walk the AST tree for the first time to reduce the tree.
        TODO: merge with _visit_tree2
        """
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
        print(node.data)
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
            print("Appending = "+node.process)
            self._visitstack.append(node.process)
            print(self._visitstack)
        elif node.data == ".":
            trans = Transition(node.action, node.rate, node.resolved)
            # add transition to the last state (in the graph)
            self.graph.ss[self._visitstack[-1]].transitions.append( trans )
            self.log.debug("(TR) " + self._visitstack[-1] + " -(" + node.action +","+ node.rate +")-> " + node.resolved)
            # new state again, but if it exists...
            self.log.debug("(NS) " +  node.resolved)
            if node.resolved not in self.graph.ss:
                # new state - append
                compnode = ComponentState()
                compnode.resolved = node.resolved
                self.graph.ss[node.resolved] = compnode
            self._visitstack.append(node.resolved)
            print("Appending "+node.resolved)
            print(self._visitstack)
        elif node.data == "+":
            pass
        if node.left is not None:
            self._visit_tree2(node.left)
        if node.right is not None:
            self._visit_tree2(node.right)
        if not self._visitstack:
            self._visitstack.pop()


