#!/usr/bin/env python
import logging
from pprint import pprint
import sys
from PEPATreeWalker import PEPATreeWalker
from PEPAParser import PEPAParser
from pyparsing import ParseException

class SS():
    pass

class ComponentStateVisitor():

    def __init__(self, graph):
        self.graph = graph
        self.visited = []

    def visit_print(self, node):
        self.visited.append(node)
        transitions = self.graph.ss[node].transitions
        for tran in transitions:
            print(node + " -> " + tran.to)
            if tran.to not in self.visited:
                self.visit_print(tran.to)


class PEPAModel():
    """
        param modelfile is a path to a file with pepa model
    """
    def __init__(self, modelfile):
        self.processes = {}
        self.systemeq = None
        self.rates = {}
        self.seq_processes = {}
        self.tw = PEPATreeWalker()
        self.log = logging.getLogger(__name__)
        self._parse_read_model(modelfile)
        self._prepare_systemeq()
        self._prepare_trees()

    def _prepare_systemeq(self):
        self.log.debug("Preparing systemeq")
        self.seq_processes = self.tw.derive_systemeq(self.systemeq)

    def _parse_read_model(self, modelfile):
        """ Reads model file and parses it.
            In case of the parse error, an exception is risen
        """
        modfile = None
        with open(modelfile, "r") as f:
            modelfile = f.read()
        try:
            parser = PEPAParser(False)
            (self.processes, self.rates, self.systemeq) = parser.parse(modelfile)
        except ParseException as e:
            self.log.debug(e)
            print("Parsing error : " + e.msg )
            sys.exit(1)

    def _prepare_trees(self):
        """ Here ss graphs of every process is derived from AST trees
        """
        for node in self.processes.values():
            self.tw.derive_processes_ss(node)
        visitor = ComponentStateVisitor(self.tw.graph)
        for comp in self.seq_processes.keys():
            self.log.debug("Deriving for component: " + comp)
            visitor.visit_print(comp)




