#!/usr/bin/env python

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


