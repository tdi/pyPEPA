#!/usr/bin/env python

import logging
import sys
from pprint import pprint
from ComponentSSGraph import Transition, ModelSSGraph, ComponentState
from PEPAAst import *
from derivation.StateSpace import StateSpace, Operator, Component


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
        self.operators = []
        self.components = []
        self.ss = StateSpace()

    def derive_processes_ss(self, node):
        """ Takes node returns state space of a single
            process (here process is P = (a,r).P;
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
        self.operators = []
        self.components = []
        self._visit_systemeq(node)
        self.graph.shared_actions = self.shared_actions
        self.ss.operators = self.operators
        self.ss.components = self.components
        return self.ss

    def _visit_systemeq(self, node):
        """ Every procdef in system equation gets offset number
            describing the position in a system equation.
            Additionally every node gets length, which is the sum of
            lengths of its children. Leaves get length 1.
            Operators are added to operators list, whereas components to
            components.
        """
        if node.asttype == "procdef":
            c = Component(self.graph.ss, node.data, len(self.components))
            c.length = 1
            if self.ss.max_length < c.length:
                self.ss.max_length = c.length
#            c.offset = len(self.components)
            # TODO zmienic, to redundantne i idiotyczne
            c.data = node.data
            node.length = 1
            node.offset = len(self.components)
            self.components.append(c)
            #self.components.append(node)
        if node.asttype != "procdef":
            c = Operator()
            c.actionset = list(node.actionset) if node.actionset is not None else []
            self.operators.append(c)
        if node.left is not None:
            l = self._visit_systemeq(node.left)
            c.lhs = l
        if node.right is not None:
            r = self._visit_systemeq(node.right)
            c.rhs = r
        if node.asttype != "procdef":
            c.length = l.length + r.length
            if self.ss.max_length < c.length:
                self.ss.max_length = c.length
            node.length = node.left.length + node.right.length
        return c


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
        if node.data == "=":
            # create new node, we are in the first node of AST
            compnode = ComponentState()
            compnode.name = node.process
            compnode.resolved = node.resolved
            # adding to ss dict
            self.graph.ss[node.process] = compnode
            self.graph.firstnodes.append( node.process )
            # first node for sure
            self.log.debug("(COMPONENT) " + node.process + " = " + node.resolved)
            self._visitstack.append(node.process)
        elif node.data == ".":
            trans = Transition(node.action, node.rate, node.resolved)
            # add transition to the last state (in the graph)
            self.graph.ss[self._visitstack[-1]].transitions.append( trans )
            self.log.debug("(TR) " + self._visitstack[-1] + " -(" + node.action +","+ node.rate +")-> " + node.resolved)
            # new state again, but if it exists...
#            self.log.debug("(NS) " +  node.resolved)
            if node.resolved not in self.graph.ss:
                # new state - append
                compnode = ComponentState()
                compnode.resolved = node.resolved
                self.graph.ss[node.resolved] = compnode
#            print("Appending " + node.resolved)
            self._visitstack.append(node.resolved)
        elif node.data == "+":
            pass
        if node.left is not None:
            self._visit_tree2(node.left)
        if node.right is not None:
            self._visit_tree2(node.right)
        if node.data !="+":
            self._visitstack.pop()


