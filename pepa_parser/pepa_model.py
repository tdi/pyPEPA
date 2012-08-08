#/usr/bin/env python
import logging
import sys
from parsing.pepa_treewalker import PEPATreeWalker
from parsing.comp_state_space_graph import ComponentSSGraph
from pylab import figure, axes,pie,title, show
from parsing.parser import PEPAParser
from solvers.solution import CTMCSolution
from parsing.component_state_visitor import ComponentStateVisitor

class PEPAModel():
    """
        Representation of a final PEPA model, everything needed to derive CTMC
        - state spaces of components that are present in a system equation
        - rate definitions
        - system equation
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
        self.log = logging.getLogger(__name__)
        self.ss = None
        self._solver = None
        self._parse_read_model(args.file)
        self._prepare_trees()
        self._prepare_systemeq()
        self._derive_steady_state()


    def get_steady_state_vector(self):
        return self._solver.get_steady_state_vector()

    def get_throughoutput(self):
        return self._solver.get_actions_throughoutput()

    def _derive_steady_state(self):
        """ Derives global state space """
        self.ss.comp_ss = self.tw.graph.ss
        self._solver = CTMCSolution(self.ss)

#        (res,actset) = self.ss.derive()
#        steady = (ctmc(create_matrix(res)))
#        print("Statespace has " + str(len(steady)) + " states")
#        print("Throughoutput")
        # act_vectors = {}
        # for (action,state) in actset.keys():
        #     if action not in act_vectors:
        #         act_vectors[action] = [0] * len(steady)
        #     act_vectors[action][state-1] = actset[ (action, state) ]
        # for action in act_vectors.keys():
        #     print(action + "\t" +  str ( vector_mult(steady, act_vectors[action])) )

    def _generate_components(self):
        """
        Generates state space graphs for every component
        in the model into components dict
        """
        visitor = ComponentStateVisitor(self.tw.graph)
        for comp in set(self.ss.components):
            self.components[comp.data] = ComponentSSGraph(comp.data)
            self.components[comp.data] = visitor.generate_ss(comp.data, self.components[comp.data])

    def _prepare_systemeq(self):
        """
        Returns StateSpace object
        """
        self.log.debug("Preparing systemeq")
        self.ss = self.tw.derive_systemeq(self.systemeq)

    def _parse_read_model(self, modelfile):
        """ Reads model file and parses it.
        """
        with open(modelfile, "r") as f:
            modelfile = f.read()
        try:
            parser = PEPAParser(False)
            (self.processes, self.rate_definitions, self.systemeq) = parser.parse(modelfile)
            self.tw = PEPATreeWalker(self.rate_definitions)
        except Exception as e:
            self.log.debug(e)
            print("Parsing error : " + str(e) )
            sys.exit(1)

    def _prepare_trees(self):
        """ Here ss graphs of every process is derived from AST trees
        """
        for node in self.processes.values():
            self.tw.derive_processes_ss(node, self.rate_definitions)

    def generate_dots(self):
        """ Generates dot files to browse with e.g. xdot """
        self._generate_components()
        visitor = ComponentStateVisitor(self.tw.graph)
        for comp in set(self.ss.components):
            visitor.get_dot(comp.data)



