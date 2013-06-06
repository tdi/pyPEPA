#/usr/bin/env python
import sys
from pypepa.logger import init_log
from pypepa.parsing.pepa_treewalker import PEPATreeWalker
from pypepa.parsing.comp_state_space_graph import ComponentSSGraph
from pypepa.parsing.parser import PEPAParser
from pypepa.solvers.solution import CTMCSolution
from pypepa.parsing.component_state_visitor import ComponentStateVisitor
import os

class PEPAModel():
    """
        Representation of a final PEPA model, everything needed to derive CTMC
        - state spaces of components that are present in a system equation
        - rate definitions
        - system equation
    """
    def __init__(self, **kwargs):
        """ Create PEPA model instance and fill the fields """
        self.args = kwargs
        self.processes = {}
        self.systemeq = None
        self.rate_definitions = {}
        self.components = {}
        # from BU alg, get rid of it
        self.tw = None
        self.ss = None
        self.log = init_log()
        self._solver = None
        self.log.info("Starting got args {}".format(kwargs))
        self.name = os.path.basename(kwargs["file"])
        self._parse_read_model(kwargs["file"])

    def get_rates(self):
        return self.rate_definitions

    def derive(self, force=False):
        # Rather than having logic for when you have and have not
        # derived the state space outside of this module, instead we
        # can simply have all procedures which require it call this
        # method. So, this method lazily only calls the statespace
        # if it hasn't been called previously. We have a force argument to
        # force it to be recomputed should we ever require that, but
        # frankly in that case it would easier just to create a new
        # PEPAModel.
        if self.ss is None or force:
          self._prepare_components()

    def recalculate(self, rates=None):
        self._parse_read_model(self.args["file"])
        self._prepare_components(rates)

    def steady_state(self):
        self._derive_steady_state()

    def transient(self, timestop, timestart=0):
        self.derive()
        self.ss.comp_ss = self.tw.graph.ss
        self._solver = CTMCSolution(self.ss, self.args["solver"])
        return self._solver.solve_transient(timestop, timestart)

    def get_steady_state_vector(self):
        return self._solver.get_steady_state_vector()

    def get_state_names(self):
        return self._solver.get_vect_names()

    def get_throughoutput(self):
        return self._solver.get_actions_throughoutput()

    def _derive_steady_state(self):
        """ Derives global state space """
        self.derive()
        self.ss.comp_ss = self.tw.graph.ss
        self._solver = CTMCSolution(self.ss, self.args["solver"])
        self._solver.solve_steady()

    def _parse_read_model(self, modelfile):
        """ Reads model file and parses it."""
        with open(modelfile, "r") as f:
            modelfile = f.read()
        try:
            parser = PEPAParser()
            (self.processes, self.rate_definitions,
            self.systemeq, self.actions) = parser.parse(modelfile)
        except Exception as e:
            self.log.debug(e)
            print("Parsing error : " + str(e) )
            raise
            sys.exit(1)

    def _prepare_components(self, rateDef=None):
        """ Here ss graphs of every process is derived from AST trees
            as well as state space of components is derived
        """
        if rateDef is None:
            self.tw = PEPATreeWalker(self.rate_definitions)
        else:
            self.log.info("Deriving model with changed rates {}"
                          .format(rateDef))
            self.tw = PEPATreeWalker(rateDef)
        for node in self.processes.values():
            self.tw.derive_process_state_space(node, self.rate_definitions)
        self.ss = self.tw.derive_systemeq(self.systemeq)

    def generate_dots(self, out_dir = "dots"):
        """
        Generates dot files to a specified directory.
        The best application to browse dot files interactively is xdot.
        pip install xdot
        """
        self.log.info("Generating dot files in: %s" % out_dir)
        self.derive()
        visitor = ComponentStateVisitor(self.tw.graph, output_dir = out_dir)
        for comp in set(self.ss.components):
            comptmp = ComponentSSGraph(comp.data)
            self.components[comp.data] = visitor.generate_ss(comp.data,
                                                             comptmp)
        for comp in set(self.ss.components):
            visitor.get_dot(comp.data)





