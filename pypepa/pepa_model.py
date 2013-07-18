#/usr/bin/env python
import collections
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
        # Set up model_filename and model_string depending upon which is
        # set in the arguments.
        self.model_filename = kwargs.get("file", None)
        self.model_string = kwargs.get("modelstring", None)

        # If 'name' is set in the kwargs then obviously that is the name of the
        # model, otherwise if there is a model filename set use that as the
        # basis for the name. If there is no name and no model filename then we
        # have little choice but to fall back on a generic default of "model"
        if self.model_filename == None:
          self.name = kwargs.get("name", "model")
        else:
          self.name = os.path.basename(kwargs.get("name", self.model_filename))

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
        self._parse_model()

    def _parse_model(self):
        """ Parses the model into the abstract syntax tree and sets the name
            of the model. Both of these depend slightly on whether we are
            parsing the model from a string or a file.
        """
        # If self.model_filename has been set then we assume that we should
        # read that in, as the file may have been updated. However we may never
        # have received a model_filename in which case we should use the
        # model_string. If neither of these two things exist we are in trouble.
        if self.model_filename:
            with open(self.model_filename, "r") as f:
                model_string = f.read()
        elif self.model_string:
            model_string = self.model_string
        else:
            raise IOError("No model file or model string present.")
        try:
            parser = PEPAParser()
            (self.processes, self.rate_definitions,
            self.systemeq, self.actions) = parser.parse(model_string)
        except:
            raise

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
        self._parse_model()
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

    def get_utilisations(self):
        """ We work out for each component a dictionary which maps the local
            states of the component to the value of its utilisation.
        """
        all_utilisations = []
        for (i, component) in enumerate(self.ss.components):
            utilisations = collections.Counter()
            name = component.name
            name_value_pairs = zip(self.get_state_names(), 
                                   self.get_steady_state_vector())
            for (state_name, steady_vector_value) in name_value_pairs:
                comp_state = state_name.split(",")[i]
                utilisations[comp_state] += steady_vector_value
            all_utilisations.append(utilisations)
        return all_utilisations

    def get_throughoutput(self):
        return self._solver.get_actions_throughoutput()

    def _derive_steady_state(self):
        """ Derives global state space """
        self.derive()
        self.ss.comp_ss = self.tw.graph.ss
        self._solver = CTMCSolution(self.ss, self.args["solver"])
        self._solver.solve_steady()

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
        self._prepare_components()
        visitor = ComponentStateVisitor(self.tw.graph, output_dir = out_dir)
        for comp in set(self.ss.components):
            comptmp = ComponentSSGraph(comp.data)
            self.components[comp.data] = visitor.generate_ss(comp.data,
                                                             comptmp)
        for comp in set(self.ss.components):
            visitor.get_dot(comp.data)
        res, act = self.ss.derive(dotdir=out_dir)
        dotmodel = []
        dotmodel.append('digraph "{}" {{\n'.format(self.name))
        for state in res:
            for tos in res[state][0]:
                dotmodel.append('"{}" -> "{}" [label="{}" fontsize=10]\n'.format(state,tos[1], tos[2]))
        dotmodel.append("}")
        with open("{}/{}.dot".format(out_dir, self.name), "w") as f:
            [f.write(x) for x in dotmodel]





