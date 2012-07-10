#!/usr/bin/env python
import logging
from pprint import pprint
import sys
from PEPATreeWalker import PEPATreeWalker
from PEPAParser import PEPAParser
from pyparsing import ParseException

class SS():
    pass

class PEPAModel():

    def __init__(self, modelfile):
        self.processes = {}
        self.systemeq = None
        self.rates = {}
        self.tw = PEPATreeWalker()
        self.log = logging.getLogger(__name__)
        self._parse_read_model(modelfile)
        self._prepare_systemeq()

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
            parser = PEPAParser(True)
            (self.processes, self.rates, self.systemeq) = parser.parse(modelfile)
        except ParseException as e:
            self.log.debug(e)
            print("Parsing error : " + e.msg )
            sys.exit(1)

    def _prepare_trees(self):
        for node in self.processes.values():
            self.tw.derive_processes(node)
        self.tw.derive_whole_ss()




