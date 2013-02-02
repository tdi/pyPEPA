#/usr/bin/env python
import sys
from libpepa.logger import init_log
from parsing.pepa_treewalker import PEPATreeWalker
from parsing.comp_state_space_graph import ComponentSSGraph
from parsing.parser import PEPAParser
from solvers.solution import CTMCSolution
from parsing.component_state_visitor import ComponentStateVisitor

class PEPAModel():
    """
        Representation of a final PEPA model, everything needed to derive CTMC
        - state spaces of components that are present in a system equation
        - rate definitions
        - system equation
        TODO: keyword arguments
    """
    def __init__(self, args):
        """ Create PEPA model instance and fill the fields

        Keyword arguments:
        modelfile --- path to the model file
        """
        self.args = args
        self.processes = {}
        self.systemeq = None
        self.rate_definitions = {}
        self.components = {}
        # from BU alg, get rid of it
        self.tw = None
        self.ss = None
        self.log = init_log()
        self._solver = None
        self.log.info("Starting got args {}".format(args))
        self._parse_read_model(args["file"])

    def get_rates(self):
        return self.rate_definitions

    def derive(self):
        self._prepare_components()

    def recalculate(self, rates=None):
        self._parse_read_model(self.args["file"])
        self._prepare_components(rates)

    def steady_state(self):
        self._derive_steady_state()

    def transient(self, timestop, timestart=0):
        self.ss.comp_ss = self.tw.graph.ss
        self._solver = CTMCSolution(self.ss, self.args["solver"])
        self._solver.solve_transient(timestop, timestart)

    def get_steady_state_vector(self):
        return self._solver.get_steady_state_vector()

    def get_state_names(self):
        return self._solver.get_vect_names()

    def get_throughoutput(self):
        return self._solver.get_actions_throughoutput()

    def _derive_steady_state(self):
        """ Derives global state space """
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
            self.systemeq) = parser.parse(modelfile)
        except Exception as e:
            raise
            self.log.debug(e)
            print("Parsing error : " + str(e) )
            sys.exit(1)

    def _prepare_components(self, rateDef=None):
        """ Here ss graphs of every process is derived from AST trees
            as well as state space of components is derived
        """
        if rateDef is None:
            self.tw = PEPATreeWalker(self.rate_definitions)
        else:
            self.log.info("Deriving model with changes rates {}"
                          .format(rateDef))
            self.tw = PEPATreeWalker(rateDef)
        for node in self.processes.values():
            self.tw.derive_process_state_space(node, self.rate_definitions)
        self.ss = self.tw.derive_systemeq(self.systemeq)

    def generate_dots(self, out_dir = "dots"):
        """
        Generates dot files to browse with e.g. xdot to a
        specified directory
        """
        self.log.info("Generating dot files")
        self._generate_components()
        visitor = ComponentStateVisitor(self.tw.graph, output_dir = out_dir)
        for comp in set(self.ss.components):
            visitor.get_dot(comp.data)

    def _generate_components(self):
        """
        Generates state space graphs for every component
        in the model into components dict
        TODO: wywalic, uzywane jedynie do testow oraz generowania dotow
        """
        visitor = ComponentStateVisitor(self.tw.graph)
        for comp in set(self.ss.components):
            self.components[comp.data] = ComponentSSGraph(comp.data)
            self.components[comp.data] = visitor.generate_ss(comp.data, self.components[comp.data])



