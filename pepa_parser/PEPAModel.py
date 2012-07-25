#/usr/bin/env python
import logging
from pprint import pprint
import sys
from PEPATreeWalker import PEPATreeWalker
from PEPAParser import PEPAParser
from pyparsing import ParseException
from ComponentSSGraph import ComponentSSGraph

class SS():
    pass

class ComponentStateVisitor():

    def __init__(self, graph):
        self.graph = graph
        self.visited = []
        self.dot = ""

    def generate_ss(self, node, comp):
        self.visited = []
        return self._visit_for_ss(node,comp)

    def _visit_for_ss(self, node, comp):
        self.visited.append(node)
        comp.ss[node] = self.graph.ss[node]
        transitions = self.graph.ss[node].transitions
        for tran in transitions:
            if tran.action in self.graph.shared_actions:
                comp.shared.append( (tran.action, tran.rate) )
            comp.activities.append( (tran.action, tran.rate) )
            if tran.to not in self.visited:
                self._visit_for_ss(tran.to, comp)
        return comp

    def visit_print(self, node):
        self.visited.append(node)
        transitions = self.graph.ss[node].transitions
        for tran in transitions:
            print(node + " -> " + tran.to)
            if tran.to not in self.visited:
                self.visit_print(tran.to)

    def get_dot(self, node):
        with open("dots/"+node + ".dot", "w") as f:
            self.dot = "digraph " + node + "{\n"
            self._visit_dot(node)
            self.dot += "}\n"
            f.write(self.dot)
        return self.dot

    def _visit_dot(self, node):
        self.visited.append(node)
        transitions = self.graph.ss[node].transitions
        for tran in transitions:
            if tran.action in self.graph.shared_actions:
                self.dot += "\"" + node + "\" -> \"" + tran.to + "\"" + \
                " [label=\"(" + tran.action + "," + tran.rate + ")\" \
                fontsize=10, fontcolor=red]\n"
            else:
                self.dot += "\"" + node + "\" -> \"" + tran.to + "\"" + " [label=\"(" + tran.action + "," + tran.rate + ")\" fontsize=10]\n"
            if tran.to not in self.visited:
                self._visit_dot(tran.to)


class PEPAModel():
    """
        Representation of a final PEPA model, everything needed to derive CTMC
        - state spaces of components that are present in a system equation
        - rate definitions
        - system equation
    """
    def __init__(self, modelfile):
        """ Create PEPA model instance and fill the fields

        Keyword arguments:
        modelfile --- path to the model file
        """
        self.processes = {}
        self.systemeq = None
        self.rate_definitions = {}
        self.components = {}
        self.seq_processes = {}
        self.global_state_start = None
        self.tw = PEPATreeWalker()
        self.log = logging.getLogger(__name__)
        self._parse_read_model(modelfile)
        self._prepare_systemeq()
        self._prepare_trees()
        self._generate_components()
        self._generate_model_ss()

    def _gs_to_string(self, gs_list):
        return ','.join( map( str, gs_list ) )

    def _generate_model_ss(self):
        """ Generates global state space work in progress
        """
        visit_queue = []
        self.log.debug("First state (" + self._gs_to_string(self.global_state_start) + ")")
        visit_queue.append(self.global_state_start)
        veni_vidi_vici = []
        while(visit_queue):
            enabled = []
            shared = []
            state = visit_queue.pop()
            print("IN STATE (" + self._gs_to_string(state) + ")")
            for proc in state:
                print("Component " + proc)
                pprint(shared)
                trans = self.tw.graph.ss[proc].transitions
                for tr in trans:
                    ty = " "
                    if tr.action in self.tw.shared_actions:
                        ty = " shared"
                        shared.append( ( tr.action, tr.rate, proc ,tr.to ) )
                    else:
                        enabled.append( ( tr.action, tr.rate, proc, tr.to) )
                    print("\tEnabled " + tr.action + " " + tr.rate +  ty + " to " + tr.to)
            # deal with independent actions
            for en in enabled:
                # we copy array
                stat = []
                stat = state[:]
                loc = stat.index(en[2])
                stat[loc] = en[3]
                if stat not in veni_vidi_vici:
                    visit_queue.append(stat)
                print("\tNEXT(i) ("+self._gs_to_string(stat) + ") action " + en[0] )
            # deal with shared actions
            shared_queue = []
            shared_transitions = []
            # TODO: zmienic - IDIOTYZM
            j = 0
            print("SHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAARED")
            for sh in shared:
                stat = []
                stat = state[:]
                pprint(stat)
                if sh[1] != "infty":
                    # now find matching guys
                    i = 0
                    indices = []
                    print("SH -- " + str(j))
                    pprint(sh)
                    for sh2 in shared:
                        if sh2[0] == sh[0] and i != j:
                            print("\tznalazl " + str(sh2))
                            indices.append(i)
                        i = i + 1
                    loc = stat.index(sh[2])
                    stat[loc] = sh[3]
                    print(shared)
                    print(indices)
                    for elem in indices:
                        loc = stat.index(shared[ elem ][2])
                        stat[loc] = shared[ elem ][3]
                        if stat not in veni_vidi_vici:
                            visit_queue.append(stat)
                        print("\tNEXT(s) ("+self._gs_to_string(stat) + ")" )
                j = j + 1



    def _findall(self, L, test):
        i=0
        indices = []
        while(True):
            try:
                nextvalue = filter(test, L[i:])[0]
                indices.append(L.index(nextvalue, i ))
                i = indices[-1]+1
            except IndexError:
                return indices



    def _generate_components(self):
        """
        Generates state space graphs for every component
        in the model into components dict
        """
        visitor = ComponentStateVisitor(self.tw.graph)
        for comp in self.seq_processes.keys():
            self.components[comp] = ComponentSSGraph(comp)
            self.components[comp] = visitor.generate_ss(comp, self.components[comp])

    def _prepare_systemeq(self):
        """
        Derives components taking part in processing into dict
        where key is name, values is number of processes
        TODO: aggregation should be here
        """
        self.log.debug("Preparing systemeq")
        self.seq_processes, self.global_state_start = self.tw.derive_systemeq(self.systemeq)

    def _parse_read_model(self, modelfile):
        """ Reads model file and parses it.
        """
        with open(modelfile, "r") as f:
            modelfile = f.read()
        try:
            parser = PEPAParser(False)
            (self.processes, self.rate_definitions, self.systemeq) = parser.parse(modelfile)
        except Exception as e:
            self.log.debug(e)
            print("Parsing error : " + e.msg )
            sys.exit(1)

    def _prepare_trees(self):
        """ Here ss graphs of every process is derived from AST trees
        """
        for node in self.processes.values():
            self.tw.derive_processes_ss(node)

    def generate_dots(self):
        visitor = ComponentStateVisitor(self.tw.graph)
        for comp in self.seq_processes.keys():
            visitor.get_dot(comp)



